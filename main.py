from flask import Flask, render_template
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



if __name__ == '__main__':
    app.run(debug=True)

