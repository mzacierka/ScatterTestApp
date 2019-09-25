from flask import Flask, render_template, request, json
import pymysql.cursors

app = Flask(__name__)

connection = pymysql.connect(host='bigbaloney.ca2jrvwqedaj.us-east-1.rds.amazonaws.com',
                             user='admin',
                             password='PvpcYgwj7d2QHJjL',
                             db='test',
                             charset='utf8mb4',
                             cursorclass=pymysql.cursors.DictCursor)



try:
    with connection.cursor() as cursor:
        # Read a single record
        sql = "SELECT `*` FROM `testTable`"
        cursor.execute(sql)
        result = cursor.fetchone()
        print(result)
finally:
    connection.close()
    




@app.errorhandler(404)
def pageNotFound(e):
    return "<h1> 404 Oh no idiot this page doesn't exist</h1>"

@app.errorhandler(500)
def internalError(e):
    return "<h1> Internal Server Error, plz fix</h1>"

@app.route('/user/<name>')
def index(name): 
    return '<h1>Hello {}!</h1>'.format(name)

@app.route('/')
def main():
    return render_template('index.html')

@app.route('/showSignUp')
def showSignUp():
    return render_template('signup.html')
    
if __name__ == "__main__":
    app.run(debug=True) 