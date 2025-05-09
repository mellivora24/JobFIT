from sentence_transformers import SentenceTransformer

model = SentenceTransformer('paraphrase-multilingual-MiniLM-L12-v2')
def create_jd_embedding(jd_text):
    """
    Creates an embedding for the job description text using a pre-trained model.
    :param jd_text: The job description text to create an embedding for.
    :return: The embedding of the job description text.
    """
    return model.encode(jd_text)