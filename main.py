from flask import Flask, request, redirect
import os
import jinja2

template_dir = os.path.join(os.path.dirname(__file__), 'templates')
jinja_env = jinja2.Environment(loader = jinja2.FileSystemLoader(template_dir), autoescape=True)

app = Flask(__name__)
app.config['DEBUG'] = True

@app.route("/")
def index():
    template = jinja_env.get_template('signup_form.html')
    return template.render()

@app.route("/", methods=['POST'])
def validate():
    username = request.form['username']
    password = request.form['password']
    verify_pw = request.form['verify_pw']
    email = request.form['email']

    username_error = ''
    password_error = ''
    verify_error = ''
    email_error = '' 

    if not username:
        username_error = 'Please enter a username'
    if not password:
        password_error = 'Please enter a password'
    if not verify_pw:
        verify_error = 'Please retype your password'

    if len(username) < 3 or len(username) > 20 or ' ' in username:
        username_error = 'Please enter a valid username'
    if len(password) < 3 or len(password) > 20 or ' ' in password:
        password_error = "Please enter a valid password"
        password = ''
    if password != verify_pw:
        verify_error = 'Passwords do not match'
        verify_pw = ''

    if not username_error and not password_error and not verify_error:
        return redirect("/welcome?username={0}".format(username))
    else:
        template = jinja_env.get_template('signup_form.html')
        return template.render(username_error=username_error, password_error=password_error,
        verify_error=verify_error)



@app.route("/welcome")
def welcome():
    username = request.args.get('username')
    template = jinja_env.get_template('welcome.html')
    return template.render(username=username)
    

app.run()