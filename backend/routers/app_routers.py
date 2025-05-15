from backend.services.load_cv import CreateCV
from backend.services.load_jd import CreateJD
from backend.services.review_cv import ReviewCV
import json
import numpy as np
from flask import render_template, request, jsonify

# Custom JSON encoder to handle NumPy types
class NumpyEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, np.integer):
            return int(obj)
        if isinstance(obj, np.floating):
            return float(obj)
        if isinstance(obj, np.ndarray):
            return obj.tolist()
        return super(NumpyEncoder, self).default(obj)

def init_routes(app):
    @app.route('/')
    def landing_page():
        return render_template('landing.html')

    @app.route('/auth')
    def auth_page():
        return render_template('auth.html')

    @app.route('/home')
    def home_page():
        return render_template('home.html')

    @app.route('/cv_review', methods=['POST'])
    def cv_review():
        """
        Receives CV file and JD then returns the review result.
        :return: JSON response with review result.
        """
        try:
            cv_file = request.files['cv']
            jd_str = request.form['jd']
        except Exception as e:
            print(f"Error retrieving CV or JD: {e}")
            return jsonify({
                'status': 'error',
                'message': f"Missing key: {str(e)}"
            }), 400

        try:
            CVS = CreateCV(cv_file)
            JDS = CreateJD(jd_str)

            cv_loaded = CVS.get_cv()
            jd_loaded = JDS.get_jd()
        except Exception as e:
            print(f"Error loading CV or JD: {e}")
            return jsonify({
                'status': 'error',
                'message': str(e)
            }), 400

        try:
            # Get result dictionary
            result = ReviewCV(cv_loaded, jd_loaded).get_result()

            print(result)

            # Use the custom encoder to handle NumPy types
            return app.response_class(
                response=json.dumps(result, cls=NumpyEncoder),
                status=200,
                mimetype='application/json'
            )
        except Exception as e:
            print(f"Error in CV review: {e}")
            return jsonify({
                'status': 'error',
                'message': str(e)
            }), 400
