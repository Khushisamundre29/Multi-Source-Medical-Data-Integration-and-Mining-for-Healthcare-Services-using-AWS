from flask import request, Flask, render_template, session, redirect, url_for, flash
import pymysql
import pandas as pd
from datetime import datetime

app = Flask(__name__)
app.config['SECRET_KEY'] = 'f9bf78b9a18ce6d46a0cd2b0b86df9da'

def getdb():
    # Update with your actual MySQL credentials
    db = pymysql.connect(host='localhost', user='root', password='manager', db='multisource', port=3306)
    cur = db.cursor()
    return db, cur

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/admin", methods=["POST", "GET"])
def admin():
    if request.method == "POST":
        name = request.form["name"]
        pwd = request.form["pwd"]
        if name == "admin" and pwd == "admin":
            return render_template("adminhome.html", msg="success")
    return render_template("admin.html")

@app.route("/viewdoctors")
def viewdoctors():
    db, cur = getdb()
    sql = "SELECT * FROM doctor"
    cur.execute(sql)
    data = cur.fetchall()
    # Adjust column names according to your 'doctor' table structure:
    df = pd.DataFrame(data, columns=["sno", "name", "email", "age", "pwd", "cpwd", "gender", "mobile", "role"])
    df["Action"] = "Action"
    # Drop sensitive columns
    df.drop(["email", "pwd", "cpwd", "gender", "mobile"], axis=1, inplace=True)
    db.close()
    return render_template("viewdoctors.html", row_val=df.values.tolist())

@app.route("/adddoct/<s1>/<s2>/<s3>")
def adddoct(s1="", s2="", s3=""):
    return render_template("adddoctors.html", s1=s1, s2=s2, s3=s3)

@app.route("/updoctors", methods=["POST", "GET"])
def updoctors():
    if request.method == "POST":
        name = request.form["name"]
        age = request.form["age"]
        role = request.form["role"]
        db, cur = getdb()
        sql = "INSERT INTO addoctors (name, age, role) VALUES (%s, %s, %s)"
        values = (name, age, role)
        cur.execute(sql, values)
        db.commit()
        db.close()
        return redirect(url_for('viewdoctors'))

@app.route("/viewpatients")
def viewpatients():
    db, cur = getdb()
    sql = "SELECT * FROM patient"
    cur.execute(sql)
    data = cur.fetchall()
    # Based on your DESC output for patient:
    df = pd.DataFrame(data, columns=["sno", "name", "email", "age", "pwd", "cpwd", "gender", "mobile", "disease"])
    db.close()
    df.drop(["email", "pwd", "cpwd", "gender", "mobile"], axis=1, inplace=True)
    df["Action"] = "Action"
    return render_template("viewpatients.html", row_val=df.values.tolist())

@app.route("/addpatients/<s1>/<s2>/<s3>")
def addpatients(s1="", s2="", s3=""):
    return render_template("addpat.html", s1=s1, s2=s2, s3=s3)

@app.route("/uppat", methods=["POST", "GET"])
def uppat():
    if request.method == "POST":
        name = request.form["name"]
        age = request.form["age"]
        disease = request.form["disease"]
        db, cur = getdb()
        sql = "INSERT INTO adpatients (name, age, disease) VALUES (%s, %s, %s)"
        values = (name, age, disease)
        cur.execute(sql, values)
        db.commit()
        db.close()
        return redirect(url_for('viewpatients'))

@app.route("/viewmedicines")
def viewmedicines():
    db, cur = getdb()
    sql = "SELECT * FROM filesupload"
    cur.execute(sql)
    data = cur.fetchall()
    # Assuming filesupload has columns: sno, files, requeststofiles
    df = pd.DataFrame(data, columns=["sno", "files", "requeststofiles"])
    db.close()
    df.drop(["requeststofiles"], axis=1, inplace=True)
    df["Action"] = "Action"
    return render_template("viewmedicines.html", row_val=df.values.tolist())

@app.route("/addreqtoioh/<s1>")
def addreqtoioh(s1=0):
    db, cur = getdb()
    sql = "UPDATE filesupload SET requeststofiles=%s WHERE sno=%s"
    cur.execute(sql, ("pending", s1))
    db.commit()
    db.close()
    return redirect(url_for('viewmedicines'))

@app.route("/viewses")
def viewses():
    db, cur = getdb()
    sql = "SELECT * FROM filesupload WHERE requeststofiles=%s"
    cur.execute(sql, ("accepted",))
    data = cur.fetchall()
    df = pd.DataFrame(data, columns=["sno", "files", "requeststofiles"])
    db.close()
    df["Action"] = "Action"
    return render_template("viewses.html", row_val=df.values.tolist())

