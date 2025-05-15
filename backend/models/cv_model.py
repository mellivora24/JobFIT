# File này được sử dụng để tạo / ánh xạ các mô hình dữ liệu cho CV (Curriculum Vitae) của người dùng.

from typing import List, Optional
from pydantic import BaseModel, EmailStr, Field

class _PersonalInfo(BaseModel):
    """
    Thông tin cá nhân của người dùng.
    """
    name: Optional[str] = Field(None, description="Họ và tên")
    gender: Optional[str] = Field(None, description="Giới tính")
    email: Optional[EmailStr] = Field(None, description="Email")
    address: Optional[str] = Field(None, description="Địa chỉ")
    phone: Optional[str] = Field(None, description="Số điện thoại")
    dob: Optional[str] = Field(None, description="Ngày tháng năm sinh")
    career_objective: Optional[str] = Field(None, description="Mục tiêu nghề nghiệp")

class _Education(BaseModel):
    """
    Thông tin học vấn của người dùng.
    """
    university: Optional[str] = Field(None, description="Tên trường đại học")
    major: Optional[str] = Field(None, description="Chuyên ngành")
    gpa: Optional[float] = Field(None, description="Điểm trung bình (GPA)")
    degree: Optional[str] = Field(None, description="Bằng cấp (ví dụ: Cử nhân, Thạc sĩ)")

class _Certification(BaseModel):
    """
    Thông tin chứng chỉ của người dùng.
    Khi người dùng đã đề cập đến chứng chỉ thì phải đầy đủ thông tin về chứng chỉ.
    """
    name: Optional[str] = Field(None, description="Tên chứng chỉ")
    issuing_organization: Optional[str] = Field(None, description="Tổ chức cấp chứng chỉ")
    certificate_link: Optional[str] = Field(None, description="Liên kết đến chứng chỉ")

class _Skill(BaseModel):
    """
    Thông tin kỹ năng của người dùng.
    """
    name: Optional[str] = Field(None, description="Tên kỹ năng")

class _WorkExperience(BaseModel):
    """
    Thông tin kinh nghiệm làm việc.
    """
    company: Optional[str] = Field(None, description="Công ty")
    position: Optional[str] = Field(None, description="Vị trí")
    time: Optional[str] = Field(None, description="Thời gian làm việc")
    description: Optional[str] = Field(None, description="Mô tả công việc")

class _PersonalProject(BaseModel):
    """
    Thông tin dự án cá nhân của người dùng.
    """
    name: Optional[str] = Field(None, description="Tên dự án")
    description: Optional[str] = Field(None, description="Mô tả dự án")
    members: Optional[int] = Field(None, description="Sô lượng thành viên tham gia dự án")
    technologies: Optional[List[str]]= Field(default_factory=list, description="Công nghệ sử dụng trong dự án")
    github_link: Optional[str] = Field(None, description="Liên kết đến GitHub hoặc trang dự án")

class CV(BaseModel):
    """
    Mô hình dữ liệu cho CV (Curriculum Vitae) của người dùng.
    """
    personal_info: Optional[_PersonalInfo] = Field(None, description="Thông tin cá nhân")
    education: Optional[List[_Education]] = Field(default_factory=list, description="Học vấn")
    certifications: Optional[List[_Certification]] = Field(default_factory=list, description="Chứng chỉ")
    personal_projects: Optional[List[_PersonalProject]] = Field(default_factory=list, description="Dự án cá nhân")
    skills: Optional[List[str]] = Field(default_factory=list, description="Kỹ năng")
    work_experience: Optional[List[_WorkExperience]]= Field(default_factory=list, description="Kinh nghiệm làm việc")
