import numpy as np
from numpy import dot
from numpy.linalg import norm


def calculate_similarity(embeddings1, embeddings2) -> float:
    """
    Tính toán độ tương đồng giữa hai danh sách embedding bằng cách sử dụng cosine similarity.

    :param embeddings1: Danh sách đầu tiên của CV embedding
    :param embeddings2: Danh sách thứ hai của JD embedding
    :return: Độ tương đồng trung bình giữa hai danh sách embedding (0-100)
    """
    if not embeddings1 or not embeddings2:
        return 0.0

    similarities = []
    for emb1, emb2 in zip(embeddings1, embeddings2):
        if emb1 is not None and emb2 is not None:
            cos_sim = dot(emb1, emb2) / (norm(emb1) * norm(emb2))
            similarities.append(cos_sim)

    if not similarities:
        return 0.0

    return np.mean(similarities) * 100