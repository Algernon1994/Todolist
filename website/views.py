from flask import Blueprint, redirect, render_template, url_for, request, flash
from .models import Todo
from.import db

my_view = Blueprint("my_view", __name__)


my_view.secret_key = "todokey"


@my_view.route("/")
def home():
    todo_list = Todo.query.all()
    return render_template("index.html",todo_list=todo_list)

@my_view.route("/add", methods=["POST"])
def add():
    task = request.form.get("task")
    if task:
        try:
            new_todo = Todo( task=task )
            db.session.add(new_todo)
            db.session.commit()
            flash("Flash added successfully.", "success")
        except Exception as e:
            flash("Error: Unable to add tast. Task may already exist.", "error")
    else:
        flash("Error: Task cannot be empty.", "error")#lower case is the 'class' of flash in css
    return redirect(url_for("my_view.home"))

@my_view.route("/update/<int:todo_id>", methods=["POST"])
def update(todo_id):
    todo = Todo.query.get_or_404(todo_id)
    todo.complete = not todo.complete
    db.session.commit()
    return redirect(url_for("my_view.home"))

@my_view.route("/delete/<int:todo_id>")
def delete(todo_id):
    todo = Todo.query.get_or_404(todo_id)
    #todo = Todo.query.filter_by(id=todo_id).first()
    db.session.delete(todo)
    db.session.commit()
    return redirect(url_for("my_view.home"))

@my_view.route("/edit/<int:todo_id>", methods=["GET", "POST"])
def edit(todo_id):
    todo = Todo.query.get_or_404(todo_id)

    if request.method == "POST":
        new_task = request.form.get("task")
        todo.task = new_task
        db.session.commit()
        return redirect(url_for("my_view.home"))

    return render_template("edit.html", todo=todo)
