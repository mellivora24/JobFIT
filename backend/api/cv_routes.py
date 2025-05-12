from flask import Blueprint, request, render_template, flash, redirect, url_for
from services.llm_service import review_cv
from utils.file_utils import extract_text_from_file
from models.cv_model import CV
from models.jd_model import JD
from config.database import save_qa
from utils.logger import setup_logger
import json

# Initialize logger
logger = setup_logger()

cv_bp = Blueprint('cv', __name__)


@cv_bp.route('/chat', methods=['GET', 'POST'])
def chat():
    """
    Handles the chat functionality for the CV and JD matching.
    GET: Renders the chat page.
    POST: Processes the CV and JD, and returns the answer to the question.
    """
    if request.method == 'POST':
        try:
            # Check if all required fields are provided
            if 'cv' not in request.files:
                logger.error("No CV file uploaded")
                flash("Please upload a CV file", "error")
                return render_template('chat.html')

            cv_file = request.files['cv']
            if cv_file.filename == '':
                logger.error("Empty CV filename")
                flash("Please select a valid CV file", "error")
                return render_template('chat.html')

            if 'jd' not in request.form or not request.form['jd'].strip():
                logger.error("No JD text provided")
                flash("Please provide a job description", "error")
                return render_template('chat.html')

            jd_text = request.form['jd']
            question = request.form.get('question', 'How well does this CV match the job description?')

            logger.info(
                f"Received request: question='{question}', cv_file='{cv_file.filename}', jd_length={len(jd_text)}")

            # Extract CV text
            cv_text = extract_text_from_file(cv_file)
            if not cv_text:
                logger.error(f"Failed to extract text from CV file: {cv_file.filename}")
                flash("Could not extract text from the uploaded CV file", "error")
                return render_template('chat.html')

            logger.debug(f"Extracted CV text: {cv_text[:100]}...")  # Log first 100 chars

            # Create CV and JD models
            try:
                # In a real implementation, you would parse the CV text to create a proper CV model
                # This is a simplified example
                cv_model = CV(
                    personal_info={"name": "Extracted from CV", "gender": "M/F", "email": "abc@gmail.com", "career_objective": "Career Objective"},
                    education=[],
                    skills=[],
                    work_experience=[]
                )

                # Create a simple JD model from the provided text
                jd_model = JD(
                    job_description={"title": "Job Position", "description": jd_text},
                    job_requirement={"knowledge": "", "experience": "", "other_requirements": ""}
                )

                # Get review result
                review_result = review_cv(cv_model, jd_model)
                print(review_result)
                print(type(review_result))
                review_result['matching_score'] = float(review_result['matching_score'])
                
                suggestions = review_result["suggestions"].replace('\n', '<br>')
                logger.debug(f"Suggestions: {suggestions}")
                matching_score = round(float(review_result["matching_score"]), 2)
                logger.debug(f"match_score: {matching_score}")

                # Save question and response to database
                # try:
                #     save_qa(question, cv_text, jd_text, response)
                #     logger.info("Saved Q&A to MongoDB")
                # except Exception as db_error:
                #     logger.error(f"Failed to save to database: {str(db_error)}")
                #     # Continue without failing the request

                return render_template('result.html', suggestions=suggestions, matching_score=matching_score)

            except Exception as parsing_error:
                logger.error(f"Error parsing CV or JD: {str(parsing_error)}")
                flash(f"Error processing the files: {str(parsing_error)}", "error")
                return render_template('chat.html')

        except Exception as e:
            logger.error(f"Error processing /chat request: {str(e)}")
            flash(f"An error occurred: {str(e)}", "error")
            return render_template('error.html', error=str(e)), 500

    # Render the chat page for GET requests
    logger.info("Rendering chat page")
    return render_template('chat.html')


@cv_bp.route('/history', methods=['GET'])
def history():
    """
    View history of CV reviews.
    """
    # Implement history viewing functionality here
    logger.info("Viewing CV review history")
    return render_template('history.html')