import json
from typing import Optional
from backend.models.jd_model import JD
import backend.api.gemini as gemini_services


class CreateJD:
    def __init__(self, jd_text: str):
        """
        Khởi tạo đối tượng CreateJD

        Args:
            jd_text: Văn bản JD được nhập vào dưới dạng chuỗi
        """
        self.jd_text = jd_text
        self.jd = self._create_jd_from_text()

    def _load_from_text(self) -> str:
        """
        Gửi văn bản JD đến API Gemini để phân tích và trích xuất dữ liệu dạng JSON

        Returns:
            str: Chuỗi JSON chứa thông tin JD
        """
        try:
            prompt = f"""
                Từ văn bản mô tả công việc sau, hãy tạo một JSON đại diện cho JD theo cấu trúc sau:
                {{
                  "job_description": {{
                    "title": "Tiêu đề công việc",
                    "description": "Mô tả công việc"
                  }},
                  "job_requirement": {{
                    "knowledge": "Kiến thức yêu cầu (có thể để trống)",
                    "skills": ["Danh sách kỹ năng yêu cầu"],
                    "experience": "Kinh nghiệm yêu cầu (có thể để trống)",
                    "other_requirements": "Yêu cầu khác (có thể để trống)"
                  }}
                }}

                Văn bản JD:
                {self.jd_text}

                Lưu ý:
                1. Chỉ trả về chuỗi JSON, không có văn bản giải thích thêm.
                2. Hãy đảm bảo JSON được trả về đúng định dạng và đúng cấu trúc như mẫu trên.
                3. Nếu thiếu thông tin nào đó không có trong văn bản, hãy để trường đó là null hoặc bỏ qua nó.
                4. Không bọc JSON trong dấu backtick hoặc markdown code block.
            """

            response = gemini_services.call_gemini_api(prompt)

            # Loại bỏ markdown nếu có
            if response and response.strip().startswith("```"):
                start = response.find("{")
                end = response.rfind("}") + 1
                if start > -1 and end > 0:
                    response = response[start:end]

            return response
        except Exception as e:
            print(f"Lỗi khi gọi API Gemini: {e}")
            return "{}"

    def _create_jd_from_text(self) -> Optional[JD]:
        """
        Tạo đối tượng JD từ chuỗi JSON

        Returns:
            JD: Đối tượng JD hoặc None nếu có lỗi
        """
        try:
            jd_json_str = self._load_from_text()

            if not jd_json_str or jd_json_str.strip() == "":
                print("Chuỗi JSON JD rỗng")
                return None

            jd_data = json.loads(jd_json_str)

            return JD(**jd_data)
        except Exception as e:
            print(f"Lỗi khi phân tích hoặc tạo JD: {e}")
            return None

    def get_job_description(self):
        """Trả về phần mô tả công việc"""
        if self.jd and self.jd.job_description:
            return self.jd.job_description
        return None

    def get_job_requirement(self):
        """Trả về phần yêu cầu công việc"""
        if self.jd and self.jd.job_requirement:
            return self.jd.job_requirement
        return None

    def to_dict(self):
        """Chuyển JD thành dictionary"""
        if self.jd:
            return self.jd.model_dump(exclude_none=True)
        return {}

# Đã kiểm thử
