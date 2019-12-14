# from flask import Flask, render_template, redirect, url_for, request

from app2 import app
from app2.forms import LoginForm
from flask import render_template, redirect, flash


@app.route('/')
def hello_world():
    return 'Hello World!'


if __name__ == '__main__':
    app.run()


@app.route('/index')
def index():
    user = {'username': 'Miguel'}
    return render_template('index.html', title='Microblg')





@app.route('/your/webroot/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        flash('Login requested for user {}, remember_me={}'.format(
            form.username.data, form.remember_me.data))
        return redirect('/index')
    return render_template('login.html', title='Sign In', form=form)

"""
@app.route('/your/webroot/spell_check')
def hello_world():
    return 'Hello World!'


@app.route('/your/webroot/register', methods=['GET','POST'])
def registration():
    error = None
    if request.method == 'POST':
        if request.form['Username'] != 'admin' or request.form['password'] != 'admin':
            error = "Invalid Credentials. Please Try Again."
        else:
            return redirect(url_for('spell_check'))
    return render_template('login.html', error=error)
@app.route('/login', methods=['GET', 'POST'])


"""