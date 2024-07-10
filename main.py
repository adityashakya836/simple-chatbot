from bot import BOT
from flask import Flask, render_template, redirect, request, session
from flask_session import Session

app = Flask(__name__, template_folder='templates', static_folder='static')
app.config['SESSION_PERMANENT'] = False
app.config['SESSION_TYPE'] = "filesystem"
Session(app)


@app.route('/', methods = ["GET", "POST"])
def home():
    # if the user not found
    if not session.get("name"):
        return redirect("/login")

    # if user logged in make a session for managing conversation
    message = " "
    if request.method == 'POST':
        query = request.form['query']
        response = BOT(query)
        message = response.generate_output(session, session.get("name")).replace('\n','<br>')
    return render_template('home.html',message = message)

@app.route("/login", methods = ['POST', 'GET'])
def login():
    if request.method == "POST":
        session["name"] = request.form.get("name")
        return redirect("/")
    return render_template("login.html")

@app.route("/logout")
def logout():
    session["name"] = None
    session.pop(session.get("name"), None)
    return redirect("/")

if __name__ == '__main__':
    app.run(debug=True)

