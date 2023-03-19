from datetime import datetime, timedelta
import os
from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
from flask_wtf import FlaskForm
from wtforms import validators
from wtforms.fields import StringField, BooleanField, DateTimeField, IntegerField, SubmitField


app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///db.sqlite'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SECRET_KEY'] = os.environ.get("SECRET_KEY") or "MilanchicTopchik"
db = SQLAlchemy(app)


class Task(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100))
    completed = db.Column(db.Boolean)
    start_date_time = db.Column(db.DateTime)
    end_date_time = db.Column(db.DateTime)


class TaskForm(FlaskForm):
    title = StringField("title")
    submit = SubmitField("create")


@app.route("/", methods=['GET', 'POST'])
def home():
    tasks_list = Task.query.all()
    task_form = TaskForm()
    if task_form.validate_on_submit():
        st=request.form.get("start")
        st_python = datetime.now().replace(second=0, microsecond=0) if st == '' else datetime(month=int(st[5:7]), day=int(st[8:10]), year=int(st[0:4]), hour=int(st[11:13]), minute=int(st[14:16]), second=0, microsecond=0)
        ed=request.form.get("end")
        ed_python = datetime.now().replace(second=0, microsecond=0) + timedelta(hours=1) if ed == '' else datetime(month=int(ed[5:7]), day=int(ed[8:10]), year=int(ed[0:4]), hour=int(ed[11:13]), minute=int(ed[14:16]), second=0, microsecond=0)
        if st_python > ed_python:
            return render_template("base.html", tasks_list=tasks_list, task_form=task_form, validation_error='invalid dates')
        new_task = Task(title=task_form.title.data, completed=False, start_date_time=st_python, end_date_time=ed_python)
        db.session.add(new_task)
        db.session.commit()
        task_form = TaskForm()
        tasks_list = Task.query.all()
        return render_template("base.html", tasks_list=tasks_list, task_form=task_form, validation_error='')
    return render_template("base.html", tasks_list=tasks_list, task_form=task_form, validation_error='')

@app.route("/about")
def about():
    return render_template("about.html", title='about')

@app.route("/add", methods=["POST"])
def add():
    title = TaskForm()
    if title.validate_on_submit():
        new_task = Task(title=title.title, completed=False, start_date_time=title.start, end_date_time=title.end)
        db.session.add(new_task)
        db.session.commit()
    return redirect(url_for("home"))

@app.route("/update/<int:task_id>")
def update(task_id):
    task = Task.query.filter_by(id=task_id).first()
    task.completed = not task.completed
    db.session.commit()
    return redirect(url_for("home"))

@app.route("/delete/<int:task_id>")
def delete(task_id):
    task = Task.query.filter_by(id=task_id).first()
    db.session.delete(task)
    db.session.commit()
    return redirect(url_for("home"))

# if __name__ == "__main__":
#    db.create_all()
#    app.run(debug=True)
