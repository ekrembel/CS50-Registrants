from flask import Flask, render_template, request, redirect
from cs50 import SQL
# from flask_session_plus import Session

app = Flask(__name__)
# app.config["SESSION_PERMANENT"] = False
# app.config["SESSION_TYPE"] = "filesystem"

db = SQL("sqlite:///registrants.db")

@app.route('/')
def index():
    rows = db.execute("SELECT * FROM registrants;")
    return render_template("index.html", rows=rows)

@app.route('/register', methods=["GET", "POST"])
def register():
    if request.method == "GET":
        return render_template("register.html")
    else:
        name = request.form.get("name")
        rows = db.execute("SELECT * FROM registrants;")
        if not name:
            return render_template("apology.html", message="You must provide a name.")
        email = request.form.get("email")
        if not email:
            return render_template("apology.html", message="You must provide an email address.")
        for row in rows:
            if row["email"] == email:
                return render_template("already.html", name=name)    
        db.execute("INSERT INTO registrants (name, email) VALUES (:name, :email);", name=name, email=email)
        return redirect('/')
@app.route('/delete', methods=["GET", "POST"])
def delete():

    if request.method == "GET":
        return render_template("delete.html")

    else: 
        email = request.form.get("email")
        rows = db.execute("SELECT * FROM registrants;")
        for row in rows:
            if row['email'] == email:
                db.execute("DELETE FROM registrants WHERE email=:email;", email=email)
                return render_template("successful.html", title="Successful", message="Sorry to see you go!")                
                
        return render_template("successful.html", title="Unsuccessful", message="Please try again.")            
        




