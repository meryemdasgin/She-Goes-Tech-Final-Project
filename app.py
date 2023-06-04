from flask import Flask, render_template, redirect, url_for, request
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///sqlite.db'
db = SQLAlchemy(app)


#create models
class TestTool(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100))
    type = db.Column(db.String(100))
    severity = db.Column(db.String(100))
    assignee = db.Column(db.String(100))
    description = db.Column(db.String(500))
    complete = db.Column(db.Boolean, default=False)

@app.route('/')
def index():
    todo_list = TestTool.query.all()
    total_todo = TestTool.query.count()
    completed_todo = TestTool.query.filter_by(complete=True).count()
    uncompleted_todo = total_todo - completed_todo

    return render_template('dashboard/index.html', **locals())

@app.route('/add', methods=['POST'])
def add():
    title = request.form.get('title')
    type = request.form.get('type')
    severity = request.form.get('severity')
    assignee = request.form.get('assignee')
    description = request.form.get('description')

    new_testtool = TestTool(title=title, type=type, severity=severity, assignee=assignee, description=description, complete=False)
    db.session.add(new_testtool)
    db.session.commit()
    return redirect(url_for('index'))

@app.route('/delete/<int:id>')
def delete(id):
    todo = TestTool.query.filter_by(id=id).first()
    db.session.delete(todo)
    db.session.commit()
    return redirect(url_for('index'))

@app.route('/update/<int:id>')
def update(id):
    todo = TestTool.query.filter_by(id=id).first()
    todo.complete = not todo.complete
    db.session.commit()
    return redirect(url_for('index'))

@app.route('/about')
def about():
    return render_template('dashboard/about.html')

# Creating db after new db connection.
# app.app_context().push()
# db.create_all()

if __name__ == '__main__':
    
    app.run(debug=True)