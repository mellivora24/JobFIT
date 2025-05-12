import openai
import json
from backend.config.settings import Settings
from backend.models.cv_model import CV
from backend.models.jd_model import JD
from backend.services.cv_service import create_cv_embedding
from backend.services.jd_service import create_jd_embedding
from backend.services.similarity_service import calculate_similarity

# Configure the OpenAI API key
openai.api_key = Settings.OPENAI_API_KEY


def _create_json_cv(cv: CV):
    """
    Convert CV object to JSON string
    """
    return cv.model_dump_json()


def _create_json_jd(jd: JD):
    """
    Convert JD object to JSON string
    """
    return jd.model_dump_json()


def _extract_text_from_cv(cv_json: str):
    """
    Extract relevant text fields from CV JSON for embedding
    """
    cv_data = json.loads(cv_json)
    texts = []

    # Extract personal info
    personal_info = cv_data.get("personal_info", {})
    personal_text = f"{personal_info.get('name', '')} {personal_info.get('career_objective', '')}"
    texts.append(personal_text.strip())

    # Extract education
    education_texts = []
    for edu in cv_data.get("education", []):
        edu_text = f"{edu.get('university', '')} {edu.get('major', '')} {edu.get('degree', '')}"
        education_texts.append(edu_text.strip())
    texts.append(" ".join(education_texts))

    # Extract skills
    skills_text = " ".join(cv_data.get("skills", []))
    texts.append(skills_text)

    # Extract work experience
    work_exp_texts = []
    for exp in cv_data.get("work_experience", []):
        exp_text = f"{exp.get('position', '')} at {exp.get('company', '')} {exp.get('description', '')}"
        work_exp_texts.append(exp_text.strip())
    texts.append(" ".join(work_exp_texts))

    return texts


def _extract_text_from_jd(jd_json: str):
    """
    Extract relevant text fields from JD JSON for embedding
    """
    jd_data = json.loads(jd_json)
    texts = []

    # Extract job description
    job_desc = jd_data.get("job_description", {})
    desc_text = f"{job_desc.get('title', '')} {job_desc.get('description', '')}"
    texts.append(desc_text.strip())

    # Extract job requirements
    job_req = jd_data.get("job_requirement", {})
    req_text = f"{job_req.get('knowledge', '')} {job_req.get('experience', '')} {job_req.get('other_requirements', '')}"
    texts.append(req_text.strip())

    # Extract required skills
    skills = job_req.get("skills", [])
    if skills:
        skills_text = " ".join(skills)
        texts.append(skills_text)

    return texts


def _get_suggestions_from_openai(cv_json, jd_json):
    """
    Get suggestions for CV improvement based on JD using OpenAI
    """
    response = openai_client.chat.completions.create(
        model="gpt-4.0",
        messages=[
            {
                "role": "user",
                "content": f"Hãy đề xuất cải tiến CV dựa vào JD sau, những trường không có nội dung được hiểu là thiếu:\nCV: {cv_json}\nJD: {jd_json}"
            }
        ]
    )
    return response.choices[0].message.content


def _get_matching_score(cv_json, jd_json):
    """
    Calculate matching score between CV and JD
    """
    cv_text = _extract_text_from_cv(cv_json)
    jd_text = _extract_text_from_jd(jd_json)

    cv_embedding = create_cv_embedding(cv_text)
    jd_embedding = create_jd_embedding(jd_text)

    similarity_score = calculate_similarity(cv_embedding, jd_embedding)
    return similarity_score


def review_cv(cv: CV, jd: JD):
    """
    Review CV based on JD
    :param cv: CV object
    :param jd: JD object
    :return: suggestions and matching score
    """
    cv_json = _create_json_cv(cv)
    jd_json = _create_json_jd(jd)

    suggestions = _get_suggestions_from_openai(cv_json, jd_json)
    matching_score = _get_matching_score(cv_json, jd_json)

    return {
        "suggestions": suggestions,
        "matching_score": matching_score
    }
