
from operator import concat
from flask import Flask,request,render_template
from flask_mysqldb import MySQL
import pickle
import numpy as np


app = Flask(__name__)


###### MYSQL Configuration 
app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = 'Only@morde123'
app.config['MYSQL_DB'] = 'siddheshwar_morde'

mysql = MySQL(app)

@app.route('/')
def index():

    return render_template('index.html')

@app.route('/data',methods=['GET','POST'])
def data():

    user_data = request.form

    Dates = request.form['Date']
    work = request.form['work']
    time_in = request.form['time_in']
    time_out = request.form['time_out']
    delete_data=request.form['delete_data']
    data =""

    cursor = mysql.connection.cursor()
    if request.form['submit_button'] == 'Write':
        query = 'CREATE TABLE IF NOT EXISTS attendance(Date text,work varchar(20),time_in text ,time_out text)'
        cursor.execute(query)
        cursor.execute('INSERT INTO attendance(Date,work,time_in,time_out) VALUES(%s,%s,%s,%s)',(Dates,work,time_in,time_out))
        # mysql.connection.commit()
        # cursor.close()
        msg ="write success"

    if request.form['submit_button'] == 'read':
        cursor.execute("SELECT * FROM attendance")
        data = cursor.fetchall()
        msg ="Read Success"
    if request.form['submit_button'] == 'delete':

        sql = (f"DELETE FROM attendance WHERE Date ='{str(delete_data)}'")
        print(sql)
        cursor.execute(sql)
        msg ="Delete Success"
        cursor.execute("SELECT * FROM attendance")
        data = cursor.fetchall()
    mysql.connection.commit()
    cursor.close()

    return render_template('index.html',success=msg,data=data)


if __name__ == "__main__":
    app.run(host = '127.0.0.100',debug=True)