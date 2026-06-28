import os
from dotenv import load_dotenv
from flask import request, Flask, render_template, session, redirect, url_for, flash
import pymysql
import pandas as pd
from datetime import datetime
import secrets
from werkzeug.security import generate_password_hash, check_password_hash 


app = Flask(__name__)

# ── SECURE SECRET KEY ──────────────────────────────────────────
app.config['SECRET_KEY'] = os.getenv('FLASK_SECRET_KEY', secrets.token_hex(32))

# ── DB CONNECTION (FROM .env) ──────────────────────────────────
def getdb():
    try:
        db = pymysql.connect(
            host=os.getenv('DB_HOST', 'localhost'),
            user=os.getenv('DB_USER', 'root'),
            password=os.getenv('DB_PASSWORD', ''),
            db=os.getenv('DB_NAME', 'multisource'),
            port=int(os.getenv('DB_PORT', 3306))
        )
        cur = db.cursor()
        return db, cur
    except pymysql.Error as e:
        print(f"Database Connection Error: {e}")
        flash("Database connection failed. Check credentials.", "danger")
        return None, None


# ── HOME ───────────────────────────────────────────────────
@app.route("/")
def index():
    return render_template("index.html")


# ── ADMIN ──────────────────────────────────────────────────
@app.route("/admin", methods=["POST", "GET"])
def admin():
    if request.method == "POST":
        username = request.form.get("name", "").strip()
        password = request.form.get("pwd", "").strip()

        db, cur = getdb()
        if not db:
            flash("Database connection failed.", "danger")
            return render_template("admin.html")

        try:
            # Look up admin by username
            cur.execute("SELECT id, password FROM admin WHERE username=%s", (username,))
            result = cur.fetchone()

            if result and check_password_hash(result[1], password):
                session["admin"] = True
                session["admin_username"] = username
                flash("Admin login successful!", "success")
                return render_template("adminhome.html")
            else:
                flash("Invalid admin credentials.", "danger")
        except Exception as e:
            flash(f"Login error: {str(e)}", "danger")
        finally:
            if db and db.open:
                db.close()

    return render_template("admin.html")


# ── ADMIN LOGOUT ───────────────────────────────────────────
@app.route("/logout")
def logout():
    session.pop("admin", None)
    session.pop("doctorloginid", None)
    session.pop("patientid", None)
    session.pop("ioh", None)
    flash("Logged out successfully!", "success")
    return redirect(url_for('index'))


# ── DOCTORS MANAGEMENT ─────────────────────────────────────
@app.route("/viewdoctors")
def viewdoctors():
    db, cur = getdb()
    if not db:
        return redirect(url_for('index'))
    
    try:
        cur.execute("SELECT id, name, age, role FROM addoctors")
        data = cur.fetchall()

        if not data:
            return render_template("viewdoctors.html", row_val=[])
        
        df = pd.DataFrame(data, columns=["id", "name", "age", "role"])
        df["Action"] = "Edit"
        return render_template("viewdoctors.html", row_val=df.values.tolist())
    except Exception as e:
        flash(f"Error loading doctors: {str(e)}", "danger")
        return redirect(url_for('index'))
    finally:
        if db and db.open:
            db.close()


@app.route("/adddoct/<int:s1>/<int:s2>/<s3>", methods=["GET", "POST"])
def adddoct(s1, s2, s3):
    if request.method == "POST":
        name = request.form.get("name", "").strip()
        age = request.form.get("age", "").strip()
        role = request.form.get("role", "").strip()
        
        db, cur = getdb()
        if not db:
            flash("Database connection failed.", "danger")
            return redirect(url_for('viewdoctors'))
        
        try:
            cur.execute(
                "INSERT INTO addoctors (name, age, role) VALUES (%s, %s, %s)",
                (name, age, role)
            )
            db.commit()
            flash("Doctor added successfully!", "success")
            return redirect(url_for('viewdoctors'))
        except Exception as e:
            flash(f"Error adding doctor: {str(e)}", "danger")
            return redirect(url_for('viewdoctors'))
        finally:
            if db and db.open:
                db.close()
    
    return render_template("adddoctors.html", s1=s1, s2=s2, s3=s3)


