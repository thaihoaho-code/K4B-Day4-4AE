import json
from pathlib import Path
from datetime import datetime
import sys
import os

sys.path.insert(0, str(Path(__file__).parent.parent))

from env_loader import load_lab_env
from providers import make_provider
from tools import load_tool_declarations, to_openai_tools
from versioning import build_artifact_version, artifact_version_dict
from chat import run_model_tool_loop, now_iso, safe_slug

sys.stdout.reconfigure(encoding='utf-8')

ROOT = Path(os.path.abspath(__file__)).parent.parent
load_lab_env(ROOT)

system_prompt_path = ROOT / "artifacts" / "system_prompt.md"
tools_path = ROOT / "artifacts" / "tools.yaml"
transcripts_dir = ROOT / "transcripts"
transcripts_dir.mkdir(exist_ok=True)

system_prompt = system_prompt_path.read_text(encoding="utf-8")
tool_declarations = load_tool_declarations(tools_path)
openai_tools = to_openai_tools(tool_declarations)
provider = make_provider("openai")
model = getattr(provider, "default_model", None)
artifact_version = build_artifact_version("v3", system_prompt_path, tools_path)

timestamp = datetime.now().strftime("%Y%m%dT%H%M%S%f")
transcript_id = f"v3_demo_evidence_{timestamp}"
transcript_path = transcripts_dir / f"{transcript_id}.transcript.json"

transcript = {
    "transcript_id": transcript_id,
    **artifact_version_dict(artifact_version),
    "provider": "openai",
    "model": model,
    "system_prompt": str(system_prompt_path),
    "tools": str(tools_path),
    "history_window": 5,
    "max_tool_rounds": 4,
    "created_at": now_iso(),
    "updated_at": now_iso(),
    "turns": [],
}

scenarios = [
    "Kiểm tra giúp tôi trạng thái hệ thống VPN production.", 
    "Laptop của tôi kết nối wifi bị lỗi.", 
    "Mã máy của tôi là LT-204.", 
    "Tạo ticket lỗi wifi cho máy này, ưu tiên cao nhé.", 
    "Tôi đồng ý tạo." 
]

history = []
turn_index = 0

print("Generating transcript...")

for user_text in scenarios:
    turn_index += 1
    print(f"\nUser: {user_text}")
    
    messages = [{"role": "system", "content": system_prompt}]
    for t in history[-10:]:
        messages.append(t)
    messages.append({"role": "user", "content": user_text})
    
    turn_record = {
        "turn_index": turn_index,
        "started_at": now_iso(),
        "user": user_text,
        "status": "started",
        "assistant_text": None,
        "rounds": [],
        "tool_events": [],
    }
    
    try:
        result = run_model_tool_loop(
            provider=provider,
            messages=messages,
            tools=openai_tools,
            model=model,
            max_tool_rounds=4
        )
        turn_record.update(result)
        assistant_text = result.get("assistant_text", "")
        history.append({"role": "user", "content": user_text})
        history.append({"role": "assistant", "content": assistant_text})
        
        # print tools called
        if result.get("tool_events"):
            for ev in result["tool_events"]:
                print(f"  -> Tool called: {ev['tool']} with args: {ev['args']}")
        
        print(f"Agent: {assistant_text}")
    except Exception as exc:
        turn_record.update({"status": "provider_error", "error": str(exc)})
        print(f"Error: {exc}")
    
    turn_record["ended_at"] = now_iso()
    transcript["turns"].append(turn_record)
    
transcript["updated_at"] = now_iso()
transcript_path.write_text(json.dumps(transcript, ensure_ascii=False, indent=2), encoding="utf-8")
print(f"\nSaved to {transcript_path.name}")
