import json
from api import chatgpt, gemini


def get_suggestion(cv_json, jd_json, model='ChatGPT'):
    if model == 'ChatGPT':
        return _chatgpt_suggestion(cv_json, jd_json)
    elif model == 'Gemini':
        return _gemini_suggestion(cv_json, jd_json)


def _chatgpt_suggestion(cv_json, jd_json):
    message = \
        f"""
            Hãy phân tích CV và JD dưới đây, và cung cấp một đánh giá chi tiết về mức độ phù hợp của CV với vị trí công việc.
            Đánh giá này cần bao gồm:
            
            1. Tổng quan (Overview):
               - Mô tả tổng quan về độ phù hợp giữa CV và JD
               - Liệt kê các điểm mạnh của CV đối với vị trí này
               - Liệt kê các điểm yếu của CV đối với vị trí này
            
            2. Phân tích chi tiết (Detailed Analysis) cho từng phần:
               - Thông tin cá nhân và mục tiêu nghề nghiệp: Mục tiêu nghề nghiệp có phù hợp với vị trí không?
               - Học vấn: Trình độ học vấn có đáp ứng yêu cầu không?
               - Chứng chỉ: Các chứng chỉ có liên quan đến công việc không?
               - Kỹ năng: Kỹ năng của ứng viên có đáp ứng yêu cầu công việc không?
               - Kinh nghiệm làm việc: Kinh nghiệm có phù hợp với yêu cầu không?
               - Dự án cá nhân: Các dự án có thể hiện năng lực phù hợp với vị trí không?
            
            3. Đề xuất (Recommendations):
               - Những gợi ý cụ thể để cải thiện CV cho phù hợp hơn với vị trí
               - Các tài nguyên hoặc khóa học có thể giúp ứng viên bổ sung kỹ năng còn thiếu
            
            CV (JSON): {cv_json}
            JD (JSON): {jd_json}
            
            Trả về phân tích của bạn dưới dạng JSON với cấu trúc sau:
            {{
                "overview": {{
                    "description": "Mô tả tổng quan về kết quả phân tích",
                    "strengths": ["Điểm mạnh 1", "Điểm mạnh 2", ...],
                    "weaknesses": ["Điểm yếu 1", "Điểm yếu 2", ...],
                    "match_score": số điểm từ 0-100 thể hiện mức độ phù hợp tổng thể (làm tròn đến hàng đơn vị)
                }},
                "detailed_analysis": {{
                    "personal_info": "Phân tích thông tin cá nhân và mục tiêu nghề nghiệp",
                    "education": "Phân tích thông tin học vấn",
                    "certifications": "Phân tích thông tin chứng chỉ",
                    "skills": "Phân tích thông tin kỹ năng",
                    "work_experience": "Phân tích thông tin kinh nghiệm làm việc",
                    "personal_projects": "Phân tích thông tin dự án cá nhân"
                }},
                "recommendations": {{
                    "suggestions": ["Gợi ý 1", "Gợi ý 2", ...],
                    "resources": ["Tài nguyên 1", "Tài nguyên 2", ...]
                }}
            }}
            
            Lưu ý:
            1. Chỉ trả về chuỗi JSON, không có văn bản giải thích thêm
            2. Đảm bảo đánh giá chi tiết, đầy đủ và có tính xây dựng
            3. Phân tích các ưu điểm, nhược điểm cụ thể của CV so với yêu cầu trong JD
            4. Đề xuất các cải tiến cụ thể cho CV
            """
    response = chatgpt.call_chatgpt_api(message)
    return response


def _gemini_suggestion(cv_json, jd_json):
    message =\
        f"""
            Hãy phân tích CV và JD dưới đây, và cung cấp một đánh giá chi tiết về mức độ phù hợp của CV với vị trí công việc.
            Đánh giá này cần bao gồm:
            
            1. Tổng quan (Overview):
               - Mô tả tổng quan về độ phù hợp giữa CV và JD
               - Liệt kê các điểm mạnh của CV đối với vị trí này
               - Liệt kê các điểm yếu của CV đối với vị trí này
            
            2. Phân tích chi tiết (Detailed Analysis) cho từng phần:
               - Thông tin cá nhân và mục tiêu nghề nghiệp: Mục tiêu nghề nghiệp có phù hợp với vị trí không?
               - Học vấn: Trình độ học vấn có đáp ứng yêu cầu không?
               - Chứng chỉ: Các chứng chỉ có liên quan đến công việc không?
               - Kỹ năng: Kỹ năng của ứng viên có đáp ứng yêu cầu công việc không?
               - Kinh nghiệm làm việc: Kinh nghiệm có phù hợp với yêu cầu không?
               - Dự án cá nhân: Các dự án có thể hiện năng lực phù hợp với vị trí không?
            
            3. Đề xuất (Recommendations):
               - Những gợi ý cụ thể để cải thiện CV cho phù hợp hơn với vị trí
               - Các tài nguyên hoặc khóa học có thể giúp ứng viên bổ sung kỹ năng còn thiếu
            
            CV (JSON): {cv_json}
            JD (JSON): {jd_json}
            
            Trả về phân tích của bạn dưới dạng JSON với cấu trúc sau:
            {{
                "overview": {{
                    "description": "Mô tả tổng quan về kết quả phân tích",
                    "strengths": ["Điểm mạnh 1", "Điểm mạnh 2", ...],
                    "weaknesses": ["Điểm yếu 1", "Điểm yếu 2", ...],
                    "match_score": số điểm từ 0-100 thể hiện mức độ phù hợp tổng thể (điểm làm tròn đến hàng đơn vị)
                }},
                "detailed_analysis": {{
                    "personal_info": "Phân tích thông tin cá nhân và mục tiêu nghề nghiệp",
                    "education": "Phân tích thông tin học vấn",
                    "certifications": "Phân tích thông tin chứng chỉ",
                    "skills": "Phân tích thông tin kỹ năng",
                    "work_experience": "Phân tích thông tin kinh nghiệm làm việc",
                    "personal_projects": "Phân tích thông tin dự án cá nhân"
                }},
                "recommendations": {{
                    "suggestions": ["Gợi ý 1", "Gợi ý 2", ...],
                    "resources": ["Tài nguyên 1", "Tài nguyên 2", ...]
                }}
            }}
            
            Lưu ý:
            1. Chỉ trả về chuỗi JSON, không có văn bản giải thích thêm
            2. Đảm bảo đánh giá chi tiết, đầy đủ và có tính xây dựng
            3. Phân tích các ưu điểm, nhược điểm cụ thể của CV so với yêu cầu trong JD
            4. Đề xuất các cải tiến cụ thể cho CV
            """
    response = gemini.call_gemini_api(message)
    return response