@app.route("/updoctors", methods=["POST", "GET"])
def updoctors():
    if request.method == "POST":
        name = request.form.get("name", "").strip()
        age = request.form.get("age", "").strip()
        role = request.form.get("role", "").strip()
        
        db, cur = getdb()
        if not db:
            flash("Database error.", "danger")
            return redirect(url_for('viewdoctors'))
        
        try:
            cur.execute(
                "INSERT INTO addoctors (name, age, role) VALUES (%s, %s, %s)",
                (name, age, role)
            )
            db.commit()
            flash("Doctor saved!", "success")
        except Exception as e:
            flash(f"Error: {str(e)}", "danger")
        finally:
            if db and db.open:
                db.close()
    
    return redirect(url_for('viewdoctors'))


# ── PATIENTS MANAGEMENT ────────────────────────────────────
@app.route("/viewpatients")
def viewpatients():
    db, cur = getdb()
    if not db:
        return redirect(url_for('index'))
    
    try:
        cur.execute("SELECT sno, name, age, disease FROM adpatients")
        data = cur.fetchall()

        if not data:
            return render_template("viewpatients.html", row_val=[])
        
        df = pd.DataFrame(data, columns=["sno", "name", "age", "disease"])
        df["Action"] = "Edit"
        return render_template("viewpatients.html", row_val=df.values.tolist())
    except Exception as e:
        flash(f"Error loading patients: {str(e)}", "danger")
        return redirect(url_for('index'))
    finally:
        if db and db.open:
            db.close()


@app.route("/addpatients/<s1>/<int:s2>/<s3>", methods=["GET", "POST"])
def addpatients(s1, s2, s3):
    if request.method == "POST":
        name = request.form.get("name", "").strip()
        age = request.form.get("age", "").strip()
        disease = request.form.get("disease", "").strip()
        
        db, cur = getdb()
        if not db:
            flash("Database connection failed.", "danger")
            return redirect(url_for('viewpatients'))
        
        try:
            cur.execute(
                "INSERT INTO adpatients (name, age, disease) VALUES (%s, %s, %s)",
                (name, age, disease)
            )
            db.commit()
            flash("Patient added successfully!", "success")
            return redirect(url_for('viewpatients'))
        except Exception as e:
            flash(f"Error adding patient: {str(e)}", "danger")
            return redirect(url_for('viewpatients'))
        finally:
            if db and db.open:
                db.close()
    
    return render_template("addpat.html", s1=s1, s2=s2, s3=s3)


@app.route("/uppat", methods=["POST", "GET"])
def uppat():
    if request.method == "POST":
        name = request.form.get("name", "").strip()
        age = request.form.get("age", "").strip()
        disease = request.form.get("disease", "").strip()
        
        db, cur = getdb()
        if not db:
            flash("Database error.", "danger")
            return redirect(url_for('viewpatients'))
        
        try:
            cur.execute(
                "INSERT INTO adpatients (name, age, disease) VALUES (%s, %s, %s)",
                (name, age, disease)
            )
            db.commit()
            flash("Patient saved!", "success")
        except Exception as e:
            flash(f"Error: {str(e)}", "danger")
        finally:
            if db and db.open:
                db.close()
    
    return redirect(url_for('viewpatients'))


# ── MEDICINES MANAGEMENT ──────────────────────────────────
@app.route("/viewmedicines")
def viewmedicines():
    db, cur = getdb()
    if not db:
        return redirect(url_for('index'))
    
    try:
        cur.execute("SELECT sno FROM filesupload")
        data = cur.fetchall()
        return render_template("viewmedicines.html", row_val=[[x[0], "Encrypted File", "Request"] for x in data])
    except Exception as e:
        flash(f"Error: {str(e)}", "danger")
        return redirect(url_for('index'))
    finally:
        if db and db.open:
            db.close()


