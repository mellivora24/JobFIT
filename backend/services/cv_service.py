from sentence_transformers import SentenceTransformer

model = SentenceTransformer('paraphrase-multilingual-MiniLM-L12-v2')
def create_cv_embedding(cv_text):
    """
    Creates an embedding for the CV file using a pre-trained model.
    :param cv_text:
    :return: The embedding of the CV file.
    """
    return model.encode(cv_text)

