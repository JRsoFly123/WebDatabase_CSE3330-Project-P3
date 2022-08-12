# Team 8
# Daniel Duy Phan (1001728612)
# Jeremiah Richard (1001475742)

from flask import Flask, render_template, request
from flask_mysqldb import MySQL
import MySQLdb.cursors
import pymysql

# Sets up the connection for the database
app = Flask(__name__)
app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = ''
app.config['MYSQL_DB'] = 'doctoral'
mysql = MySQL(app)

# This function will:
# - lead to the home page of the web interface which will contain hyperlinks to the supported queries
#   for the DOCTORAL database.
@app.route('/')
def main_page():
    return render_template("main_page.html")

# This function will:
# - Add a student into the database
# - Link the new student with an existing scholarship
# - Add committee members for the student in the PhDCommittee table
@app.route('/insert_student', methods=['GET','POST'])
def insert_student():
    if request.method == "POST":

        # Fetches the data from the form
        details = request.form
        stuid = details['StudentId']
        fName = details['FName']
        lName = details['LName']
        stSem = details['StSem']
        stYear = details['StYear']
        supervisor = details['Supervisor']
        scholarship_t = details['Scholarship_Type']
        scholarship_s = details['Scholarship_Source']

        # Inserts the form data into the PHDSTUDENT, PHDCOMMITEE, and SCHOLARSHIPSUPPORT tables
        cursor = mysql.connection.cursor()
        cursor.execute("INSERT INTO `phdstudent`(`StudentId`, `FName`, `LName`, `StSem`, `StYear`, `Supervisor`) VALUES"
                       " ('"+stuid+"','"+fName+"','"+lName+"','"+stSem+"','"+stYear+"','"+supervisor+"');")
        cursor.execute("INSERT INTO `phdcommittee`(`StudentId`, `InstructorId`) VALUES ('"+stuid+"','"+supervisor+"');")
        cursor.execute("INSERT INTO `scholarshipsupport`(`StudentId`, `Type`, `Source`) VALUES ('"+stuid+"','"+scholarship_t+"','"+scholarship_s+"');")
        mysql.connection.commit()
        cursor.close()
        return 'Insert successful!'
    return render_template("insert_student.html")

# This function will:
# - update the payment of all TAs for a course based on a provided course ID.
@app.route('/update_payment_TA', methods=['GET','POST'])
def update_payment_TA():
    if request.method == 'POST':

        # Fetches the data from the form
        details = request.form
        courseId = details['CourseId']
        updatedMonthyPay = details['MonthlyPay']

        # Updates the GTA table
        cursor = mysql.connection.cursor()
        cursor.execute('UPDATE GTA gt SET gt.MonthlyPay = ' + updatedMonthyPay + ' WHERE gt.SectionId IN '
                    + '(SELECT s.SectionId FROM SECTION s, COURSE c, GTA gt '
                    + 'WHERE s.CourseId = c.CourseId AND gt.SectionId = s.SectionId AND c.CourseId = ' + "'" + courseId + "'" +');')
        mysql.connection.commit()
        cursor.close()
        return 'Update successful!'
    return render_template('update_payment_TA.html')

# This function will:
# - Get user input for a GRA student ID
# - Display Grant Title, Type and Account No. of Grant
@app.route('/display_grant',methods=['GET','POST'])
def display_grant():
    if request.method == "POST":

        # Fetches the data from the form
        details = request.form
        stuid = details['StudentId']

        # Displays the corresponding GRANT record
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute("SELECT g.GrantTitle, g.Type, g.AccountNo FROM gra as gr join `grants` as g on gr.Funding = g.AccountNo WHERE gr.StudentId = '"+stuid+"'")
        grant = cursor.fetchall()
        return render_template("display_grant.html", grant=grant)
    return render_template("get_graID.html")

# This function will
# - delete a self-support student if they haven't pass a milestone yet.
@app.route('/delete_self_support_student', methods=['GET','POST'])
def del_self_supportstudent():
    if request.method == "POST":

        # Fetches the data from the form
        details = request.form
        stuid = details['StudentId']

        # Deletes the student from the PHDSTUDENT table
        cursor = mysql.connection.cursor()
        cursor.execute("DELETE st FROM phdstudent st WHERE EXISTS (SELECT * FROM selfsupport sst WHERE (sst.StudentId = "
                       "st.StudentId) AND (sst.StudentId = '"+stuid+"') AND (st.StudentId NOT IN (SELECT StudentId "
                                                                    "FROM milestonespassed)));")
        mysql.connection.commit()
        cursor.close()
        return 'Query successful!'
    return render_template("delete_self_support_student.html")

if __name__ == '__main__':
    app.run(debug=True)