@app.route("/addreqtoioh/<int:s1>")
def addreqtoioh(s1):
    db, cur = getdb()
    if not db:
        flash("Database error.", "danger")
        return redirect(url_for('viewmedicines'))
    
    try:
        cur.execute("UPDATE filesupload SET requeststofiles=%s WHERE sno=%s", ("pending", s1))
        db.commit()
        flash("Request sent to IOH.", "success")
    except Exception as e:
        flash(f"Error: {str(e)}", "danger")
    finally:
        if db and db.open:
            db.close()
    
    return redirect(url_for('viewmedicines'))


@app.route("/viewses")
def viewses():
    db, cur = getdb()
    if not db:
        return redirect(url_for('index'))
    
    try:
        cur.execute("SELECT sno FROM filesupload WHERE requeststofiles=%s", ("accepted",))
        data = cur.fetchall()
        return render_template("viewses.html", row_val=[[x[0], "Encrypted File", "Accepted", "Decrypt"] for x in data])
    except Exception as e:
        flash(f"Error: {str(e)}", "danger")
        return redirect(url_for('index'))
    finally:
        if db and db.open:
            db.close()


@app.route("/key/<int:s1>")
def key(s1):
    db, cur = getdb()
    if not db:
        return redirect(url_for('viewses'))
    
    try:
        cur.execute("SELECT AES_DECRYPT(files, %s) FROM filesupload WHERE sno=%s", ('rupesh', s1))
        row = cur.fetchone()

        if not row or row[0] is None:
            flash("File not found or decryption failed.", "danger")
            return redirect(url_for('viewses'))
        
        data = row[0].decode('utf-8') if isinstance(row[0], bytes) else row[0]
        return render_template("key.html", row_val=data)
    except Exception as e:
        flash(f"Error decrypting file: {str(e)}", "danger")
        return redirect(url_for('viewses'))
    finally:
        if db and db.open:
            db.close()


@app.route("/Viewre")
def Viewre():
    db, cur = getdb()
    if not db:
        return redirect(url_for('index'))
    
    try:
        cur.execute("SELECT sno FROM filesupload WHERE requeststofiles=%s", ("pending",))
        data = cur.fetchall()
        return render_template("Viewre.html", row_val=[[x[0], "Encrypted File", "Approve"] for x in data])
    except Exception as e:
        flash(f"Error: {str(e)}", "danger")
        return redirect(url_for('index'))
    finally:
        if db and db.open:
            db.close()


@app.route("/upd/<int:s1>")
def upd(s1):
    db, cur = getdb()
    if not db:
        flash("Database error.", "danger")
        return redirect(url_for('Viewre'))
    
    try:
        cur.execute("UPDATE filesupload SET requeststofiles=%s WHERE sno=%s", ("accepted", s1))
        db.commit()
        flash("Request approved.", "success")
    except Exception as e:
        flash(f"Error: {str(e)}", "danger")
    finally:
        if db and db.open:
            db.close()
    
    return redirect(url_for('Viewre'))


# ── DOCTOR ROUTES ──────────────────────────────────────────
@app.route("/doctor", methods=["POST", "GET"])
def doctor():
    if request.method == "POST":
        name = request.form.get("name", "").strip()
        email = request.form.get("email", "").strip()
        age = request.form.get("age", "").strip()
        pwd = request.form.get("pwd", "").strip()
        cpwd = request.form.get("cpwd", "").strip()
        gender = request.form.get("gender", "").strip()
        mobile = request.form.get("mobile", "").strip()
        role = request.form.get("role", "").strip()
        
        if pwd != cpwd:
            flash("Passwords do not match.", "danger")
            return render_template("doctor.html")
        
        db, cur = getdb()
        if not db:
            flash("Database connection failed.", "danger")
            return render_template("doctor.html")
        
        try:
            hashed_pwd = generate_password_hash(pwd)
            cur.execute(
                "INSERT INTO doctor (name, email, age, pwd, cpwd, gender, mobile, role) VALUES (%s, %s, %s, %s, %s, %s, %s, %s)",
                (name, email, age, hashed_pwd, hashed_pwd, gender, mobile, role)
            )
            db.commit()
            flash("Registration successful! Please login.", "success")
            return redirect(url_for('doctorlogin'))
        except pymysql.IntegrityError:
            flash("Email already registered.", "danger")
            return render_template("doctor.html")
        except Exception as e:
            flash(f"Registration error: {str(e)}", "danger")
            return render_template("doctor.html")
        finally:
            if db and db.open:
                db.close()
    
    return render_template("doctor.html")


