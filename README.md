# 💼 JobFIT - Match your CV with JD

## Giới thiệu
**JobFIT** là hệ thống hỗ trợ người dùng phân tích mức độ phù hợp giữa CV (PDF/DOCX) và Mô tả Công việc (JD), cung cấp điểm tương đồng (Match Score) và gợi ý cải thiện dựa trên Mô hình Ngôn ngữ Lớn (LLM). Dự án sử dụng Flask để xây dựng backend, render giao diện bằng HTML templates, và hỗ trợ triển khai với Docker. 

JobFIT được thiết kế để dễ mở rộng, bảo trì, và là nền tảng lý tưởng cho các nhà phát triển muốn đóng góp vào một hệ thống phân tích CV thông minh. 🚀

---

## Tính năng

### Chức năng chính
- **Tải lên CV**: Hỗ trợ file PDF hoặc DOCX.
- **Nhập/Tải JD**: Nhập JD dạng văn bản hoặc tải file.
- **Trích xuất văn bản**: Trích xuất nội dung từ CV và JD.
- **Xử lý lỗi**: Thông báo lỗi khi upload hoặc phân tích thất bại.
- **Prompt động**: Tùy chỉnh prompt LLM cho từng cặp CV-JD.
- **Tạo embedding**: Sử dụng API (như OpenAI) để tạo embedding.
- **Tính độ tương đồng**: So sánh CV và JD bằng cosine similarity.
- **Phân tích với LLM**: Gửi CV/JD vào LLM để phân tích và gợi ý cải thiện.
- **Hiển thị kết quả**: Render Match Score, điểm mạnh, điểm yếu qua HTML.

### Chức năng tùy chọn
- 💾 **Lưu lịch sử**: Lưu kết quả phân tích để xem lại.
- 🕒 **Xem lịch sử**: Hiển thị các đánh giá trước đó.
- 🗂️ **Quản lý CV**: Quản lý hoặc xóa file CV đã tải.
- 📈 **Thống kê admin**: Hiển thị số liệu về người dùng và lượt đánh giá.
- 🔒 **Xác thực người dùng**: (Dự kiến) Hỗ trợ đăng nhập để quản lý lịch sử.

---

## Cấu trúc dự án
```
JobFIT/
├── backend/                    # Backend Flask
    │   main.py
    ├───api
    │   │   chatgpt.py
    │   │   gemini.py
    │   │   other.py
    ├───config
    │   │   database.py
    │   │   __init__.py
    ├───logs
    │       app_log.py
    ├───models
    │   │   cv_model.py
    │   │   jd_model.py
    │   │   result_model.py
    │   │   __init__.py
    ├───plugins
    │       __init__.py
    ├───routers
    │   │   app_routers.py
    │   │   __init__.py
    ├───services
    │   │   load_cv.py
    │   │   load_jd.py
    │   │   review_cv.py
    │   │   __init__.py
    ├───static
    │   ├───css
    │   │       style.css
    │   │
    │   ├───images
    │   │       logo.png
    │   │
    │   └───js
    │           main.js
    │
    ├───templates
    │       auth.html
    │       home.html
    │       landing.html
    │
    └───utils
        │   convert.py
        │   embedding.py
        │   similarity.py
        │   suggestion.py
        │   __init__.py
```

---

## Yêu cầu kỹ thuật
- **Backend**:
  - Python 3.8+
  - Flask 2.3.3
  - Thư viện: `PyPDF2`, `python-docx`, `openai`, `numpy`, `scikit-learn`, `pymongo`, `python-dotenv`
- **Frontend**:
  - HTML/CSS/JavaScript
  - Jinja2 (cho templating trong Flask)
- **Cơ sở dữ liệu** (tùy chọn):
  - MongoDB hoặc PostgreSQL (cho lịch sử đánh giá)
- **Công cụ**:
  - Docker (khuyến nghị)
  - Git
  - API key từ OpenAI (hoặc LLM tương tự)

---

## Hướng dẫn cài đặt và chạy dự án

### 1. Clone repository
```bash
git clone https://github.com/username/JobFIT.git
cd JobFIT
```

### 2. Cài đặt môi trường
- **Tạo virtual environment**:
  ```bash
  python -m venv venv
  .\venv\Scripts\activate  # Windows
  ```
- **Cài đặt dependencies**:
  ```bash
  pip install -r requirements.txt
  ```

### 3. Cấu hình
  ```
- Cập nhật `.env` với các giá trị:
  ```env
  OPENAI_API_KEY=your_openai_key
  DATABASE_URL=mongodb://localhost:27017/jobfit_db  # Hoặc PostgreSQL
  FLASK_ENV=development
  SECRET_KEY=your_flask_secret_key
  ```

### 4. Chạy ứng dụng
```bash
python backend/main.py
```
- Truy cập: `http://localhost:5000`

---

## API Endpoints
- `GET /`: Trang chủ JobFIT.
- `POST /cv/upload`: Tải lên file CV.
- `POST /jd/upload`: Tải lên hoặc nhập JD.
- `GET /analyze`: Phân tích CV-JD, trả Match Score và gợi ý.
- `GET /history`: Xem lịch sử đánh giá (yêu cầu xác thực).
- `DELETE /cv/<id>`: Xóa file CV.

Chi tiết API: Xem `docs/api.md`.

---

## Hướng dẫn đóng góp
Chúng tôi hoan nghênh mọi đóng góp để cải thiện JobFIT! Để tham gia:

1. **Fork repository** và clone về máy:
   ```bash
   git clone https://github.com/your-username/JobFIT.git
   ```

2. **Tạo branch mới**:
   ```bash
   git checkout -b feature/your-feature-name
   ```

3. **Thêm code**:
   - **Backend**: Thêm logic vào `services/` hoặc routes vào `api/`.
   - **Frontend**: Cập nhật HTML trong `templates/` hoặc CSS/JS trong `static/`.
   - **Test**: Viết unit test trong `tests/`.

4. **Commit và push**:
   ```bash
   git add .
   git commit -m "Add your feature description"
   git push origin feature/your-feature-name
   ```

5. **Tạo Pull Request**:
   - Mô tả rõ ràng thay đổi và mục đích.
   - Liên kết với issue (nếu có).

6. **Quy tắc code**:
   - Tuân thủ PEP 8 cho Python.
   - Sử dụng Jinja2 đúng cách trong HTML templates.
   - Viết code modular, dễ đọc.
   - Thêm comment cho logic phức tạp.
   - Đảm bảo test pass: `pytest backend/tests`.

---

## Xử lý lỗi
- **Lỗi upload file**: Kiểm tra định dạng file trong `utils/file_utils.py`.
- **Lỗi LLM**: Xác minh API key và kết nối trong `services/llm_service.py`.
- **Lỗi database**: Kiểm tra cấu hình trong `config/database.py`.
- Log được lưu trong `utils/logger.py` để debug.
