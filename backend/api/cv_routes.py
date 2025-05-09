from flask import Blueprint, request, render_template
from services.llm_service import answer_question
from utils.file_utils import extract_text_from_file
from config.database import save_qa

cv_bp = Blueprint('cv', __name__)

@cv_bp.route('/chat', methods=['POST'])
def chat():
    """
    Handles the chat request by extracting text from the CV file,
    answering the question based on the CV and JD text, and saving the QA.
    """
    cv_file = request.files['cv']
    jd_text = request.form['jd']
    question = request.form['question']
    cv_text = extract_text_from_file(cv_file)
    response = answer_question(question, cv_text, jd_text)
    # save_qa(question, cv_text, jd_text, response)
    return render_template('result.html', response=response)