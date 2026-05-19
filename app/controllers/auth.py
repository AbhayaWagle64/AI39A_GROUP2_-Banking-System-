from flask import render_template

class AuthController:
    def login(self):
        return render_template("login.html")
    
    def register(self):
        return render_template("register.html")
    
    def home(self):
        return render_template("home.html")
    
    def blog(self):
        return render_template("blog.html")
    
    def contact(self):
        return render_template("contact.html")
    
    def services(self):
        return render_template("services.html")