@app.route("/doctorlogin", methods=["POST", "GET"])
def doctorlogin():
    if request.method == "POST":
        name = request.form.get("name", "").strip()
        pwd = request.form.get("pwd", "").strip()
        
        db, cur = getdb()
        if not db:
            flash("Database error.", "danger")
            return render_template("doctorlogin.html")
        
        try:
            cur.execute("SELECT sno, name, pwd FROM doctor WHERE name=%s", (name,))
            result = cur.fetchone()

            if result and check_password_hash(result[2], pwd):
                session["doctorloginid"] = result[0]
                session["doctorname"] = result[1]
                flash(f"Welcome, {result[1]}!", "success")
                return render_template("doctorshome.html")
            
            flash("Invalid name or password.", "danger")
        except Exception as e:
            flash(f"Login error: {str(e)}", "danger")
        finally:
            if db and db.open:
                db.close()
    
    return render_template("doctorlogin.html")


@app.route("/viewappointments")
def viewappointments():
    if "doctorloginid" not in session:
        flash("Please login first.", "warning")
        return redirect(url_for('doctorlogin'))
    
    db, cur = getdb()
    if not db:
        return redirect(url_for('doctorlogin'))
    
    try:
        cur.execute(
            "SELECT sno, name, age, disease, patientid FROM addrequesttodoctor WHERE doctorid=%s",
            (session["doctorloginid"],)
        )
        data = cur.fetchall()

        if not data:
            return render_template("viewappointments.html", msg="No appointments found.", row_val=[])
        
        if data:
            session["s1"] = data[0][0]
        
        df = pd.DataFrame(data, columns=["sno", "name", "age", "disease", "patientid"])
        df["Action"] = "Set Date"
        return render_template("viewappointments.html", row_val=df.values.tolist())
    except Exception as e:
        flash(f"Error: {str(e)}", "danger")
        return redirect(url_for('doctorlogin'))
    finally:
        if db and db.open:
            db.close()


@app.route("/addappointment", methods=["POST", "GET"])
def addappointment():
    if request.method == "POST":
        date1 = request.form.get("date", "").strip()
        currentDay = datetime.now().strftime('%Y-%m-%d')
        
        if date1 <= currentDay:
            flash("Please select a future date.", "danger")
            return redirect(url_for('viewappointments'))
        
        db, cur = getdb()
        if not db:
            flash("Database error.", "danger")
            return redirect(url_for('viewappointments'))
        
        try:
            cur.execute(
                "UPDATE addrequesttodoctor SET appointmentdate=%s, status=%s, doctorname=%s WHERE sno=%s",
                (date1, "accepted", session.get("doctorname"), session.get("s1"))
            )
            db.commit()
            flash("Appointment confirmed!", "success")
            return redirect(url_for('viewappointments'))
        except Exception as e:
            flash(f"Error: {str(e)}", "danger")
            return redirect(url_for('viewappointments'))
        finally:
            if db and db.open:
                db.close()
    
    return render_template("addappointment.html")


