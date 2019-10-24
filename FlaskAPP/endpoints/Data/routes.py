from flask import Blueprint, Response, render_template, redirect, url_for, request, jsonify, send_file
from FlaskAPP.models.Questions import Questions
from FlaskAPP.models.jsonfiles import JSONFiles
from flask_marshmallow import Marshmallow
from sqlalchemy.sql.expression import func, select
from FlaskAPP import ma
import os
import json
import requests

from io import BytesIO


class QuestionSchema(ma.ModelSchema):
    class Meta:
        model = Questions


class JSONFileSchema(ma.ModelSchema):
    class Meta:
        model = JSONFiles


data = Blueprint('data', __name__)


@data.route("/data/upload_patient_test_data", methods=['POST'])
def upload_patient_test_data():
    try:
        testData = request.get_json() if request.is_json else None
    except Exception:
        raise ApiSysExceptions.invalid_json
    for x in testData:
        print(x)
    
    print("This should work")
    return "Great job!"


@data.route('/data/download/<filename>')
def download_test(filename):
    file_data = JSONFiles.query.filter_by(name=filename).first()
    return send_file(BytesIO(file_data.data), attachment_filename=filename, as_attachment=True)


@data.route('/data/download/getTestList')
def getList():
    fileList = JSONFiles.query.order_by(JSONFiles.name).all()
    file_schema = JSONFileSchema(many=True)
    output = file_schema.dump(fileList)
    return jsonify(output)


@data.route("/data/download_test_info", methods=['POST', 'GET'])
def download_test_info():
    # pull from database
    # downloadFile = TestData.query.filter_by("DoctorID").all()
    return "Great job!"
    # add code that will grab the json stored in the database and push it to the app


@data.route("/data/upload_patient_questionnaire_answers", methods=['POST'])
def upload_patient_questionnaire_answers():
    try:
        questionnaire_answers = request.get_json() if request.is_json else None
    except Exception:
        raise ApiSysExceptions.invalid_json
    print(questionnaire_answers)
    return "Great job!"


# make sure to perform error checking - this endpoint is open to anyone


@data.route("/data/download_questions", methods=['POST', 'GET'])
def download_questions():

    questions = Questions.query.order_by(func.random(Questions.QuestionID)).limit(5)
    question_schema = QuestionSchema(many=True)
    output = question_schema.dump(questions)
    return jsonify(output)
   
#    ''' return jsonify(Question=questions[0].Question, 
#     QuestionType=questions[0].QuestionType, 
#     PossibleAnswers=questions[0].PossibleAnswers, 
#     QuestionID=questions[0].QuestionID)
#     #add code that will grab the data stored in the database and push it to the app
#     '''