@app.route("/key/<s1>")
def key(s1=0):
    db, cur = getdb()
    sql = "SELECT COUNT(*), AES_DECRYPT(files, %s) FROM filesupload WHERE sno=%s"
    cur.execute(sql, ('rupesh', s1))
    x = cur.fetchone()
    db.close()
    count = x[0]
    if count == 0:
        flash("Invalid Key", "success")
        return redirect(url_for('viewses'))
    else:
        data = x[1]
        if data is not None:
            data = data.decode('utf-8')
        return render_template("key.html", row_val=data)

@app.route("/doctor", methods=["POST", "GET"])
def doctor():
    if request.method == "POST":
        name = request.form["name"]
        email = request.form["email"]
        age = request.form["age"]
        pwd = request.form["pwd"]
        cpwd = request.form["pwd"]
        gender = request.form["gender"]
        mobile = request.form["mobile"]
        role = request.form["role"]
        db, cur = getdb()
        sql = "INSERT INTO doctor (name, email, age, pwd, cpwd, gender, mobile, role) VALUES (%s, %s, %s, %s, %s, %s, %s, %s)"
        values = (name, email, age, pwd, cpwd, gender, mobile, role)
        cur.execute(sql, values)
        db.commit()
        db.close()
        return render_template("doctor.html", ms="success")
    return render_template("doctor.html")

@app.route("/doctorlogin", methods=['POST', 'GET'])
def doctorlogin():
    if request.method == 'POST':
        name = request.form["name"]
        pwd = request.form["pwd"]
        db, cur = getdb()
        sql = "SELECT * FROM doctor WHERE name=%s AND pwd=%s"
        val = (name, pwd)
        cur.execute(sql, val)
        Results = cur.fetchall()
        db.close()
        # Check if any results were returned
        if Results and len(Results) > 0:
            session["doctorloginid"] = Results[0][0]
            session["doctorname"] = Results[0][1]
            return render_template("doctorshome.html", msg="success")
        else:
            return render_template("doctorlogin.html", mfg="not found")
    return render_template("doctorlogin.html")

@app.route("/viewappointments")
def viewappointments():
    try:
        # Use the logged-in doctor's id stored in session
        db, cur = getdb()
        sql = "SELECT * FROM addrequesttodoctor WHERE doctorid=%s"
        cur.execute(sql, (session["doctorloginid"],))
        data = cur.fetchall()
        db.close()
        # Assuming columns: sno, name, age, disease, patientid, doctorid, appointmentdate, status, doctorname
        df = pd.DataFrame(data, columns=["sno", "name", "age", "disease", "patientid", "doctorid", "appointmentdate", "status", "doctorname"])
        if not df.empty:
            session["s1"] = df.iloc[0]["sno"]
            df.drop(["appointmentdate", "status", "doctorname", "doctorid"], axis=1, inplace=True)
            df["Action"] = "Action"
            return render_template("viewappointments.html", row_val=df.values.tolist())
        else:
            msg = "No appointments found"
            return render_template("viewappointments.html", msg=msg)
    except Exception as e:
        msg = "Admin hasn't accepted your appointments"
        return render_template("viewappointments.html", msg=msg)

@app.route("/addappointment", methods=["POST", "GET"])
def addappointment():
    if request.method == "POST":
        date1 = request.form["date"]
        currentDay = datetime.now().strftime('%Y-%m-%d')
        if date1 > currentDay:
            db, cur = getdb()
            sql = "UPDATE addrequesttodoctor SET appointmentdate=%s, status=%s, doctorname=%s WHERE sno=%s"
            cur.execute(sql, (date1, "accepted", session["doctorname"], session["s1"]))
            db.commit()
            db.close()
            flash("Appointment confirmed", "success")
            return redirect(url_for('viewappointments'))
        else:
            flash("Select a future date", "danger")
            return redirect(url_for('viewappointments'))
    return render_template("addappointment.html")

@app.route("/patient", methods=["POST", "GET"])
def patient():
    if request.method == "POST":
        name = request.form["name"]
        email = request.form["email"]
        pwd = request.form["pwd"]
        cpwd = request.form["pwd"]
        age = request.form["age"]
        gender = request.form["gender"]
        mobile = request.form["mobile"]
        disease = request.form["disease"]
        if pwd == cpwd:
            db, cur = getdb()
            sql = "INSERT INTO patient (name, email, age, pwd, cpwd, gender, mobile, disease) VALUES (%s, %s, %s, %s, %s, %s, %s, %s)"
            values = (name, email, age, pwd, cpwd, gender, mobile, disease)
            cur.execute(sql, values)
            db.commit()
            db.close()
            return render_template("patient.html", ms="success")
        else:
            return render_template("patient.html", m1s="Passwords do not match")
    return render_template("patient.html")

