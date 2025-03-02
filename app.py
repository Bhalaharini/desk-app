from flask import Flask, render_template, request, url_for, flash
from werkzeug.utils import redirect
from flask_mysqldb import MySQL
import MySQLdb.cursors


app = Flask(__name__)
app.secret_key = 'many random bytes'

app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = '################'
app.config['MYSQL_DB'] = 'crud1'

mysql = MySQL(app)

@app.route('/')
def Index():
    return render_template('p1.html')

@app.route('/login', methods =['POST'])
def login():
    
    msg=''
    name=request.form.get('name')
    password=request.form.get('password')
    
    cursor=mysql.connection.cursor(MySQLdb.cursors.DictCursor)
    cursor.execute("""INSERT into `user` VALUES (%s,%s)""",(name,password))
    data1=cursor.fetchone()
    mysql.connection.commit()
    
    cur = mysql.connection.cursor()
    cur.execute("SELECT * FROM student")
    data = cur.fetchall()
    cur.close()

    return render_template('index.html', student=data)

       
    

@app.route('/insert', methods = ['POST'])
def insert():
    if request.method == "POST":
        flash("Data Inserted Successfully")
        date= request.form['date']
        EmpNo = request.form['EmpNo']
        Idno=request.form['Idno']
        status=request.form['status']
        phone = request.form['phone']
        cur = mysql.connection.cursor()
        cur.execute("INSERT INTO student (date,EmpNo,Idno,status, phone) VALUES (%s, %s, %s,%s,%s)", (date, EmpNo,Idno,status, phone))
        mysql.connection.commit()
        return render_template('in.html')

@app.route('/delete/<string:id_data>', methods = ['GET'])
def delete(id_data):
    flash("Record Has Been Deleted Successfully")
    cur = mysql.connection.cursor()
    cur.execute("DELETE FROM student WHERE id=%s", (id_data,))
    mysql.connection.commit()
    return redirect(url_for('Index'))



@app.route('/update', methods= ['POST', 'GET'])
def update():
    if request.method == 'POST':
        id_data = request.form['id']
        date= request.form['date']
        EmpNo = request.form['EmpNo']
        Idno=request.form['Idno']
        status=request.form['status']
        phone = request.form['phone']

        cur = mysql.connection.cursor()
        cur.execute("""
        UPDATE student SET date=%s, EmpNo=%s, Idno=%s, status=%s, phone=%s
        WHERE id=%s
        """, (date,EmpNo,Idno,status,phone, id_data))
        flash("Data Updated Successfully")
        return redirect(url_for('Index'))
@app.route('/ven')
def ven():
    return render_template('index.html')

if __name__ == "__main__":
    app.run(debug=True)