# TEAM — Day04, K4-L3B

**Làm nhóm.** Mỗi người tự viết và commit phần INDIVIDUAL của mình.

## Thông tin bài nộp

- Tên nhóm: 4AE
- Người đại diện / MSSV: Hồ Thái Hòa / 2A202602915
- Tên repo: `K4B-Day4-4AE`
- URL repo, nhánh nộp, commit chốt: `https://github.com/thaihoaho-code/K4B-Day4-4AE` | Nhánh: `main` | Commit chốt: `docs: finalize report and team submission metadata`
- Deadline áp dụng và link thông báo đổi hạn nếu có: `12:00 ngày 16/09/2026`

## Thành viên

| Họ và tên | MSSV | GitHub | Vai trò và công việc | File/commit/PR |
|---|---|---|---|---|
| Hồ Thái Hòa | 2A202602915 | @thaihoaho-code | Sửa lỗi wrong-boundary, xây dựng UI Streamlit, xử lý merge conflict | nhánh `fix/wrong-boundary`, file: `app.py`, `system_prompt.md`, `tools.yaml` |
| Nguyễn Văn Hồng | 2A202602800 | @hongneuk65 | Sửa lỗi missing-info, cấu hình Zero-Guessing | nhánh `fix/missing-info`, file: `system_prompt.md`, `tools.yaml` |
| Nguyễn Đình Lâm Phúc | 2A202602986 | @NguyenDinhLamPhuc | Sửa lỗi wrong-tool, tạo 10 test cases mới | nhánh `fix/wrong-tool`, file: `eval_group.json`, `tools.yaml` |
| Lê Minh Sang | 2A202602864 | @minhsangmr | Chạy baseline v0, quản lý `\runs`, quản lý version_log và báo cáo | file: `version_log.csv`, `REPORT.md` |

## Nhận xét chung

- **Kết quả và bằng chứng:** Hệ thống đạt 100% (30/30) `case_accuracy` trên bộ test cơ sở (`v3_B_base_openai`). Tất cả các lỗi `wrong_tool`, `missing_info` và `wrong_boundary` đều đã được xử lý triệt để. Bằng chứng log được ghi nhận đầy đủ trong thư mục `runs/` và theo dõi minh bạch tiến trình tại `artifacts/version_log.csv`.
- **Thay đổi hiệu quả nhất:** Việc định nghĩa lại ranh giới của công cụ `clarify` (chia thành các điều kiện bắt buộc rõ ràng) kết hợp với "Zero-Guessing Policy" (chính sách chống đoán mò) trong `system_prompt.md`. Đây là thay đổi mang lại tác động lớn nhất, dập tắt hoàn toàn tình trạng ảo giác tham số của Agent.
- **Giới hạn còn lại:** Dù hoàn hảo ở bộ test cơ bản, hệ thống vẫn còn một số sơ hở trên bộ test tấn công bảo mật (`eval_adversarial.json`). Agent đôi khi vẫn bị lừa bởi các dữ liệu JSON giả mạo do người dùng nhúng vào (`Forged Tool Result`), hoặc bị đánh lừa để tìm kiếm lộ lọt mã định danh nội bộ ra ngoài web. 
- **Cách phân công và tích hợp:** Nhóm làm việc song song hiệu quả bằng cách phân công công việc theo từng nhóm lỗi (`failure_type`). Mỗi thành viên tạo một Git branch riêng biệt (ví dụ: `fix/missing-info`, `fix/wrong-boundary`, `fix/wrong-tool`) để sửa lỗi. Mã nguồn được tích hợp về nhánh `main` thông qua việc xử lý trực tiếp các Merge Conflict (nhất là tại `tools.yaml` khi logic giao thoa).

## INDIVIDUAL

### Hồ Thái Hòa — 2A202602915

- **Phần việc và file/commit/PR:** 
  - Phụ trách nhánh `fix/wrong-boundary`, xử lý lỗi Agent tự ý ghi dữ liệu mà không xin phép người dùng. (Các commit: `f368247d`, `19428511`)
  - Cập nhật `artifacts/system_prompt.md` (thêm mục `Write Actions`) và `artifacts/tools.yaml` (ràng buộc kỹ tool `create_ticket` và `clarify`). Ghi nhận đo lường ở phiên bản `v1` (tăng case accuracy từ 66.67% lên 80%). (Commit: `b7d84f25`)
  - Trực tiếp xử lý merge conflict khi gộp nhánh `fix/wrong-boundary` với nhánh `fix/missing-info` của teammate. (Commit: `0e74eca8`)
  - Phân tích bộ test bảo mật `eval_adversarial.json` ở bản `v3`. (Commit: `f3c6039e`)
  - Xây dựng giao diện Web Chat hiện đại bằng Streamlit (`app.py`), tích hợp hiển thị luồng tool gọi đa bước (multi-turn), và cập nhật tài liệu `README.md`. (Commit: `fef162ce`)
