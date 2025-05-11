# File này được sử dụng để tạo / ánh xạ các mô hình dữ liệu cho JD (Job Description) mà người dùng cung cấp.

from datetime import date
from typing import List, Optional
from pydantic import BaseModel, EmailStr, Field

class _JobDescription(BaseModel):
    """
    Mô tả công việc mà JD cung cấp.
    """
    title: str = Field(..., description="Tiêu đề công việc")
    description: str = Field(..., description="Mô tả công việc")

class _JobRequirement(BaseModel):
    """
    Yêu cầu công việc mà JD cung cấp.
    """
    knowledge: Optional[str] = Field(None, description="Kiến thức")
    skills: Optional[List[str]] = Field(None, description="Kỹ năng")
    experience: Optional[str] = Field(None, description="Kinh nghiệm làm việc")
    other_requirements: Optional[str] = Field(None, description="Yêu cầu khác (ví dụ: độ tuổi, giới tính, học vấn)")

class JD(BaseModel):
    """
    Mô hình dữ liệu cho JD (Job Description) mà người dùng cung cấp, gồm:
    - Mô tả công việc: mô tả công việc mà JD cung cấp.
    - Yêu cầu công việc:
        + Kiên thức: yêu cầu về kiến thức mà JD cung cấp.
        + Kỹ năng: yêu cầu về kỹ năng mà JD cung cấp.
        + Kinh nghiệm làm việc: yêu cầu về kinh nghiệm làm việc mà JD cung cấp.
        + Yêu cầu khác: yêu cầu khác mà JD cung cấp (ví dụ: yêu cầu về độ tuổi, giới tính, hoc vấn, v.v...).
    """
    job_description: _JobDescription = Field(..., description="Mô tả công việc")
    job_requirement: _JobRequirement = Field(..., description="Yêu cầu công việc")