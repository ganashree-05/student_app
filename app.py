import json
from flask import Flask, render_template, request, redirect, url_for, jsonify

app = Flask(__name__)

# File to store student data
DATA_FILE = 'students.json'

# Load data from file
def load_students():
    try:
        with open(DATA_FILE, 'r') as file:
            return json.load(file)
    except FileNotFoundError:
        return {}

# Save data to file
def save_students():
    with open(DATA_FILE, 'w') as file:
        json.dump(students, file)

# Initialize students dictionary
students = load_students()

@app.route('/')
def index():
    return render_template('index.html', students=students.values())

@app.route('/addstudent', methods=['GET', 'POST'])
def add_student():
    if request.method == 'POST':
        # Collect the data from the form
        name = request.form['name']
        usn = request.form['usn']
        age = request.form['age']
        phone_number = request.form['phone_number']
        department = request.form['department']
        college = request.form['college']
        grade = request.form['grade']
        email = request.form['email']
        dob = request.form['dob']
        permanent_address = request.form['permanent_address']

        # Check if the student with the same USN already exists
        if usn in students:
            return jsonify({"message": "Student with this USN already exists."}), 400

        # Add the student data to the students dictionary
        students[usn] = {
            "name": name,
            "usn": usn,
            "age": age,
            "phone_number": phone_number,
            "department": department,
            "college": college,
            "grade": grade,
            "email": email,
            "dob": dob,
            "permanent_address": permanent_address
        }

        save_students()  # Save the updated data
        return redirect(url_for('index'))
    return render_template('addstudent.html')

@app.route('/editstudent/<usn>', methods=['GET', 'POST'])
def edit_student(usn):
    student = students.get(usn)
    if not student:
        return jsonify({"message": "Student not found."}), 404

    if request.method == 'POST':
        # Collect the updated data from the form
        student['name'] = request.form['name']
        student['usn'] = request.form['usn']
        student['age'] = request.form['age']
        student['phone_number'] = request.form['phone_number']
        student['department'] = request.form['department']
        student['college'] = request.form['college']
        student['grade'] = request.form['grade']
        student['email'] = request.form['email']
        student['dob'] = request.form['dob']
        student['permanent_address'] = request.form['permanent_address']

        save_students()  # Save the updated data
        return redirect(url_for('index'))

    return render_template('editstudent.html', student=student)

@app.route('/delete_student/<usn>', methods=['GET'])
def delete_student(usn):
    if usn in students:
        del students[usn]
        save_students()  # Save the updated data
        return redirect(url_for('index'))
    return jsonify({"message": "Student not found."}), 404

if __name__ == '__main__':
    app.run(debug=True)