- **Quyết định, khó khăn và cách xử lý:** 
  - *Khó khăn:* Khi merge hai nhánh, file `tools.yaml` bị conflict tại description của tool `clarify` do hai người cùng sửa logic.
  - *Cách xử lý:* Phân tích và resolve conflict bằng tay, gộp cả điều kiện "thiếu thông tin" và "xác nhận ghi dữ liệu" thành một danh sách quy tắc rõ ràng, bảo toàn logic của cả hai nhánh.
- **Điều đã học:** 
  - Hiểu sâu về cách dùng Prompt Engineering để "rào" ranh giới (boundary) của Agent, ngăn chặn mô hình vượt quyền.
  - Hiểu được các phương thức tấn công thao túng (Adversarial attacks) như Stale Confirmation hay Data Exfiltration thông qua phân tích test cases v3.
  - Cách làm việc nhóm song song hiệu quả: chia mỗi người fix một loại `failure_type` trên một Git branch riêng để hạn chế tối đa conflict.
- **AI/công cụ đã dùng và cách kiểm tra:** 
  - Dùng AI để phân tích và trích xuất dữ liệu từ các file log JSON phức tạp (`v0_B_base`, `v3_B_adversarial`), hỗ trợ sinh code layout cho giao diện Streamlit.
  - Luôn kiểm chứng bằng cách chạy thực tế `python run_eval.py --provider openai` và so sánh metric trước/sau trước khi tạo commit chốt.
- **Thời điểm đã tự nộp URL repo chung trên VLearn:** 09:46:12 16/9/2026

### Nguyễn Văn Hồng — 2A202602800

- **Phần việc và file/commit/PR:** 
  - Phụ trách nhánh `fix/missing-info`, giải quyết triệt để lỗi Agent tự đoán mò dữ liệu (ảo giác tham số) khi người dùng cung cấp thiếu thông tin. (Commit: `ce179e1d`)
  - Viết thêm mục `Zero-Guessing Policy` vào `artifacts/system_prompt.md` và tinh chỉnh schema trong `artifacts/tools.yaml` (yêu cầu gọi `clarify` thay vì tự điền bừa). (Commit: `72bc30ea`)
  - Ghi nhận đo lường ở phiên bản `v2` trong `version_log.csv` (giúp tăng case accuracy từ 80.0% lên 83.33% và xóa sạch lỗi `missing_info`).
- **Quyết định, khó khăn và cách xử lý:** 
  - *Khó khăn:* Agent thường xuyên có xu hướng "chiều" người dùng bằng cách tự bịa mã tài sản (vd: nhập "laptop" vào `asset_id`) hoặc lấy tên phòng ban làm mã nhân viên khi user không cung cấp đúng định dạng.
  - *Cách xử lý:* Thay vì chỉ bảo mô hình "không được đoán", tôi quyết định đưa ra các rule định dạng cứng (phải có prefix `LT-xxx`, `EMP-xxx`) và yêu cầu mô hình gọi `clarify(response_type="text")` ngay lập tức nếu không thấy chuỗi định dạng này.
- **Điều đã học:** 
  - Hiểu được tầm quan trọng của Schema Guidance: LLM dễ bị ảo giác nếu mô tả trường tham số (properties description) quá chung chung.
  - Học được kỹ năng Zero-shot Prompting để bắt buộc mô hình phải hỏi lại người dùng trong các môi trường mơ hồ (như "demo", "QA").
- **AI/công cụ đã dùng và cách kiểm tra:** 
  - Sử dụng AI để rà soát các case fail do `wrong_arg_value` và `missing_tool_call` trong log `v1_B_base_openai...`.
  - Kiểm thử trực tiếp bằng CLI Chat nội bộ (gõ thử các câu lệnh không đầy đủ) để xem phản xạ của hệ thống trước khi chạy eval tổng.
- **Thời điểm đã tự nộp URL repo chung trên VLearn:** Đã nộp lúc 00:00:55 16/9/2026

### Nguyễn Đình Lâm Phúc — 2A202602986

