from sentence_transformers import SentenceTransformer
from utils.file_utils import extract_text_from_file

model = SentenceTransformer('paraphrase-multilingual-MiniLM-L12-v2')
def create_cv_embedding(cv_file):
    """
    Creates an embedding for the CV file using a pre-trained model.
    :param cv_file: The CV file to create an embedding for.
    :return: The embedding of the CV file.
    """
    text = extract_text_from_file(cv_file)
    return model.encode(text)