# TEAM — Day04, K4-L3B

**Làm nhóm.** Mỗi người tự viết và commit phần INDIVIDUAL của mình.

## Thông tin bài nộp

- Tên nhóm:4AE
- Người đại diện / MSSV:Hồ Thái Hòa / 2A202602915
- Tên repo: `K4-L3-DAY04-HoVaTen-MSSV-PromptEngineeringToolCalling`
- URL repo, nhánh nộp, commit chốt:
- Deadline áp dụng và link thông báo đổi hạn nếu có:

## Thành viên

| Họ và tên | MSSV | GitHub | Vai trò và công việc | File/commit/PR |
|---|---|---|---|---|
| | | | | |

## Nhận xét chung

- Kết quả và bằng chứng:
- Thay đổi hiệu quả nhất:
- Giới hạn còn lại:
- Cách phân công và tích hợp:

## INDIVIDUAL

Sao chép mục này cho từng thành viên.

### Họ và tên — MSSV: Nguyễn Đình Lâm Phúc - 2A202602986

- Phần việc và file/commit/PR: Phân tích kết quả chạy OpenAI v0 trong starter_v0/runs/v0_B_base_openai_20260915T190024665013.json, xác định 4 test được gắn lỗi wrong_tool: H03, H04, H13 và H17. Đối chiếu công cụ, tham số kỳ vọng với thực tế; đề xuất cải thiện mô tả search_kb, lookup_user và inspect_device trong starter_v0/artifacts/tools.yaml. Xây dựng bộ starter_v0/data/eval_group.json gồm 10 tình huống mới: 5 một lượt và 5 nhiều lượt, tham khảo các ranh giới an toàn trong bộ adversarial.

Link Commit: https://github.com/VinUni-AI20k/K4-L3B-Day04-Prompt-Engineering-Tool-Calling-Labs/commit/15e857ac0ea32746aa5e73657bfb24e488c5fd37

Link PR: https://github.com/VinUni-AI20k/K4-L3B-Day04-Prompt-Engineering-Tool-Calling-Labs/pull/54

- Quyết định, khó khăn và cách xử lý: Giữ nguyên tên tool và bộ test có sẵn; tập trung đề xuất sửa mô tả tool và tham số. Khó khăn là nhãn wrong_tool không luôn có nghĩa chọn sai công cụ: ba trường hợp thực tế sai hoặc thiếu tham số, một trường hợp gọi thừa công cụ. Tôi đối chiếu thêm observed_mismatch, failures và logic chấm điểm để xác định đúng vấn đề. Với bộ test nhóm, bổ sung manual_review cho những yêu cầu về nội dung trả lời mà bộ chấm tự động chưa kiểm tra.
- Điều đã học: Phân biệt lỗi chọn tool, lỗi tham số và lỗi thực thi tool; hiểu sự khác nhau giữa case_failure_type, failure_type và observed_mismatch. Biết xây dựng giả thuyết cải tiến có thể kiểm chứng bằng cùng bộ test, đồng thời thiết kế tình huống kiểm tra xác nhận, hủy yêu cầu, giả mạo chỉ dẫn và bảo vệ dữ liệu nội bộ.
- AI/công cụ đã dùng và cách kiểm tra:Sử dụng Codex để hỗ trợ phân tích run JSON, đề xuất mô tả tool và soạn bộ test nhóm. Phân biệt kiểm tra cấu trúc dữ liệu với đánh giá hành vi model; không coi JSON hợp lệ là bằng chứng agent đã vượt qua test.
- Thời điểm đã tự nộp URL repo chung trên VLearn: 11:00 16/9/2026
