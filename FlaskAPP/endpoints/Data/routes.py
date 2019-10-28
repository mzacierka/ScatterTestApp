from io import BytesIO
import json
from FlaskAPP import ma
from sqlalchemy.sql.expression import func
from flask import Blueprint, Response, render_template, redirect, url_for, request, jsonify, send_file
from FlaskAPP.models.questions import Questions
from FlaskAPP.models.jsonfiles import JSONFiles
from FlaskAPP.models.circles import Circles
from FlaskAPP.models.answers import Answers
from FlaskAPP.models.pressure import Pressure
from FlaskAPP.models.testframe import TestFrame
import flask_marshmallow
import xlsxwriter


class QuestionSchema(ma.ModelSchema):
    class Meta:
        model = Questions


class JSONFileSchema(ma.ModelSchema):
    class Meta:
        model = JSONFiles


data = Blueprint('data', __name__)

@data.route("/data/upload_patient_test_data", methods=['POST'])
def upload_patient_test_data():
    # try:
    #     testData = request.get_json("FlaskAPP\static\json\sample.json") if request.is_json else None
    # except Exception:
    #     raise ApiSysExceptions.invalid_json
    # for x in testData:
    #     print(x)
    
    
    file = open("FlaskAPP/static/json/sample.json")
    jsonfile = json.dumps(file.read())

    # for item in jsonfile
    #     print(item[0])

    print("This should work")
    return "Great job!"


@data.route('/data/download/<filename>')
def download_test(filename):
    file_data = JSONFiles.query.filter_by(name=filename).first()
    return send_file(BytesIO(file_data.data), attachment_filename=filename, as_attachment=True)


@data.route('/data/download/getTestList')
def getList():
    fileList = JSONFiles.query.all()
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

    questions = Questions.query.order_by(func.rand()).limit(5)
    question_schema = QuestionSchema(many=True)
    output = question_schema.dump(questions)
    return jsonify(output)
   
#    ''' return jsonify(Question=questions[0].Question, 
#     QuestionType=questions[0].QuestionType, 
#     PossibleAnswers=questions[0].PossibleAnswers, 
#     QuestionID=questions[0].QuestionID)
#     #add code that will grab the data stored in the database and push it to the app
#     '''

@data.route('/data/get_excel')
def get_excel():

    
    
    workbook = xlsxwriter.Workbook('hello.xlsx')
    formula = workbook.add_worksheet()
    raw = workbook.add_worksheet()
    final = workbook.add_worksheet()
    
    
    formula.write('A1', 'Hello world')
    raw.write('A2', )

    workbook.close()

    return "Hi"
    
