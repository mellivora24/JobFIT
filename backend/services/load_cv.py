import json
from typing import Optional
from models.cv_model import CV
import api.gemini as gemini_services
from utils.convert import extract_text_from_file

class CreateCV:
    def __init__(self, cv_file):
        """
        Khởi tạo đối tượng CreateCV

        Args:
            cv_file: File CV được tải lên (có thể là docx, pdf, hoặc hình ảnh)
        """
        self.cv_file = cv_file
        self.cv = self._create_cv_from_file()

    def _load_from_file(self) -> str:
        """
        Trích xuất nội dung từ file CV và gọi API Gemini để phân tích

        Returns:
            str: Chuỗi JSON chứa thông tin CV
        """
        try:
            text_from_file = extract_text_from_file(self.cv_file)
            print(f"Đã trích xuất văn bản từ file, độ dài: {len(text_from_file)} ký tự")

            prompt = f"""
                Từ văn bản đã trích xuất từ tệp CV, hãy tạo một file JSON đại diện cho CV của người dùng, tuân thủ cấu trúc dữ liệu sau:
                {{
                  "personal_info": {{
                    "name": "Họ và tên (chuỗi, tùy chọn)",
                    "gender": "Giới tính (chuỗi, tùy chọn)",
                    "email": "Email hợp lệ (chuỗi, tùy chọn)",
                    "address": "Địa chỉ (chuỗi, tùy chọn)",
                    "phone": "Số điện thoại (chuỗi, tùy chọn)",
                    "dob": "Ngày tháng năm sinh, định dạng YYYY-MM-DD (chuỗi, tùy chọn)",
                    "career_objective": "Mục tiêu nghề nghiệp (chuỗi, tùy chọn)"
                  }},
                  "education": [
                    {{
                      "university": "Tên trường đại học (chuỗi, tùy chọn)",
                      "major": "Chuyên ngành (chuỗi, tùy chọn)",
                      "gpa": "Điểm trung bình (số thực, tùy chọn)",
                      "degree": "Bằng cấp, ví dụ: Cử nhân, Thạc sĩ (chuỗi, tùy chọn)"
                    }}
                  ],
                  "certifications": [
                    {{
                      "name": "Tên chứng chỉ (chuỗi, bắt buộc nếu có chứng chỉ)",
                      "issuing_organization": "Tổ chức cấp chứng chỉ (chuỗi, bắt buộc nếu có chứng chỉ)",
                      "certificate_link": "Liên kết đến chứng chỉ (chuỗi, tùy chọn)"
                    }}
                  ],
                  "personal_projects": [
                    {{
                      "name": "Tên dự án (chuỗi, tùy chọn)",
                      "description": "Mô tả dự án (chuỗi, tùy chọn)",
                      "members": "Số lượng thành viên tham gia dự án (số nguyên, tùy chọn)",
                      "technologies": "Công nghệ sử dụng trong dự án (danh sách chuỗi, tùy chọn)",
                      "github_link": "Liên kết đến GitHub hoặc trang dự án (chuỗi, tùy chọn)"
                    }}
                  ],
                  "skills": ["Kỹ năng (chuỗi, danh sách các kỹ năng, tùy chọn)"],
                  "work_experience": [
                    {{
                      "company": "Tên công ty (chuỗi, tùy chọn)",
                      "position": "Vị trí công việc (chuỗi, tùy chọn)",
                      "time": "Thời gian làm việc, ví dụ: 2020-2023 (chuỗi, tùy chọn)",
                      "description": "Mô tả công việc (chuỗi, tùy chọn)"
                    }}
                  ]
                }}
                Đây là văn bản đã trích xuất từ tệp CV:
                {text_from_file}

                Lưu ý:
                1. Chỉ trả về chuỗi JSON, không có văn bản giải thích thêm.
                2. Hãy đảm bảo JSON được trả về đúng định dạng và đúng cấu trúc như mẫu trên.
                3. Nếu thiếu thông tin nào đó không có trong văn bản, hãy ghi là không có thông tin (với gpa, members, time thì ghi là None).
                4. Không bọc JSON trong dấu backtick hoặc markdown code block.
            """

            response = gemini_services.call_gemini_api(message=prompt)

            # Xử lý nếu phản hồi được bọc trong markdown code block
            if response and response.strip().startswith("```"):
                # Loại bỏ markdown code block nếu có
                if "```json" in response or "```" in response:
                    # Tìm vị trí bắt đầu và kết thúc của JSON
                    start = response.find("{")
                    end = response.rfind("}") + 1
                    if start > -1 and end > 0:
                        response = response[start:end]

            return response
        except Exception as e:
            print(f"Lỗi khi trích xuất văn bản từ file: {e}")
            return "{}"  # Trả về một JSON rỗng nếu có lỗi

    def _create_cv_from_file(self) -> Optional[CV]:
        """
        Tạo đối tượng CV từ chuỗi JSON

        Returns:
            CV: Đối tượng CV theo model định nghĩa, hoặc None nếu có lỗi
        """
        try:
            cv_json_str = self._load_from_file()

            # Kiểm tra chuỗi JSON trước khi phân tích
            if not cv_json_str or cv_json_str.strip() == "":
                print("Chuỗi JSON trả về rỗng")
                return self._create_empty_cv()

            try:
                cv_data = json.loads(cv_json_str)
            except json.JSONDecodeError as e:
                print(f"Lỗi khi phân tích JSON: {e}")
                # Tạo một CV rỗng trong trường hợp này
                return self._create_empty_cv()

            # Đảm bảo các trường cần thiết tồn tại trong dữ liệu
            if "personal_info" not in cv_data:
                cv_data["personal_info"] = {}
            if "education" not in cv_data:
                cv_data["education"] = []
            if "certifications" not in cv_data:
                cv_data["certifications"] = []
            if "personal_projects" not in cv_data:
                cv_data["personal_projects"] = []
            if "skills" not in cv_data:
                cv_data["skills"] = []
            if "work_experience" not in cv_data:
                cv_data["work_experience"] = []

            return CV(**cv_data)
        except Exception as e:
            print(f"Lỗi khi tạo CV từ file: {e}")
            return self._create_empty_cv()

    def _create_empty_cv(self) -> CV:
        """
        Tạo một đối tượng CV rỗng

        Returns:
            CV: Đối tượng CV rỗng
        """
        return CV(
            personal_info=None,
            education=[],
            certifications=[],
            personal_projects=[],
            skills=[],
            work_experience=[]
        )

    def get_cv(self) -> CV:
        """
        Lấy đối tượng CV đã được tạo

        Returns:
            CV: Đối tượng CV theo model định nghĩa
        """
        if self.cv is None:
            return self._create_empty_cv()
        return self.cv

    def get_personal_info(self):
        """Trả về thông tin cá nhân từ CV"""
        if self.cv and self.cv.personal_info:
            return self.cv.personal_info
        return None

    def get_education(self):
        """Trả về danh sách thông tin học vấn từ CV"""
        if self.cv and self.cv.education:
            return self.cv.education
        return []

    def get_certifications(self):
        """Trả về danh sách chứng chỉ từ CV"""
        if self.cv and self.cv.certifications:
            return self.cv.certifications
        return []

    def get_skills(self):
        """Trả về danh sách kỹ năng từ CV"""
        if self.cv and self.cv.skills:
            return self.cv.skills
        return []

    def get_work_experience(self):
        """Trả về danh sách kinh nghiệm làm việc từ CV"""
        if self.cv and self.cv.work_experience:
            return self.cv.work_experience
        return []

    def get_career_objective(self):
        """Trả về mục tiêu nghề nghiệp từ CV"""
        if self.cv and self.cv.personal_info and self.cv.personal_info.career_objective:
            return self.cv.personal_info.career_objective
        return None

    def to_dict(self):
        """
        Chuyển đổi đối tượng CV thành dictionary để dễ dàng xử lý

        Returns:
            dict: Dictionary chứa thông tin CV
        """
        if self.cv:
            # Sử dụng model_dump thay vì dict do Pydantic v2 đã không còn hỗ trợ dict
            return self.cv.model_dump(exclude_none=True)
        return {}

# Đã kiểm thử