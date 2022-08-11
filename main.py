from flask import Flask, render_template, request
from flask_mysqldb import MySQL
import MySQLdb.cursors
import pymysql

app = Flask(__name__)
app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = ''
app.config['MYSQL_DB'] = 'doctoral'
mysql = MySQL(app)

@app.route('/')
def example():
    cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
    cursor.execute("SELECT * FROM Instructor")
    instructors = cursor.fetchall()
    return render_template("demo.html", instructors=instructors)

# This function must:
# - Add a student into the database
# - Link the new student with an existing scholarship
# - Add committee members for the student in the PhDCommittee table
@app.route('/add_student', methods=['GET','POST'])
def add_student():
    if request.method == "POST":
        # Fetching the data from the form
        details = request.form
        stuid = details['StudentId']
        fName = details['FName']
        lName = details['LName']
        stSem = details['StSem']
        stYear = details['StYear']
        supervisor = details['Supervisor']
        scholarship_t = details['Scholarship_Type']
        scholarship_s = details['Scholarship_Source']
        cursor = mysql.connection.cursor()
        cursor.execute("INSERT INTO `phdstudent`(`StudentId`, `FName`, `LName`, `StSem`, `StYear`, `Supervisor`) VALUES"
                       " ('"+stuid+"','"+fName+"','"+lName+"','"+stSem+"','"+stYear+"','"+supervisor+"')")
        cursor.execute("INSERT INTO `scholarshipsupport`(`StudentId`, `Type`, `Source`) VALUES ('"+stuid+"','"+scholarship_t+"','"+scholarship_s+"')")
        cursor.execute("INSERT INTO `phdcommittee`(`StudentId`, `InstructorId`) VALUES ('"+stuid+"','"+supervisor+"')")
        mysql.connection.commit()
        cursor.close()
        return 'success'
    return render_template("add_student.html")

@app.route('/del_students', methods=['GET','POST'])
def del_ssstudent():
    if request.method == "POST":
        # Fetching the data from form
        details = request.form
        stuid = details['StudentId']
        cursor = mysql.connection.cursor()
        cursor.execute("DELETE st FROM phdstudent st WHERE EXISTS (SELECT * FROM selfsupport sst WHERE (sst.StudentId = "
                       "st.StudentId) AND (sst.StudentId = '"+stuid+"') AND (st.StudentId NOT IN (SELECT StudentId "
                                                                    "FROM milestonespassed)));")
        mysql.connection.commit()
        cursor.close()
        return 'success'
    return render_template("del_student.html")

if __name__ == '__main__':
    app.run(debug=True)

