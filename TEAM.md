# TEAM — Day04, K4-L3B

**Làm nhóm.** Mỗi người tự viết và commit phần INDIVIDUAL của mình.

## Thông tin bài nộp

- Tên nhóm:
- Người đại diện / MSSV:
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

### Nguyễn Văn Hồng — 2A202602800

- Phần việc và file/commit/PR: Xử lý phần lỗi `missing info` trong run v2, thay đổi tool `clarify`, `inspect_device`, `lookup_user` và` check_service_status `  trong file `tools.yaml` và thêm trong file `system_prompt.md` commit `fix missing info` 
- Quyết định, khó khăn và cách xử lý: Không sửa bộ test gốc. Tách ba nguyên nhân: (1) thiếu mã tài sản phải gọi `clarify` dạng `text`; (2) thiếu mã nhân viên phải gọi `clarify` dạng `text`; (3) môi trường ngoài `production`/`staging` phải gọi `clarify` dạng `choice`. Mô tả tool được làm rõ để hướng dẫn lựa chọn, còn system prompt đặt quy tắc cấm đoán mò. Baseline cho thấy `H10` đã gọi `inspect_device(asset_id="laptop")`, `H11` gọi `lookup_user(employee_id="Sales")`, và `H19` gọi `check_service_status(environment="staging")`, đều không đúng kỳ vọng.
- Điều đã học: `required` trong schema chỉ buộc model gửi một trường, không đảm bảo giá trị được gửi là định danh hợp lệ. Vì vậy cần kết hợp schema/mô tả tool với luật quyết định trong system prompt; đồng thời phải xác nhận bằng run mới, không suy luận rằng thay đổi prompt chắc chắn đã pass.
- AI/công cụ đã dùng và cách kiểm tra: Dùng `scripts/parse_runs.py` để đọc từng case và đối chiếu `expected_tool_calls` với `actual_tool_calls`; đọc trực tiếp JSON run và kiểm tra SHA-256 artifact bằng `versioning.py`/script Python. Không dùng dữ liệu thật, mật khẩu, OTP, token hoặc khóa truy cập.
- Thời điểm đã tự nộp URL repo chung trên VLearn: Đã nộp lúc 00:00:55 16/9/2026



