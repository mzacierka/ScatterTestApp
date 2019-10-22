from flask import Blueprint, render_template, redirect, url_for, request
import os

data = Blueprint('data', __name__)

@data.route("/data/upload_patient_test_data", methods=['POST'])
def upload_patient_test_data():
    testData = request.get_json(force=True)
    print(testData)

@data.route("/download_test_info", methods=['POST'])
def download_test_info():
    print("something - just so python will be happy")
    #add code that will grab the json stored in the database and push it to the app

@data.route("/upload_patient_questionnaire_answers", methods=['POST'])
def upload_patient_questionnaire_answers():
    try:
        questionnaire_answers = request.get_json() if request.is_json else None
    except Exception:
        raise ApiSysExceptions.invalid_json
    print(questionnaire_answers)
	#make sure to perform error checking - this endpoint is open to anyone
	
@data.route("/download_questions", methods=['POST'])
def download_questions():
    print("")
    #add code that will grab the data stored in the database and push it to the app
