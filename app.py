from flask import Flask, request, render_template, redirect, url_for
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///attendance.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False  # Avoids warning
db = SQLAlchemy(app)

class Attendance(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    student_id = db.Column(db.String(50), nullable=False)
    name = db.Column(db.String(100), nullable=False)
    date = db.Column(db.String(10), nullable=False)
    status = db.Column(db.String(10), nullable=False)

@app.route('/', methods=['GET'])
def index():
    return render_template('index.html')

@app.route('/submit', methods=['POST'])
def submit():
    try:
        student_id = request.form['student_id']
        name = request.form['name']
        date = request.form['date']
        status = request.form['status']

        # Validate input
        if not student_id or not name or not date or not status:
            return "All fields are required", 400

        # Save to database
        new_record = Attendance(student_id=student_id, name=name, date=date, status=status)
        db.session.add(new_record)
        db.session.commit()

        return redirect(url_for('index'))

    except Exception as e:
        return f"An error occurred: {str(e)}", 500

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True)
