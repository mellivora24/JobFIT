import re
from backend.models.jd_model import JD, _JobDescription, _JobRequirement


def parse_text(text):
    """
    Parse plain text into a structured JD object
    :param text: Job description text (paragraph)
    :return: List of text segments for embedding
    """
    if isinstance(text, str):
        segments = segment_jd_text(text)
        return segments
    elif isinstance(text, list):
        return text
    else:
        return [str(text)]


def segment_jd_text(text):
    """
    Segment JD text into meaningful parts for embedding
    :param text: Raw JD text
    :return: List of text segments
    """
    # Split text into sections
    sections = re.split(r'\n\s*\n', text)
    sections = [s.strip() for s in sections if s.strip()]

    # Identify job description and requirements sections
    description_sections = []
    requirement_sections = []

    for section in sections:
        lower_section = section.lower()
        # Check if section contains requirements keywords
        if any(kw in lower_section for kw in ['yêu cầu', 'requirements', 'qualification', 'skills needed']):
            requirement_sections.append(section)
        else:
            description_sections.append(section)

    # If no clear segmentation was possible, use the original structure
    if not requirement_sections:
        # Just split the text roughly in half for description and requirements
        half_point = len(sections) // 2
        description_sections = sections[:half_point] if half_point > 0 else sections
        requirement_sections = sections[half_point:] if half_point < len(sections) else []

    # Combine sections
    description_text = "\n\n".join(description_sections)
    requirement_text = "\n\n".join(requirement_sections)

    return [description_text, requirement_text]


def create_jd_object(text):
    """
    Creates a JD object from the provided text
    :param text: Job description text
    :return: JD object
    """
    segments = segment_jd_text(text)

    description_text = segments[0] if segments else text
    requirement_text = segments[1] if len(segments) > 1 else ""

    # Extract skills from requirement text
    skills = extract_skills(requirement_text)

    # Create JD components
    job_description = _JobDescription(
        title=extract_job_title(description_text),
        description=description_text
    )

    job_requirement = _JobRequirement(
        knowledge=extract_knowledge(requirement_text),
        skills=skills,
        experience=extract_experience(requirement_text),
        other_requirements=extract_other_requirements(requirement_text)
    )

    return JD(
        job_description=job_description,
        job_requirement=job_requirement
    )


def extract_job_title(text):
    """Extract job title from text"""
    # Look for a short first line that might be the title
    lines = text.split('\n')
    if lines and len(lines[0]) < 100:
        return lines[0].strip()
    return "Job Position"  # Default title


def extract_skills(text):
    """Extract skills from requirement text"""
    skills = []
    # Look for bullet points or numbered lists
    skill_patterns = [
        r'[-•*]\s*([^•\n-]+)',  # Bullet points
        r'\d+\.\s*([^\n]+)',  # Numbered lists
    ]

    for pattern in skill_patterns:
        matches = re.findall(pattern, text)
        if matches:
            skills.extend([match.strip() for match in matches if match.strip()])

    # If no skills found, look for common technical terms
    if not skills:
        tech_terms = [
            "Python", "Java", "JavaScript", "TypeScript", "React", "Angular", "Vue",
            "Node.js", "SQL", "NoSQL", "MongoDB", "AWS", "Azure", "Docker", "Git",
            "DevOps", "CI/CD", "REST API", "GraphQL", "HTML", "CSS", "UI/UX",
            "Machine Learning", "AI", "Data Science", "Big Data", "Cloud Computing"
        ]

        for term in tech_terms:
            if term.lower() in text.lower():
                skills.append(term)

    return skills[:10]  # Limit to 10 skills


def extract_knowledge(text):
    """Extract knowledge requirements"""
    knowledge_section = ""

    # Look for sections that might contain knowledge requirements
    knowledge_keywords = ["knowledge", "kiến thức", "academic", "education", "học vấn"]

    for keyword in knowledge_keywords:
        pattern = rf'{keyword}[:\s]+(.*?)(?:\n\n|\Z)'
        match = re.search(pattern, text, re.IGNORECASE | re.DOTALL)
        if match:
            knowledge_section = match.group(1).strip()
            break

    if not knowledge_section:
        # Look for education level requirements
        edu_levels = ["bachelor", "master", "phd", "degree", "cử nhân", "thạc sĩ", "tiến sĩ", "bằng cấp"]
        for level in edu_levels:
            if level.lower() in text.lower():
                sentence_pattern = r'[^.!?]*' + level + r'[^.!?]*[.!?]'
                match = re.search(sentence_pattern, text, re.IGNORECASE)
                if match:
                    knowledge_section = match.group(0).strip()
                    break

    return knowledge_section


def extract_experience(text):
    """Extract experience requirements"""
    experience_section = ""

    # Look for experience requirements
    exp_keywords = ["experience", "kinh nghiệm", "years", "năm"]

    for keyword in exp_keywords:
        pattern = rf'{keyword}[:\s]+(.*?)(?:\n\n|\Z)'
        match = re.search(pattern, text, re.IGNORECASE | re.DOTALL)
        if match:
            experience_section = match.group(1).strip()
            break

    if not experience_section:
        # Look for years of experience
        year_pattern = r'(\d+)[\+\s]*(year|năm)'
        match = re.search(year_pattern, text, re.IGNORECASE)
        if match:
            sentence_pattern = r'[^.!?]*' + match.group(0) + r'[^.!?]*[.!?]'
            exp_match = re.search(sentence_pattern, text, re.IGNORECASE)
            if exp_match:
                experience_section = exp_match.group(0).strip()

    return experience_section


def extract_other_requirements(text):
    """Extract other requirements"""
    # This function extracts requirements that are not skills, knowledge or experience
    other_req_keywords = ["other", "khác", "additional", "bonus", "preferred", "location", "benefits", "salary"]

    for keyword in other_req_keywords:
        pattern = rf'{keyword}[:\s]+(.*?)(?:\n\n|\Z)'
        match = re.search(pattern, text, re.IGNORECASE | re.DOTALL)
        if match:
            return match.group(1).strip()

    return ""
