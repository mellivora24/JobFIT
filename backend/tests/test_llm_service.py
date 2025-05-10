import pytest
from unittest.mock import patch
from services.llm_service import answer_question

@pytest.fixture
def mock_openai():
    with patch("openai.ChatCompletion.create") as mock:
        mock.return_value = {
            "choices": [{"message": {"content": "Match Score: 92%. Gợi ý: Thêm Docker."}}]
        }
        yield mock

def test_answer_question(mock_openai):
    question = "CV này có phù hợp không?"
    cv_text = "Tôi có 5 năm kinh nghiệm Python."
    jd_text = "Yêu cầu 3 năm kinh nghiệm Python."
    response = answer_question(question, cv_text, jd_text)
    assert "Match Score: 92%" in response
    assert "Thêm Docker" in response