- **Phần việc và file/commit/PR:** 
  - Phân tích log lỗi `wrong_tool` (cụ thể ở các case H03, H04, H13, H17) và đảm nhiệm xử lý nhánh `fix/wrong-tool`. (Commit: `8d5d11a1`)
  - Cải thiện mô tả của các công cụ `search_kb`, `lookup_user` và `inspect_device` trong `artifacts/tools.yaml` để siết chặt ranh giới chọn tool. Ghi nhận đo lường ở phiên bản `v3` (tăng case accuracy lên tuyệt đối 100%). (Commit: `ff318bc1`)
  - Xây dựng bộ dữ liệu kiểm thử riêng của nhóm `starter_v0/data/eval_group.json` gồm 10 tình huống mới (5 một lượt và 5 nhiều lượt), tham khảo tiêu chuẩn từ bộ adversarial. (Commit: `15e857ac`)
- **Quyết định, khó khăn và cách xử lý:** 
  - *Khó khăn:* Lỗi gắn nhãn `wrong_tool` rất dễ gây nhầm lẫn (có thể là gọi sai tool, sai/thiếu tham số, hoặc gọi thừa một tool không cần thiết).
  - *Cách xử lý:* Thay vì sửa mù mờ, tôi đối chiếu chéo giữa `failure_type` và `observed_mismatch` trong logic chấm điểm để bắt đúng gốc rễ vấn đề. Riêng bộ test nhóm, quyết định bổ sung thêm tiêu chí đánh giá thủ công (`manual_review`) cho các câu trả lời mà hệ thống tự động không kiểm tra được.
- **Điều đã học:** 
  - Phân biệt được sự khác nhau giữa lỗi chọn tool (routing), lỗi truyền tham số (argument) và hiểu cơ chế chấm điểm: `case_failure_type`, `failure_type` vs `observed_mismatch`.
  - Nắm được cách thiết kế bộ test case chất lượng, bao trùm các tình huống như: xác nhận/hủy yêu cầu, giả mạo chỉ dẫn (spoofing) và bảo vệ dữ liệu nội bộ.
- **AI/công cụ đã dùng và cách kiểm tra:** 
  - Dùng AI (Codex/Gemini) hỗ trợ bóc tách, phân tích file run JSON, và gợi ý soạn thảo bộ test nhóm.
  - Phân biệt rõ việc một file JSON hợp lệ về cú pháp hoàn toàn không đồng nghĩa với việc Agent đã hành xử đúng kỳ vọng bài test.
- **Thời điểm đã tự nộp URL repo chung trên VLearn:** 11:00 16/9/2026

### Lê Minh Sang — 2A202602864

- **Phần việc và file/commit/PR:** 
  - Đảm nhiệm vai trò quản lý dự án & tổng hợp: thiết lập môi trường chạy baseline (`v0`) và kiểm soát toàn bộ file trong `/runs` và `artifacts/version_log.csv` (đảm bảo các giả thuyết và metric từ v0 -> v3 được ghi nhận chính xác). (Các commit: `642bfee2`, `34352f81`)
  - Chịu trách nhiệm chính trong việc biên soạn file báo cáo tổng kết `artifacts/REPORT.md`.
  - Phân tích và viết mục "Nhận xét chung" cho toàn đội trong `TEAM.md`, đánh giá hiệu quả thay đổi và các giới hạn còn sót lại của hệ thống.
- **Quyết định, khó khăn và cách xử lý:** 
  - *Khó khăn:* Khi chạy đánh giá ban đầu, rate limit của Gemini (lỗi `429`) làm hỏng log khiến không thể chốt baseline. Đồng thời việc gom log từ nhiều nhánh của các bạn rất dễ gây sai lệch mã băm (hash version).
  - *Cách xử lý:* Chủ động chuyển sang chạy API OpenAI để chốt file JSON chuẩn làm baseline (accuracy 66.67%). Để báo cáo chính xác, tôi đặt quy tắc buộc các thành viên phải cung cấp đủ file run JSON hợp lệ (`provider_error_cases == 0`) trước khi tôi cập nhật chúng vào `version_log.csv`.
- **Điều đã học:** 
  - Cải thiện mạnh mẽ kỹ năng viết tài liệu kỹ thuật (Technical Writing) và quản lý tiến độ nhóm qua Git.
  - Học được cốt lõi của quy trình Eval: Không thể chứng minh Prompt tốt lên nếu thiếu một baseline sạch và một bảng tracking metric (trước/sau) có tính đối chứng nghiêm ngặt.
- **AI/công cụ đã dùng và cách kiểm tra:** 
  - Thao tác trực tiếp với `run_eval.py` để đo đạc. Sử dụng AI (Gemini/ChatGPT) để rà soát logic, tinh chỉnh văn phong và định dạng lại cấu trúc markdown của file `REPORT.md`.
- **Thời điểm đã tự nộp URL repo chung trên VLearn:** 09:41:24 16/9/2026
