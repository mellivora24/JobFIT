from flask import Blueprint, request, render_template
from services.llm_service import answer_question
from utils.file_utils import extract_text_from_file
from config.database import save_qa
from utils.logger import setup_logger

# Initialize logger
logger = setup_logger()

cv_bp = Blueprint('cv', __name__)

@cv_bp.route('/chat', methods=['GET', 'POST'])
def chat():
    """
    Handles the chat functionality for the CV and JD matching.\n
    GET: Renders the chat page.\n
    POST: Processes the CV and JD, and returns the answer to the question.
    """
    if request.method == 'POST':
        try:
            cv_file = request.files['cv']
            jd_text = request.form['jd']
            question = request.form['question']
            logger.info(f"Received request: question='{question}', cv_file='{cv_file.filename}', jd_length={len(jd_text)}")
            
            cv_text = extract_text_from_file(cv_file)
            logger.debug(f"Extracted CV text: {cv_text[:100]}...")  # Log first 100 chars
            
            response = answer_question(question, cv_text, jd_text)
            logger.info(f"Chatbot response: {response[:100]}...")  # Log first 100 chars
            
            # save_qa(question, cv_text, jd_text, response)
            # logger.info("Saved Q&A to MongoDB")
            
            return render_template('result.html', response=response)
        except Exception as e:
            logger.error(f"Error processing /chat request: {str(e)}")
            return render_template('error.html', error=str(e)), 500
        
    # Render the chat page for GET requests
    logger.info("Rendering chat page")
    return render_template('chat.html')