# from flask import Flask, render_template, redirect, url_for, request
import os

from app2 import app, db
from app2.forms import LoginForm, RegForm, SpellCheckForm, HistoryForm
from flask import render_template, redirect, flash, url_for, request
from subprocess import Popen, PIPE
from flask_login import current_user, login_user
from app2.models import User, SpellQueries
from pylint.checkers import spelling
from werkzeug.urls import url_parse


@app.route('/')
def hello_world():
    return 'Hello World!'


if __name__ == '__main__':
    app.run()


@app.route('/index')
def index():
    return render_template('index.html', title='Microblg')


@app.route('/history', methods=['GET', 'POST'])
def history():
    if not current_user.is_authenticated:
        redirect(url_for('login'))
    form = HistoryForm()
    if request.method == 'POST':
        spelling_queries = form.gethistory()
        spelling_queries
        return render_template('history.html',)
    return render_template('history.html', title='History search', form=form)

@app.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('spell_check'))
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.uname.data).first()
        if not (not (user is None) and user.check_password(form.pword.data)):
            flash('Invalid Username or password')
            form.result.data = 'Incorrect'
            return redirect(url_for('login'))
        if not (not (user is None) and user.check_2fa(form.twofa.data)):
            flash('Invalid 2FA')
            form.result.data = "Two-Factor failure"
            return redirect(url_for('login'))
        form.result.data = "Success"
        login_user(user, remember=form.remember_me.data)
        # next_page = request.args.get('next')
        # if not next_page or url_parse(next_page).netloc != '':
        #    next_page = url_for('spell_check')

        return redirect(url_for('index'))
    return render_template('login.html', title='Sign In', form=form)


@app.route('/register', methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('spell_check'))
    form = RegForm()
    if form.validate_on_submit():
        user = User(username=form.uname.data)
        user.set_password(form.pword.data)
        user.set_2fa(form.twofa.data)
        db.session.add(user)
        db.session.commit()
        form.success.data = "Registration Success"
        flash(form.success.data)
        return redirect(url_for('login'))
    form.success.data = "Registration failure"
    flash(form.success.data)
    return render_template('register.html', title='Register', form=form)


@app.route('/spell_check',  methods=['GET', 'POST'])
def spell_check():
    error = None
    if not current_user.is_authenticated:
        return redirect(url_for('login'))
    form = SpellCheckForm()
    query = SpellQueries(user_id=User.get_id(current_user), query=form.textout)
    if request.method == 'POST':

        dir = os.getcwd()
        f = open("infile", "w+")
        f.write(form.inputtext.data)
        f.close()
        form.textout.data = form.inputtext.data
        proc = Popen(['./a.out', "infile", './wordlist.txt'], cwd=dir, stdout=PIPE)
        outdata, error = proc.communicate()
        form.misspelled.data = outdata.decode("utf-8").rstrip()
    return render_template('spell_check.html', error=error, form=form)
