import streamlit as st
import json
from pathlib import Path
from datetime import datetime

from env_loader import load_lab_env
from providers import make_provider
from tools import load_tool_declarations, to_openai_tools
from versioning import build_artifact_version, artifact_version_dict
from chat import run_model_tool_loop, now_iso, safe_slug, write_transcript

ROOT = Path(__file__).parent
load_lab_env(ROOT)

# --- Configuration ---
st.set_page_config(page_title="Northstar IT Agent", page_icon="⚡", layout="wide")

# --- Custom CSS (Modern Look) ---
st.markdown("""
<style>
    .modern-header { text-align: center; padding: 1rem 0 2rem 0; font-family: 'Inter', sans-serif; }
    .modern-header h1 { font-size: 2.5rem; font-weight: 700; background: -webkit-linear-gradient(45deg, #2196F3, #00BCD4); -webkit-background-clip: text; -webkit-text-fill-color: transparent; margin-bottom: 0.5rem; }
    .modern-header p { color: #6B7280; font-size: 1.1rem; font-weight: 400; }
    .status-pill { display: inline-block; padding: 4px 12px; border-radius: 50px; font-size: 0.8rem; font-weight: 600; letter-spacing: 0.5px; margin-bottom: 12px; text-transform: uppercase; }
    .pill-success { background: rgba(16, 185, 129, 0.1); color: #10B981; border: 1px solid rgba(16, 185, 129, 0.2); }
    .pill-warning { background: rgba(245, 158, 11, 0.1); color: #F59E0B; border: 1px solid rgba(245, 158, 11, 0.2); }
    .pill-error   { background: rgba(239, 68, 68, 0.1); color: #EF4444; border: 1px solid rgba(239, 68, 68, 0.2); }
    .block-container { padding-top: 2rem; }
</style>
<div class='modern-header'>
    <h1>⚡ Northstar IT Agent</h1>
    <p>Hệ thống hỗ trợ kỹ thuật thông minh thế hệ mới</p>
</div>
""", unsafe_allow_html=True)

def reset_session():
    st.session_state.messages = []
    st.session_state.history = []
    if "transcript" in st.session_state:
        del st.session_state["transcript"]

# --- Minimal Sidebar ---
with st.sidebar:
    st.markdown("### ⚙️ Cấu hình")
    provider_name = st.selectbox("Provider", ["gemini", "openai", "openrouter", "anthropic"], index=1, on_change=reset_session)
    version_label = st.text_input("Version", value="v3", on_change=reset_session)
    
    st.write("") # Spacing
    if st.button("✨ Bắt đầu phiên mới", use_container_width=True):
        reset_session()
        st.rerun()

# --- System Initialization ---
try:
    system_prompt_path = ROOT / "artifacts" / "system_prompt.md"
    tools_path = ROOT / "artifacts" / "tools.yaml"
    
    system_prompt = system_prompt_path.read_text(encoding="utf-8")
    tool_declarations = load_tool_declarations(tools_path)
    openai_tools = to_openai_tools(tool_declarations)
    provider = make_provider(provider_name)
    artifact_version = build_artifact_version(version_label, system_prompt_path, tools_path)
except Exception as e:
    st.error(f"🚨 Lỗi khởi tạo: {e}")
    st.stop()

# --- State Management & Transcript Setup ---
if "messages" not in st.session_state:
    st.session_state.messages = []
if "history" not in st.session_state:
    st.session_state.history = []
    
if "transcript" not in st.session_state:
    timestamp = datetime.now().strftime("%Y%m%dT%H%M%S%f")
    transcript_id = f"{safe_slug(version_label)}_{safe_slug(provider_name)}_{timestamp}"
    st.session_state.transcript_path = ROOT / "transcripts" / f"{transcript_id}.transcript.json"
    st.session_state.transcript = {
        "transcript_id": transcript_id,
        **artifact_version_dict(artifact_version),
        "provider": provider_name,
        "model": getattr(provider, "default_model", None),
        "system_prompt": str(system_prompt_path),
        "tools": str(tools_path),
        "history_window": 5,
        "max_tool_rounds": 4,
        "created_at": now_iso(),
        "updated_at": now_iso(),
        "turns": [],
    }
    st.session_state.turn_index = 0

