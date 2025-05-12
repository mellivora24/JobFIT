
from utils.file_utils import extract_text_from_file
from utils.embedded_vector import embedded_vector

def create_cv_embedding(cv_text):
    """
    Creates an embedding for the CV file using a pre-trained model.
    :param cv_text: The CV text to create an embedding for.
    :return: The embedding of the CV file.
    """

    cv_content = extract_text_from_file(cv_text)

    embedded_cv = []
    for content in cv_content:
        if content is not None:
            embedded_cv.append(embedded_vector(content))
        else:
            embedded_cv.append(None)

    return embedded_cv