# ── PATIENT ROUTES ─────────────────────────────────────────
@app.route("/patient", methods=["POST", "GET"])
def patient():
    if request.method == "POST":
        name = request.form.get("name", "").strip()
        email = request.form.get("email", "").strip()
        pwd = request.form.get("pwd", "").strip()
        cpwd = request.form.get("cpwd", "").strip()
        age = request.form.get("age", "").strip()
        gender = request.form.get("gender", "").strip()
        mobile = request.form.get("mobile", "").strip()
        disease = request.form.get("disease", "").strip()
        
        if pwd != cpwd:
            flash("Passwords do not match.", "danger")
            return render_template("patient.html")
        
        db, cur = getdb()
        if not db:
            flash("Database connection failed.", "danger")
            return render_template("patient.html")
        
        try:
            hashed_pwd = generate_password_hash(pwd)
            cur.execute(
                "INSERT INTO patient (name, email, age, pwd, cpwd, gender, mobile, disease) VALUES (%s, %s, %s, %s, %s, %s, %s, %s)",
                (name, email, age, hashed_pwd, hashed_pwd, gender, mobile, disease)
            )
            db.commit()
            flash("Registration successful! Please login.", "success")
            return redirect(url_for('patientlogin'))
        except pymysql.IntegrityError:
            flash("Email already registered.", "danger")
            return render_template("patient.html")
        except Exception as e:
            flash(f"Registration error: {str(e)}", "danger")
            return render_template("patient.html")
        finally:
            if db and db.open:
                db.close()
    
    return render_template("patient.html")


@app.route("/patientlogin", methods=["POST", "GET"])
def patientlogin():
    if request.method == "POST":
        name = request.form.get("name", "").strip()
        pwd = request.form.get("pwd", "").strip()
        
        db, cur = getdb()
        if not db:
            flash("Database error.", "danger")
            return render_template("patientlogin.html")
        
        try:
            cur.execute("SELECT sno, name, age, disease, pwd FROM patient WHERE name=%s", (name,))
            result = cur.fetchone()

            if result and check_password_hash(result[4], pwd):
                session["patientid"] = result[0]
                session["patientname"] = result[1]
                session["patientage"] = result[2]
                session["patientdisease"] = result[3]
                flash(f"Welcome, {result[1]}!", "success")
                return render_template("patienthome.html")
            
            flash("Invalid name or password.", "danger")
        except Exception as e:
            flash(f"Login error: {str(e)}", "danger")
        finally:
            if db and db.open:
                db.close()
    
    return render_template("patientlogin.html")


@app.route("/search", methods=["GET", "POST"])
def search():
    if request.method == "POST":
        dtype = request.form.get("dtype", "").strip()
        
        db, cur = getdb()
        if not db:
            return render_template("search.html")
        
        try:
            cur.execute("SELECT id, name, age, role FROM addoctors WHERE role LIKE %s", ('%' + dtype + '%',))
            data = cur.fetchall()

            if not data:
                flash("No doctors found for this specialization.", "info")
                return render_template("search.html")
            
            df = pd.DataFrame(data, columns=["id", "name", "age", "role"])
            df["Action"] = "Book"
            return render_template("viewaddoctors.html", row_val=df.values.tolist())
        except Exception as e:
            flash(f"Search error: {str(e)}", "danger")
            return render_template("search.html")
        finally:
            if db and db.open:
                db.close()
    
    return render_template("search.html")


@app.route("/viewaddoctors")
def viewaddoctors():
    if "patientdisease" not in session:
        flash("Please login first.", "warning")
        return redirect(url_for('patientlogin'))
    
    db, cur = getdb()
    if not db:
        return redirect(url_for('patientlogin'))
    
    try:
        cur.execute("SELECT id, name, age, role FROM addoctors WHERE role LIKE %s", (session["patientdisease"] + '%',))
        data = cur.fetchall()

        if not data:
            return render_template("viewaddoctors.html", row_val=[])
        
        df = pd.DataFrame(data, columns=["id", "name", "age", "role"])
        df["Action"] = "Book"
        return render_template("viewaddoctors.html", row_val=df.values.tolist())
    except Exception as e:
        flash(f"Error: {str(e)}", "danger")
        return redirect(url_for('patientlogin'))
    finally:
        if db and db.open:
            db.close()