def render_tool_event(event):
    res = event.get('result', {})
    is_error = 'error' in res
    status_state = "error" if is_error else "complete"
    
    with st.status(f"Gọi công cụ: **{event['tool']}**", state=status_state, expanded=False):
        st.markdown("**📥 Input:**")
        st.json(event['args'])
        
        st.markdown("**📤 Output:**")
        if is_error:
            st.error(f"{res['error']}: {res.get('message', '')}")
        else:
            st.json(res)

# --- Render Chat History ---
for msg in st.session_state.messages:
    avatar = "🧑‍💻" if msg["role"] == "user" else "⚡"
    with st.chat_message(msg["role"], avatar=avatar):
        if msg["role"] == "assistant":
            if "status" in msg:
                status_html = ""
                if msg["status"] == "answered":
                    status_html = "<div class='status-pill pill-success'>Hoàn thành</div>"
                elif msg["status"] == "waiting_for_user":
                    status_html = "<div class='status-pill pill-warning'>Cần xác nhận</div>"
                elif msg["status"] == "max_tool_rounds":
                    status_html = "<div class='status-pill pill-error'>Quá tải vòng lặp</div>"
                
                if status_html:
                    st.markdown(status_html, unsafe_allow_html=True)

            if "rounds" in msg and msg["rounds"]:
                for r in msg["rounds"]:
                    for event in r.get("tool_results", []):
                        render_tool_event(event)
        
        st.markdown(msg["content"])

# --- User Input & Processing ---
if prompt := st.chat_input("Hỏi tôi về sự cố IT, kiểm tra máy tính, hoặc tạo ticket..."):
    # 1. Show UI immediately
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user", avatar="🧑‍💻"):
        st.markdown(prompt)

    # 2. Setup transcript turn record
    st.session_state.turn_index += 1
    turn_record = {
        "turn_index": st.session_state.turn_index,
        "started_at": now_iso(),
        "user": prompt,
        "status": "started",
        "assistant_text": None,
        "rounds": [],
        "tool_events": [],
    }

    # 3. Build Context
    recent_history = st.session_state.history[-5:]
    model_messages = [{"role": "system", "content": system_prompt}]
    for turn in recent_history:
        model_messages.append({"role": "user", "content": turn["user"]})
        model_messages.append({"role": "assistant", "content": turn["assistant"]})
    model_messages.append({"role": "user", "content": prompt})

    # 4. Process
    with st.chat_message("assistant", avatar="⚡"):
        with st.spinner("Đang phân tích yêu cầu..."):
            try:
                result = run_model_tool_loop(
                    provider=provider,
                    messages=model_messages,
                    tools=openai_tools,
                    model=None,
                    max_tool_rounds=4
                )
                
                bot_text = result.get("assistant_text", "")
                rounds = result.get("rounds", [])
                status = result.get("status", "unknown")
                
                # --- Auto Save Transcript ---
                turn_record.update(result)
                turn_record["ended_at"] = now_iso()
                st.session_state.transcript["turns"].append(turn_record)
                write_transcript(st.session_state.transcript_path, st.session_state.transcript)
                
                # --- Render UI Updates ---
                status_html = ""
                if status == "answered":
                    status_html = "<div class='status-pill pill-success'>Hoàn thành</div>"
                elif status == "waiting_for_user":
                    status_html = "<div class='status-pill pill-warning'>Cần xác nhận</div>"
                elif status == "max_tool_rounds":
                    status_html = "<div class='status-pill pill-error'>Quá tải vòng lặp</div>"
                
                if status_html:
                    st.markdown(status_html, unsafe_allow_html=True)
                
                for r in rounds:
                    for event in r.get("tool_results", []):
                        render_tool_event(event)
                
                st.markdown(bot_text)
                st.caption(f"📝 Đã lưu transcript tự động vào: {st.session_state.transcript_path.name}")
                
                # --- Update State ---
                st.session_state.messages.append({
                    "role": "assistant",
                    "content": bot_text,
                    "rounds": rounds,
                    "status": status
                })
                
                st.session_state.history.append({
                    "user": prompt,
                    "assistant": bot_text
                })
                
            except Exception as e:
                st.error(f"🚨 Provider Error: {str(e)}")
                turn_record.update({"status": "provider_error", "error": str(e), "ended_at": now_iso()})
                st.session_state.transcript["turns"].append(turn_record)
                write_transcript(st.session_state.transcript_path, st.session_state.transcript)
