from stud_model import *
from flask import render_template,request

@app.route('/')
def welcome_page():
    return render_template('index.html')

@app.route('/add-stud',methods=['GET'])
@app.route('/stud-save',methods=['GET','POST'])
def add_student():
    if request.method == 'POST':
        formdata = request.form
        print(formdata)

        errors = []
        if not formdata.get('sname'):
            errors.append("Student Name Cannot be Empty")
        if not formdata.get('semail'):
            errors.append("Student Email Cannot be Empty")
        if not formdata.get('sfees'):
            errors.append("Student fees Cannot be Empty")
        else:
            try:
                s_fees = float(formdata.get('sfees'))
                if s_fees<=0:
                    errors.append('Invalid Fees')
            except:
                errors.append('Invalid Fees')

        if errors:
            return render_template('addstud.html', smessage=errors)

        student = Student(rollno=formdata.get('rno'),s_name=formdata.get('sname'),s_email=formdata.get('semail'),
        s_fees=s_fees,s_dept=formdata.get('sdept'))
        db.session.add(student)
        db.session.commit()
        return render_template('addstud.html', message="Student Added Successfully...")

    return render_template('addstud.html')

@app.route('/stud-delete/<int:rno>')
def delete_student(rno):
    student = Student.query.filter_by(rollno=rno).first()
    db.session.delete(student)
    db.session.commit()
    return render_template('liststud.html', slist=Student.query.all())


def search_student():
    pass


@app.route('/stud-edit/<int:rno>')
@app.route('/stud-edit/',methods = ['POST'])
def update_student(rno=None):
    if request.method == 'GET':
        student = Student.query.filter_by(rollno=rno).first()
        return render_template('updatestud.html',record = student)
    else:
        formdata = request.form
        rno = formdata.get('rno')
        student = Student.query.filter_by(rollno=rno).first()
        student.s_name = formdata.get('sname')
        student.s_email = formdata.get('semail')
        student.s_fees = formdata.get('sfees')
        student.s_dept = formdata.get('sdept')
        db.session.commit()
        return render_template('liststud.html', slist=Student.query.all())



@app.route('/stud-list')
def list_student():
    return render_template('liststud.html',slist=Student.query.all())
SORT_ROLL = True
SORT_NAME = True
SORT_FEE = True
SORT_DEPT = True
@app.route('/sort/<by>')
def sort_student(by):
    global SORT_ROLL
    global SORT_NAME
    global SORT_FEE
    global SORT_DEPT

    student = Student.query.all()
    student = list(student)

    if by == 'roll':
        student.sort(key=lambda item: item.rollno, reverse=SORT_ROLL)
        SORT_ROLL = False if SORT_ROLL else True

    elif by == 'name':
        student.sort(key=lambda item : item.s_name,reverse=SORT_NAME)
        SORT_NAME = False if SORT_NAME else True
    elif by == 'fee':
        student.sort(key=lambda item : item.s_fees,reverse=SORT_FEE)
        SORT_FEE = False if SORT_FEE else True
    elif by =='dept':
        student.sort(key=lambda item: item.s_dept, reverse=SORT_DEPT)
        SORT_DEPT = False if SORT_DEPT else True
    else:
        student.sort(key=lambda item: item.rollno)

    return render_template('liststud.html', slist=student)


@app.route('/stud-fee-range',methods = ['POST'])
def stud_fees_range():
    formdata = request.form
    start_range = float(formdata.get('ffee'))
    end_range = float(formdata.get('sfee'))
    message = ''
    if start_range<=0.0 or end_range<=0.0:
        message = "Invalid Fees"
    elif start_range<end_range:
        student= Student.query.filter(Student.s_fees>=start_range,Student.s_fees<=end_range).all()
        if student:
            return render_template('liststud.html', studs = student,slist = Student.query.all())
        message = "No Record with Given Range..!"

    return render_template('liststud.html',message = message,slist = Student.query.all())

