from numpy import dot
from numpy.linalg import norm

def calculate_similarity(embedding1, embedding2) -> float:
    """
    Calculate the cosine similarity between two embeddings.
    """
    return dot(embedding1, embedding2) / (norm(embedding1) * norm(embedding2)) * 100