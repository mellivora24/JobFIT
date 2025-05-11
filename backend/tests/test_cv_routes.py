import pytest
from flask import Flask
from api.cv_routes import cv_bp
from unittest.mock import patch
import io

@pytest.fixture
def client():
    app = Flask(__name__)
    app.register_blueprint(cv_bp)
    app.config['TESTING'] = True
    with app.test_client() as client:
        yield client

@patch("services.llm_service.answer_question")
@patch("utils.file_utils.extract_text_from_file")
def test_chat_endpoint(mock_extract_text, mock_answer_question, client):
    mock_extract_text.return_value = "Tôi có 5 năm kinh nghiệm Python."
    mock_answer_question.return_value = "Match Score: 92%. Gợi ý: Thêm Docker."
    data = {
        "cv": (io.BytesIO(b"fake_pdf_content"), "test.pdf"),
        "jd": "Yêu cầu 3 năm kinh nghiệm Python.",
        "question": "CV này có phù hợp không?"
    }
    response = client.post('/chat', content_type='multipart/form-data', data=data)
    assert response.status_code == 200
    assert b"Match Score: 92%" in response.data