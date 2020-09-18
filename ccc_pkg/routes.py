from flask import render_template, flash, redirect, url_for, request
from ccc_pkg import app, db
from ccc_pkg.forms import LoginForm, RegistrationForm
from flask_login import current_user, login_user, logout_user, login_required
from werkzeug.urls import url_parse
from ccc_pkg.models import User

@app.route('/')
@app.route('/index')
def index():
    user = {'username': 'Asia'}
    posts = [
        {
            'author': {'username': 'Asia'},
            'body': 'Color palette that helps me not have a mental breakdown...'
        },
        {
            'author': {'username': 'Bobby'},
            'body': 'I have no idea what I should be doing!'
        }
    ]
    return render_template('index.html', title="Code Concoctions", user=user, posts=posts)

@app.route('/signup', methods=['GET', 'POST'])
def signup():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    form = RegistrationForm()
    if form.validate_on_submit():
        user = User(username=form.username.data,
        email=form.email.data)
        user.set_password(form.password.data)
        db.session.add(user)
        db.session.commit()
        flash('Thanks for signing up for Code Concoctions!')
        return redirect(url_for('login'))
    return render_template('signup.html', title="Sign Up", form=form)

@app.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('profile'))
    form=LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user is None or not user.check_password(form.password.data):
            flash('Invalid username or password')
            return redirect(url_for('login'))
        login_user(user, remember=form.remember_me.data)
        next_page = request.args.get('next')
        if not next_page or url_parse(next_page).netloc != '':
            next_page = url_for('index')
            return redirect(next_page)
    return render_template('login.html', title="Log In", form=form)

@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('index'))

@app.route('/user/<username>')
@login_required
def user(username):
    user = User.query.filter_by(username=username).first_or_404()
    posts = [
        {'author': user, 'body': 'Test post #1'},
        {'author': user, 'body': 'Test post #2'}
    ]
    return render_template('profile.html', title="Profile", user=user, posts=posts)

@app.route('/todo')
@login_required
def todo():
    return render_template('todo.html', title="To-Do Listing")