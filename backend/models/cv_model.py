# File này được sử dụng để tạo / ánh xạ các mô hình dữ liệu cho CV (Curriculum Vitae) của người dùng.

from datetime import date
from typing import List, Optional
from pydantic import BaseModel, EmailStr, Field

class _PersonalInfo(BaseModel):
    """
    Thông tin cá nhân của người dùng.
    Tất cả các trường là không bắt buộc vì người dùng có thể không muốn cung cấp tất cả thông tin.
    Khi đó service sẽ tự động đề xuất người dùng cung cấp thông tin này để hoàn thiện CV.
    """
    name: Optional[str] = Field(..., description="Họ và tên")
    gender: Optional[str] = Field(..., description="Giới tính")
    email: Optional[EmailStr] = Field(..., description="Email")
    address: Optional[str] = Field(None, description="Địa chỉ")
    phone: Optional[str] = Field(None, description="Số điện thoại")
    dob: Optional[date] = Field(None, description="Ngày tháng năm sinh")
    career_objective: Optional[str] = Field(None, description="Mục tiêu nghề nghiệp")

class _Education(BaseModel):
    """
    Thông tin học vấn của người dùng.
    Tất cả các trường là không bắt buộc vì người dùng có thể không muốn cung cấp tất cả thông tin.
    Nếu JD yêu cầu thông tin này, service sẽ tự động đề xuất người dùng cung cấp thông tin này để hoàn thiện CV.
    Nếu JD không yêu cầu thông tin này, nó sẽ được bỏ qua.
    """
    university: Optional[str] = Field(..., description="Tên trường đại học")
    major: Optional[str] = Field(..., description="Chuyên ngành")
    gpa: Optional[float] = Field(None, description="Điểm trung bình (GPA)")
    degree: Optional[str] = Field(None, description="Bằng cấp (ví dụ: Cử nhân, Thạc sĩ)")

class _Certification(BaseModel):
    """
    Thông tin chứng chỉ của người dùng.
    Khi người dùng đã đề cập đến chứng chỉ thì phải đầy đủ thông tin về chứng chỉ.
    """
    name: str = Field(..., description="Tên chứng chỉ")
    issuing_organization: str = Field(..., description="Tổ chức cấp chứng chỉ")
    certificate_link: Optional[str] = Field(None, description="Liên kết đến chứng chỉ")


class _Skill(BaseModel):
    """
    Thông tin kỹ năng của người dùng.
    """
    name: str = Field(..., description="Tên kỹ năng")

class _WorkExperience(BaseModel):
    """
    Thông tin kinh nghiệm làm việc, người dùng cần cung cấp ít nhất thông tin về công ty, vị trí làm việc còn lại có thể bỏ qua.
    """
    company: str = Field(..., description="Công ty")
    position: str = Field(..., description="Vị trí")
    time: Optional[str] = Field(..., description="Thời gian (ví dụ: 2020-2023)")
    description: Optional[str] = Field(None, description="Mô tả công việc")

class _PersonalProject(BaseModel):
    """
    Thông tin dự án cá nhân của người dùng.
    """
    name: str = Field(..., description="Tên dự án")
    description: Optional[str] = Field(None, description="Mô tả dự án")
    members: Optional[List[int]] = Field(default_factory=list, description="Sô lượng thành viên tham gia dự án")
    technologies: List[str] = Field(default_factory=list, description="Công nghệ sử dụng trong dự án")
    github_link: Optional[str] = Field(None, description="Liên kết đến GitHub hoặc trang dự án")

class CV(BaseModel):
    """
    Mô hình dữ liệu cho CV (Curriculum Vitae) của người dùng.
    """
    personal_info: _PersonalInfo = Field(..., description="Thông tin cá nhân")
    career_objective: Optional[str] = Field(None, description="Mục tiêu nghề nghiệp")
    education: Optional[List[_Education]] = Field(default_factory=list, description="Học vấn")
    certifications: Optional[List[_Certification]] = Field(default_factory=list, description="Chứng chỉ")
    skills: List[str] = Field(default_factory=list, description="Kỹ năng")
    work_experience: List[_WorkExperience] = Field(default_factory=list, description="Kinh nghiệm làm việc")