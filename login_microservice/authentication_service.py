from flask import Flask, request, redirect, render_template, url_for
from pymongo import MongoClient
from uuid import uuid1

mongoserver_uri = f"mongodb://127.0.0.1:27017"
                    
client = MongoClient(mongoserver_uri)

db = client["project_management"].get_collection("users")

app = Flask(__name__)

@app.route('/', methods=['GET'])
def root():
    return redirect('/login')

@app.route('/register', methods=['GET'])
def register_get():
    return render_template('register.html')

@app.route('/register', methods=['POST'])
def register_post():
    if client.admin.command("replSetGetStatus")["votingMembersCount"] < 3:
        return render_template("register.html", user_exists="Database is currently in read-only mode")
    if (len(list(db.find({"login": request.form["login"]}))) != 0):
        return render_template("register.html", user_exists="User Already exists")
    user = {"login": request.form["login"], "password": request.form["pass"], "uuid": uuid1().int % (2^64) }
    db.insert_one(user)
    
    return redirect("/login")

@app.route('/login', methods=['GET'])
def login_get():
    return render_template('login.html')

@app.route('/login', methods=['POST'])
def login_post():
    if (len(list(db.find({"login":request.form["login"], "password":request.form["pass"]}))) == 0):
        return render_template('login.html', incorrect="Incorrect username or password")
    
    cursor = db.find_one({"login":request.form["login"], "password":request.form["pass"]})

    return redirect(f"http://127.0.0.1:5000?uuid={cursor['uuid']}")

if __name__ == "__main__":
    app.run(debug=True, port=5001)
