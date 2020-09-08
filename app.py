from flask import Flask, render_template

app = Flask(__name__)


@app.route('/')
def login_page():
    return render_template('login_page.html')

@app.route('/signup')
def signup_page():
    return render_template('signup_page.html')

if __name__ == '__main__':
    app.run(debug=True)
