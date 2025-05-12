from backend.utils.jd_parse import parse_text
from backend.utils.embedded_vector import embedded_vector

def create_jd_embedding(jd_text):
    """
    Creates an embedding for the job description text using a pre-trained model.
    :param jd_text: The job description text to create an embedding for.
    :return: The embedding of the job description text.
    """
    jd_content = parse_text(jd_text)

    embedded_jd = []
    for content in jd_content:
        if content is not None:
            embedded_jd.append(embedded_vector(content))
        else:
            embedded_jd.append(None)

    return embedded_jd