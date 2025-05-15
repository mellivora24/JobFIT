from typing import List, Optional
from pydantic import BaseModel, Field

class _Overview(BaseModel):
    """
    Thông tin tổng quan về kết quả phân tích.
    """
    description: Optional[str] = Field(None, description="Mô tả tổng quan về kết quả phân tích")
    strengths: Optional[List[str]] = Field(default_factory=list, description="Điểm mạnh của CV")
    weaknesses: Optional[List[str]] = Field(default_factory=list, description="Điểm yếu của CV")
    match_score: Optional[float] = Field(None, description="Điểm số phù hợp với vị trí ứng tuyển")

class _DetailedAnalysis(BaseModel):
    """
    Phân tích chi tiết về từng phần của CV.
    """
    personal_info: Optional[str] = Field(None, description="Phân tích thông tin cá nhân")
    education: Optional[str] = Field(None, description="Phân tích thông tin học vấn")
    certifications: Optional[str] = Field(None, description="Phân tích thông tin chứng chỉ")
    skills: Optional[str] = Field(None, description="Phân tích thông tin kỹ năng")
    work_experience: Optional[str] = Field(None, description="Phân tích thông tin kinh nghiệm làm việc")
    personal_projects: Optional[str] = Field(None, description="Phân tích thông tin dự án cá nhân")

class _Recommendations(BaseModel):
    """
    Đề xuất cải thiện cho CV.
    """
    suggestions: Optional[List[str]] = Field(default_factory=list, description="Đề xuất cải thiện cho CV")
    resources: Optional[List[str]] = Field(default_factory=list, description="Tài nguyên tham khảo để cải thiện CV")

class ResultModel(BaseModel):
    """
    Mô hình dữ liệu cho kết quả phân tích CV.
    """
    overview: Optional[_Overview] = Field(None, description="Thông tin tổng quan về kết quả phân tích")
    detailed_analysis: Optional[_DetailedAnalysis] = Field(None, description="Phân tích chi tiết về từng phần của CV")
    recommendations: Optional[_Recommendations] = Field(None, description="Đề xuất cải thiện cho CV")