@app.route("/patientlogin", methods=['POST', 'GET'])
def patientlogin():
    if request.method == 'POST':
        name = request.form["name"]
        pwd = request.form["pwd"]
        db, cur = getdb()
        sql = "SELECT * FROM patient WHERE name=%s AND pwd=%s"
        val = (name, pwd)
        cur.execute(sql, val)
        Results = cur.fetchall()
        db.close()
        if Results and len(Results) > 0:
            session["patientdisease"] = Results[0][8]
            session["patientname"] = Results[0][1]
            session["patientage"] = Results[0][3]
            session["patientid"] = Results[0][0]
            return render_template("patienthome.html", msg="success")
        else:
            return render_template("patientlogin.html", mfg="not found")
    return render_template("patientlogin.html")

@app.route("/search")
def search():
    return render_template("search.html")

@app.route("/searchback", methods=['POST', 'GET'])
def searchback():
    if request.method == 'POST':
        dtype = request.form['dtype']
        db, cur = getdb()
        sql = "SELECT * FROM addoctors WHERE role LIKE %s"
        cur.execute(sql, ('%' + dtype + '%',))
        data = cur.fetchall()
        db.close()
        df = pd.DataFrame(data, columns=["id", "name", "age", "role"])  # Adjust column names as needed.
        df["Action"] = "Action"
        return render_template("viewaddoctors.html", row_val=df.values.tolist())
    return redirect(url_for('search'))

@app.route("/viewaddoctors")
def viewaddoctors():
    db, cur = getdb()
    sql = "SELECT * FROM addoctors WHERE role LIKE %s"
    cur.execute(sql, (session["patientdisease"] + '%',))
    data = cur.fetchall()
    db.commit()
    db.close()
    df = pd.DataFrame(data, columns=["id", "name", "age", "role"])  # Adjust if needed.
    df["Action"] = "Action"
    return render_template("viewaddoctors.html", row_val=df.values.tolist())

@app.route("/addrequesttodoctor/<s1>/<s2>")
def addrequesttodoctor(s1=0, s2=""):
    d = session.get('patientdisease')
    session['doctorid'] = s1  # This may be redundant if you're using doctorloginid instead.
    db, cur = getdb()
    sql = "INSERT INTO addrequesttodoctor (name, age, disease, doctorid, patientid) VALUES (%s, %s, %s, %s, %s)"
    values = (session["patientname"], s2, d, s1, session["patientid"])
    cur.execute(sql, values)
    db.commit()
    db.close()
    return redirect(url_for('viewaddoctors'))

@app.route("/viewstatus")
def viewstatus():
    db, cur = getdb()
    sql = "SELECT * FROM addrequesttodoctor WHERE status=%s"
    cur.execute(sql, ("accepted",))
    data = cur.fetchall()
    db.commit()
    db.close()
    df = pd.DataFrame(data, columns=["sno", "name", "age", "disease", "patientid", "doctorid", "appointmentdate", "status", "doctorname"])
    df.drop(["disease", "patientid", "age", "doctorid", "sno"], axis=1, inplace=True)
    return render_template("viewstatus.html", row_val=df.values.tolist())

@app.route("/ioh", methods=["POST", "GET"])
def ioh():
    if request.method == "POST":
        name = request.form["name"]
        pwd = request.form["pwd"]
        if name == "IOH" and pwd == "IOH":
            return render_template("iohhome.html", msg="success")
    return render_template("ioh.html")

@app.route("/iohviewpatients")
def iohviewpatients():
    db, cur = getdb()
    sql = "SELECT * FROM adpatients"
    cur.execute(sql)
    data = cur.fetchall()
    db.commit()
    db.close()
    df = pd.DataFrame(data, columns=["sno", "name", "age", "disease"])
    df.drop(["sno", "age"], axis=1, inplace=True)
    return render_template("iohviewpatients.html", row_val=df.values.tolist())

@app.route("/uploadmedicienes", methods=["POST", "GET"])
def uploadmedicienes():
    if request.method == "POST":
        files = request.form["files"]
        dd = "uploadfiles/" + files
        with open(dd, "r") as f:
            data = f.read()
        db, cur = getdb()
        sql = "INSERT INTO filesupload (files) VALUES (AES_ENCRYPT(%s, %s))"
        cur.execute(sql, (data, "rupesh"))
        db.commit()
        db.close()
    return render_template("uploadmedicienes.html")

@app.route("/viewadminrequests")
def viewadminrequests():
    return render_template("viewadminrequests.html")

@app.route("/Viewre")
def Viewre():
    db, cur = getdb()
    sql = "SELECT * FROM filesupload WHERE requeststofiles=%s"
    cur.execute(sql, ("pending",))
    data = cur.fetchall()
    df = pd.DataFrame(data, columns=["sno", "files", "requeststofiles"])
    db.commit()
    db.close()
    return render_template("Viewre.html", row_val=df.values.tolist())

@app.route("/upd/<s1>")
def upd(s1=0):
    db, cur = getdb()
    sql = "UPDATE filesupload SET requeststofiles=%s WHERE sno=%s"
    cur.execute(sql, ("accepted", s1))
    db.commit()
    db.close()
    return redirect(url_for('viewadminrequests'))

if __name__ == "__main__":
    app.run(debug=True)
