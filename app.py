from flask import Flask, render_template, request, redirect, url_for

app = Flask(__name__)

# Home Page
@app.route("/")
def home():
    return redirect(url_for("register"))

# Register Page
@app.route("/register", methods=["GET", "POST"])
def register():

    if request.method == "POST":

        fullname = request.form.get("fullname")
        email = request.form.get("email")
        phone = request.form.get("phone")

        print(fullname, email, phone)

        return redirect(url_for("register"))

    return render_template("register.html")

# Terms & Conditions Page
@app.route("/terms")
def terms():
    return render_template("terms.html")

# Login Page
@app.route("/login")
def login():
    return "Login Page"

if __name__ == "__main__":
    app.run(debug=True)