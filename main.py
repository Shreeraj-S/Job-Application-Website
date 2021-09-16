from flask import Flask, render_template, request, redirect 
from flask_mysqldb import MySQL

app = Flask(__name__)

app.config["MYSQL_HOST"] = "sql6.freemysqlhosting.net"
app.config["MYSQL_USER"] = "sql6437644"
app.config["MYSQL_PASSWORD"] = "YvgMiyUdpB"
app.config["MYSQL_DB"] = "sql6437644"

mydatabase = MySQL(app)

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "POST":
        # data fetching
        userDetails = request.form
        #Assigning to variables
        firstname = userDetails['firstname']
        lastname = userDetails['lastname']
        email = userDetails["email"]
        phone = userDetails["phone"]
        gender = userDetails["gender"]
        skills = ", ".join(userDetails.getlist("skill"))
        experience = userDetails["experience"]
        noticeperiod = userDetails["noticeperiod"]
        currentctc = userDetails["currentctc"]
        expectedctc = userDetails["expectedctc"]
        #Inserting data to db
        cur = mydatabase.connection.cursor()
        insertQuery = f"""INSERT INTO userForm(firstname, lastname, email, phone, gender, skills, experience, noticeperiod, currentctc, expectedctc) 
                            VALUES('{firstname}','{lastname}', '{email}', '{phone}', '{gender}', '{skills}', '{experience}', '{noticeperiod}', '{currentctc}', '{expectedctc}')"""
        cur.execute(insertQuery) # "(INSERT INTO register(username, email) VALUES(%s, %s),(username, email))"
        mydatabase.connection.commit()
        cur.close() 
        return redirect("/users")
    return render_template("register.html")

@app.route("/users")
def users():
    cur = mydatabase.connection.cursor()
    selectQuery = "SELECT * FROM userForm"
    result = cur.execute(selectQuery)
    if result > 0:
        userDetails = cur.fetchall()
        cur.close()
        return render_template("users.html", userDetails = userDetails)
    else:
        return "Nobody Has registered yet"

if __name__ == "__main__":
    app.run(debug=True)