@app.route("/addrequesttodoctor/<int:s1>/<int:s2>")
def addrequesttodoctor(s1, s2):
    if "patientid" not in session:
        flash("Please login first.", "warning")
        return redirect(url_for('patientlogin'))
    
    db, cur = getdb()
    if not db:
        flash("Database error.", "danger")
        return redirect(url_for('viewaddoctors'))
    
    try:
        cur.execute(
            "INSERT INTO addrequesttodoctor (name, age, disease, doctorid, patientid) VALUES (%s, %s, %s, %s, %s)",
            (session["patientname"], s2, session["patientdisease"], s1, session["patientid"])
        )
        db.commit()
        flash("Appointment request sent to doctor!", "success")
        return redirect(url_for('viewaddoctors'))
    except Exception as e:
        flash(f"Error: {str(e)}", "danger")
        return redirect(url_for('viewaddoctors'))
    finally:
        if db and db.open:
            db.close()


@app.route("/viewstatus")
def viewstatus():
    db, cur = getdb()
    if not db:
        return redirect(url_for('index'))
    
    try:
        cur.execute("SELECT name, appointmentdate, status, doctorname FROM addrequesttodoctor WHERE status=%s", ("accepted",))
        data = cur.fetchall()

        if not data:
            return render_template("viewstatus.html", row_val=[])
        
        df = pd.DataFrame(data, columns=["name", "date", "status", "doctor"])
        return render_template("viewstatus.html", row_val=df.values.tolist())
    except Exception as e:
        flash(f"Error: {str(e)}", "danger")
        return redirect(url_for('index'))
    finally:
        if db and db.open:
            db.close()


# ── IOH ROUTES ─────────────────────────────────────────────
@app.route("/ioh", methods=["POST", "GET"])
def ioh():
    if request.method == "POST":
        name = request.form.get("name", "").strip()
        pwd = request.form.get("pwd", "").strip()
        
        if name == "IOH" and pwd == "IOH":
            session["ioh"] = True
            flash("IOH login successful!", "success")
            return render_template("iohhome.html")
        
        flash("Invalid IOH credentials.", "danger")
    
    return render_template("ioh.html")


@app.route("/iohviewpatients")
def iohviewpatients():
    db, cur = getdb()
    if not db:
        return redirect(url_for('ioh'))
    
    try:
        cur.execute("SELECT name, disease FROM adpatients")
        data = cur.fetchall()

        if not data:
            return render_template("iohviewpatients.html", row_val=[])
        
        df = pd.DataFrame(data, columns=["name", "disease"])
        return render_template("iohviewpatients.html", row_val=df.values.tolist())
    except Exception as e:
        flash(f"Error: {str(e)}", "danger")
        return redirect(url_for('ioh'))
    finally:
        if db and db.open:
            db.close()


@app.route("/uploadmedicienes", methods=["POST", "GET"])
def uploadmedicienes():
    if request.method == "POST":
        filename = request.form.get("files", "").strip()
        
        # Check if file exists
        filepath = os.path.join("uploadfiles", filename)
        if not os.path.exists(filepath):
            flash(f"File '{filename}' not found in uploadfiles/ folder.", "danger")
            return render_template("uploadmedicienes.html")
        
        db, cur = getdb()
        if not db:
            flash("Database error.", "danger")
            return render_template("uploadmedicienes.html")
        
        try:
            with open(filepath, "r", encoding='utf-8') as f:
                data = f.read()
            
            cur.execute(
                "INSERT INTO filesupload (files) VALUES (AES_ENCRYPT(%s, %s))",
                (data, "rupesh")
            )
            db.commit()
            flash("File uploaded and encrypted successfully!", "success")
        except FileNotFoundError:
            flash(f"File '{filename}' not found.", "danger")
        except Exception as e:
            flash(f"Upload error: {str(e)}", "danger")
        finally:
            if db and db.open:
                db.close()
    
    return render_template("uploadmedicienes.html")


# ── ERROR HANDLERS ─────────────────────────────────────────
@app.errorhandler(404)
def not_found(error):
    return render_template("index.html"), 404

@app.errorhandler(500)
def server_error(error):
    flash("Internal server error. Please try again.", "danger")
    return render_template("index.html"), 500


if __name__ == "__main__":
    app.run(
        debug=os.getenv('FLASK_DEBUG', 'False') == 'True',
        host='localhost',
        port=5000
    )