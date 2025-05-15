import json
import numpy as np
from typing import Dict, List
from backend.models.cv_model import CV
from backend.models.jd_model import JD
from backend.utils.embedding import embedded_vector
from backend.utils.suggestion import get_suggestion
from backend.utils.similarity import calculate_similarity
from backend.models.result_model import ResultModel, _Overview, _DetailedAnalysis, _Recommendations

class ReviewCV:
    def __init__(self, cv: CV, jd: JD):
        """
        Khởi tạo đối tượng ReviewCV

        Args:
            cv: Đối tượng CV
            jd: Đối tượng JD
        """
        self.cv = cv
        self.jd = jd
        self.result = self._analyze_cv()

    def _embed_cv_sections(self) -> Dict[str, np.ndarray]:
        """
        Tạo embedding cho các phần của CV

        Returns:
            Dict[str, np.ndarray]: Dictionary chứa embedding của các phần CV
        """
        embeddings = {}

        # Tạo embedding cho thông tin cá nhân
        if self.cv.personal_info and self.cv.personal_info.career_objective:
            embeddings['career_objective'] = embedded_vector(self.cv.personal_info.career_objective)

        # Tạo embedding cho học vấn
        education_texts = []
        for edu in self.cv.education:
            text_parts = []
            if edu.university:
                text_parts.append(f"University: {edu.university}")
            if edu.major:
                text_parts.append(f"Major: {edu.major}")
            if edu.degree:
                text_parts.append(f"Degree: {edu.degree}")
            if text_parts:
                education_texts.append(" ".join(text_parts))
        if education_texts:
            embeddings['education'] = embedded_vector(" ".join(education_texts))

        # Tạo embedding cho kỹ năng
        if self.cv.skills:
            embeddings['skills'] = embedded_vector(" ".join(self.cv.skills))

        # Tạo embedding cho kinh nghiệm làm việc
        work_exp_texts = []
        for exp in self.cv.work_experience:
            text_parts = []
            if exp.position:
                text_parts.append(f"Position: {exp.position}")
            if exp.description:
                text_parts.append(f"Description: {exp.description}")
            if text_parts:
                work_exp_texts.append(" ".join(text_parts))
        if work_exp_texts:
            embeddings['work_experience'] = embedded_vector(" ".join(work_exp_texts))

        # Tạo embedding cho dự án cá nhân
        project_texts = []
        for project in self.cv.personal_projects:
            text_parts = []
            if project.name:
                text_parts.append(f"Project: {project.name}")
            if project.description:
                text_parts.append(f"Description: {project.description}")
            if project.technologies:
                text_parts.append(f"Technologies: {', '.join(project.technologies)}")
            if text_parts:
                project_texts.append(" ".join(text_parts))
        if project_texts:
            embeddings['personal_projects'] = embedded_vector(" ".join(project_texts))

        return embeddings

    def _embed_jd_sections(self) -> Dict[str, np.ndarray]:
        """
        Tạo embedding cho các phần của JD

        Returns:
            Dict[str, np.ndarray]: Dictionary chứa embedding của các phần JD
        """
        embeddings = {}

        # Tạo embedding cho mô tả công việc
        if self.jd.job_description and self.jd.job_description.description:
            embeddings['job_description'] = embedded_vector(self.jd.job_description.description)

        # Tạo embedding cho các yêu cầu công việc
        requirement_texts = []
        if self.jd.job_requirement:
            if self.jd.job_requirement.knowledge:
                requirement_texts.append(f"Knowledge: {self.jd.job_requirement.knowledge}")
            if self.jd.job_requirement.skills:
                requirement_texts.append(f"Skills: {', '.join(self.jd.job_requirement.skills)}")
            if self.jd.job_requirement.experience:
                requirement_texts.append(f"Experience: {self.jd.job_requirement.experience}")
            if self.jd.job_requirement.other_requirements:
                requirement_texts.append(f"Other Requirements: {self.jd.job_requirement.other_requirements}")
        if requirement_texts:
            embeddings['job_requirement'] = embedded_vector(" ".join(requirement_texts))

        return embeddings

    def _calculate_section_similarities(self) -> Dict[str, float]:
        """
        Tính toán mức độ tương đồng giữa các phần của CV và JD

        Returns:
            Dict[str, float]: Dictionary chứa điểm tương đồng của mỗi phần
        """
        similarities = {}
        cv_embeddings = self._embed_cv_sections()
        jd_embeddings = self._embed_jd_sections()

        # Tính toán tương đồng giữa mục tiêu nghề nghiệp và mô tả công việc
        if 'career_objective' in cv_embeddings and 'job_description' in jd_embeddings:
            similarities['career_objective'] = calculate_similarity(
                [cv_embeddings['career_objective']], [jd_embeddings['job_description']]
            )

        # Tính toán tương đồng giữa kỹ năng trong CV và yêu cầu công việc
        if 'skills' in cv_embeddings and 'job_requirement' in jd_embeddings:
            similarities['skills'] = calculate_similarity(
                [cv_embeddings['skills']], [jd_embeddings['job_requirement']]
            )

        # Tính toán tương đồng giữa kinh nghiệm làm việc và yêu cầu công việc
        if 'work_experience' in cv_embeddings and 'job_requirement' in jd_embeddings:
            similarities['work_experience'] = calculate_similarity(
                [cv_embeddings['work_experience']], [jd_embeddings['job_requirement']]
            )

        # Tính toán tương đồng tổng thể
        if cv_embeddings and jd_embeddings:
            cv_combined = np.mean([emb for emb in cv_embeddings.values()], axis=0)
            jd_combined = np.mean([emb for emb in jd_embeddings.values()], axis=0)
            similarities['overall'] = calculate_similarity([cv_combined], [jd_combined])

        return similarities

    def _analyze_cv(self) -> ResultModel:
        """
        Phân tích CV và so sánh với JD để tạo kết quả đánh giá

        Returns:
            ResultModel: Đối tượng chứa kết quả phân tích
        """
        try:
            similarities = self._calculate_section_similarities()

            # Chuyển đổi CV và JD thành chuỗi JSON để gửi đến Gemini
            cv_json = self.cv.model_dump(exclude_none=True)
            jd_json = self.jd.model_dump(exclude_none=True)

            analysis_json_str = get_suggestion(cv_json, jd_json, model='Gemini')

            # Xử lý nếu phản hồi được bọc trong markdown code block
            if analysis_json_str and analysis_json_str.strip().startswith("```"):
                start = analysis_json_str.find("{")
                end = analysis_json_str.rfind("}") + 1
                if start > -1 and end > 0:
                    analysis_json_str = analysis_json_str[start:end]

            try:
                analysis_data = json.loads(analysis_json_str)

                # Tạo đối tượng ResultModel từ dữ liệu phân tích
                result = ResultModel(**analysis_data)

                # Cập nhật điểm tương đồng từ embedding similarity
                if result.overview:
                    result.overview.match_score = similarities.get('overall', 0)

                return result
            except json.JSONDecodeError as e:
                print(f"Lỗi khi phân tích JSON từ phản hồi: {e}")
                # Trả về đối tượng ResultModel mặc định
                return self._create_default_result()

        except Exception as e:
            print(f"Lỗi khi phân tích CV: {e}")
            return self._create_default_result()

    def _create_default_result(self) -> ResultModel:
        """
        Tạo một đối tượng ResultModel mặc định khi có lỗi

        Returns:
            ResultModel: Đối tượng kết quả mặc định
        """
        return ResultModel(
            overview=_Overview(
                description="Không thể phân tích chi tiết CV và JD",
                strengths=[],
                weaknesses=[],
                match_score=0.0
            ),
            detailed_analysis=_DetailedAnalysis(),
            recommendations=_Recommendations(
                suggestions=["Vui lòng thử lại sau"],
                resources=[]
            )
        )

    def get_result(self) -> ResultModel:
        """
        Lấy kết quả phân tích

        Returns:
            ResultModel: Đối tượng chứa kết quả phân tích
        """
        return self.result

    def get_overview(self):
        """
        Lấy tổng quan về kết quả phân tích

        Returns:
            _Overview: Đối tượng chứa tổng quan về kết quả phân tích
        """
        if self.result and self.result.overview:
            return self.result.overview
        return None

    def get_detailed_analysis(self):
        """
        Lấy phân tích chi tiết về từng phần của CV

        Returns:
            _DetailedAnalysis: Đối tượng chứa phân tích chi tiết
        """
        if self.result and self.result.detailed_analysis:
            return self.result.detailed_analysis
        return None

    def get_recommendations(self):
        """
        Lấy đề xuất cải thiện cho CV

        Returns:
            _Recommendations: Đối tượng chứa đề xuất cải thiện
        """
        if self.result and self.result.recommendations:
            return self.result.recommendations
        return None

    def get_match_score(self) -> float:
        """
        Lấy điểm số phù hợp với vị trí ứng tuyển

        Returns:
            float: Điểm số phù hợp (0-100)
        """
        if self.result and self.result.overview and self.result.overview.match_score is not None:
            return self.result.overview.match_score
        return 0.0

    def get_improvement_suggestions(self) -> List[str]:
        """
        Lấy gợi ý cải thiện CV sử dụng module suggestion

        Returns:
            List[str]: Danh sách các gợi ý cải thiện
        """
        # Chuyển đổi CV và JD thành dạng văn bản
        cv_str = json.dumps(self.cv.model_dump(exclude_none=True), ensure_ascii=False)
        jd_str = json.dumps(self.jd.model_dump(exclude_none=True), ensure_ascii=False)

        # Gọi API từ module suggestion để lấy gợi ý
        suggestion_text = get_suggestion(cv_str, jd_str, model='Gemini')

        # Xử lý phản hồi và tách thành danh sách gợi ý
        suggestions = []
        if suggestion_text:
            # Tìm kiếm các dòng bắt đầu bằng số hoặc dấu - để tách thành các gợi ý riêng biệt
            lines = suggestion_text.split('\n')
            current_suggestion = ""

            for line in lines:
                stripped_line = line.strip()
                # Bắt đầu một gợi ý mới
                if (stripped_line and
                        (stripped_line[0].isdigit() and '.' in stripped_line[:3]) or
                        stripped_line.startswith('-') or
                        stripped_line.startswith('*')):
                    if current_suggestion:
                        suggestions.append(current_suggestion.strip())
                    current_suggestion = stripped_line
                # Tiếp tục gợi ý hiện tại
                elif current_suggestion:
                    current_suggestion += " " + stripped_line

            # Thêm gợi ý cuối cùng
            if current_suggestion:
                suggestions.append(current_suggestion.strip())

            # Nếu không tìm thấy định dạng gợi ý, lấy toàn bộ nội dung
            if not suggestions:
                suggestions = [suggestion_text]

        return suggestions

    def to_dict(self) -> dict:
        """
        Chuyển đổi kết quả phân tích thành dictionary

        Returns:
            dict: Dictionary chứa kết quả phân tích
        """
        if self.result:
            return self.result.model_dump(exclude_none=True)
        return {}
# Đã kiểm thử