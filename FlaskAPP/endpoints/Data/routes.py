from io import BytesIO
import json
from FlaskAPP import ma, db
from sqlalchemy import desc
from sqlalchemy.sql.expression import func
from flask import Flask, Blueprint, Response, render_template, redirect, url_for, request, jsonify, send_file
from FlaskAPP.models.questions import Questions
from FlaskAPP.models.jsonfiles import JSONFiles
from FlaskAPP.models.circles import Circles
from FlaskAPP.models.answers import Answers
from FlaskAPP.models.pressure import Pressure
from FlaskAPP.models.testframe import TestFrame
from random import randint
import flask_marshmallow
import xlsxwriter
import datetime, time

class QuestionSchema(ma.ModelSchema):
    class Meta:
        model = Questions


class JSONFileSchema(ma.ModelSchema):
    class Meta:
        model = JSONFiles


data = Blueprint('data', __name__)

# Divdies to get milliseconds, then subtracts from the start time to get interval
def convert(nano, testStartTime):
    return (nano - testStartTime) / 100000

@data.route("/data/upload_patient_test_data", methods=['POST'])
def upload_patient_test_data():
    try:
        testData = request.get_json() if request.is_json else None
    except Exception:
        raise ApiSysExceptions.invalid_json
    
    # Get testframe data
    testID = round(time.time())
    doctorID = testData["doctorID"]
    patientID = testData["patientID"]
    testStartTime = testData["testStartTime"] 
    testEndTime = testData["testEndTime"]
    testName = testData["testName"]

    if(testName == "alphabet_test"):
        testName = "AlphabetTest.json"

    # Get the difference in time from start to end, then convert to seconds
    convertToSeconds = ((testEndTime / 100000000) - (testStartTime / 100000000))
    testLength = str(datetime.timedelta(seconds=convertToSeconds))

    # Target symbol to circle
    targetSymbol = testData["answerSymbol"]

    # Begin transaction
    db.session.rollback()

    # Create the row for the test frame
    testframe = TestFrame(TestID = testID, PatientID = patientID, 
        DoctorID = doctorID, DateTaken = str(datetime.date.today()), 
        TestName = testName, TestLength = testLength)

    db.session.add(testframe)
    db.session.commit()

    db.session.rollback()
    # Loop through each circle made
    for i in range(len(testData["patientAnswers"])):
        
        currentSymbol = testData["patientAnswers"][i]
        currentTouchDataArray = testData["patientAnswerTouchData"][i]

        # Get intervals 
        beginTime = convert(currentTouchDataArray[0]['time'], testStartTime)
        endTime = convert(currentTouchDataArray[len(currentTouchDataArray)-1]['time'], testStartTime)
        totalTime = endTime - beginTime

        # Create a row for circle, then add it
        CircleRow = Circles(TestID = testID, CircleID = i, 
                symbol = currentSymbol['name'], begin_circle = beginTime,
                end_circle = endTime, total_time = totalTime)

        db.session.add(CircleRow)

    db.session.commit()
    db.session.rollback()

    # Loop through the pressure data
    # Important this is committed separately to avoid foreign key constraints
    for i in range(len(testData["patientAnswers"])):
        
        currentSymbol = testData["patientAnswers"][i]
        currentTouchDataArray = testData["patientAnswerTouchData"][i]    
        
        # Loop through Touch Data, PressureIDCounter counts each touch made, per circle
        PressureIDCounter = 0
        for point in currentTouchDataArray:
                
                # you have access to each point in the touch array
                PressureRow = Pressure(TestID = testID, CircleID = i, PressureID = PressureIDCounter,
                    Xcoord = point['x'], Ycoord = point['y'], Pressure = point['force'])
                PressureIDCounter += 1
                db.session.add(PressureRow)

    # Complete transaction
    db.session.commit()
    db.session.close()

    return "Nice!"

@data.route("/data/upload_patient_questionnaire_answers", methods=['POST'])
def upload_patient_questionnaire_answers():
    try:
        data = request.get_json() if request.is_json else None
    except Exception:
        raise ApiSysExceptions.invalid_json
    
    db.session.rollback()

    testframe = TestFrame.query.order_by(desc(TestFrame.TestID)).first()

    testID = testframe.TestID

    for question in data["answers"]:
        answer = question["Answer"]
        questionID = question["QuestionID"]

        # Add row for each answer given
        row = Answers(TestID = testID, QuestionID = questionID, Answer = answer)
        db.session.add(row)

    db.session.commit()

    return "Answers"

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
    
