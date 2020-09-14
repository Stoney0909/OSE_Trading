from flask import Flask, render_template

app = Flask(__name__)

@app.route('/')
def login_page():
    return render_template('Login_page.html')

@app.route('/Signup')
def signup_page():
    return render_template('Signup_page.html')

@app.route('/ForgetPassword')
def forgetPassword_page():
    return render_template('ForgetPassword_page.html')

@app.route('/Home')
def home_page():
    return render_template('Home_page.html')

if __name__ == '__main__':
    app.run(debug=True)
