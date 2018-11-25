from flask import Flask, render_template, request, redirect, url_for
import mlab
from all_functions import verify_code, verify_email
from all_classes import Question, Qbank, User, Updateqbank, Deletedqbank, Deletedquestion, Verifyuser, Exam
from random import *

app = Flask(__name__)
mlab.connect()

user_id = '5bf85436d7bca08988dc9cb2'

@app.route('/student/<user_id>/exam/student_info', methods = ['GET', 'POST'])
def exam_student_info(user_id):
    user = User.objects().with_id(user_id)
    print('1')
    if request.method == 'GET':
        print('1.5')
        return render_template('student_info.html')
    elif request.method == 'POST':
        form = request.form
        student_user_id = user_id
        student_name = form['student_name']
        class_id= form['class_id']
        student_id= form['student_id']
        print('2')
        new_exam = Exam(
            student_user_id= user_id,
            student_name= student_name,
            class_id= class_id,
            student_id= student_id,
            teacher_id = "",
            qbank_code = "",
            n_easy = 0,
            n_medium = 0,
            n_hard = 0,
            time = 0,
            exam_questions = [],
            answer = [],
        )
        print('3')
        # class_id = form['class_id']
        new_exam.save()
        print('student_name')
        return redirect(url_for('exam_teacher_info', user_id = user_id, class_id = class_id))

@app.route('/student/<user_id>/exam/<class_id>/teacher_info', methods = ['GET', 'POST'])
def exam_teacher_info(user_id, class_id):
    exam = Exam.objects(student_user_id = user_id, class_id = class_id).first()
    print(6)
    if request.method == 'GET':
        print(4)
        return render_template('teacher_info.html')
    elif request.method == 'POST':
        form = request.form
        teacher_id = form['teacher_id']
        qbank_code = form['qbank_code']
        n_easy = int(form['n_easy'])
        n_medium = int(form['n_medium'])
        n_hard = int(form['n_hard'])
        time = int(form['time'])
        exam.update(
            set__teacher_id = teacher_id,
            set__qbank_code = qbank_code,
            set__n_easy = n_easy,
            set__n_medium = n_medium,
            set__n_hard = n_hard,
            set__time = time,
        )
        print(5)
        return redirect(url_for('exam_waiting', user_id = user_id, class_id= class_id))


@app.route('/student/<user_id>/exam/<class_id>/exam_waiting', methods = ['GET', 'POST'])
def exam_waiting(user_id, class_id):
    exam = Exam.objects(student_user_id = user_id, class_id = class_id).first()
    print(exam['qbank_code'])
    qbank_code = exam['qbank_code']
    qbank = Qbank.objects(qbank_code = qbank_code).first()
    print(qbank)
    print(qbank['qbank_easy'])
    if request.method == 'GET':
        print(31)
        qbank_easy = qbank['qbank_easy']
        qbank_medium = qbank['qbank_medium']
        qbank_hard = qbank['qbank_hard']
        n_easy = exam['n_easy']
        n_medium = exam['n_medium']
        n_hard = exam['n_hard']
        len_easy = len(qbank_easy)
        len_medium = len(qbank_medium)
        len_hard = len(qbank_hard)
        print(len_easy)
        choose_easy = sample(range(len_easy), n_easy)
        choose_medium = sample(range(len_medium), n_medium)
        choose_hard = sample(range(len_hard), n_hard)
        exam_questions = []
        for i in choose_easy:
            q = qbank_easy[i]
            exam_questions.append(q)
        for i in choose_medium:
            q = qbank_medium[i]
            exam_questions.append(q)
        for i in choose_hard:
            q = qbank_hard[i]
            exam_questions.append(q)
        return render_template('waiting.html', user_id = user_id, class_id= class_id)
    elif request.method == 'POST':
        print(10)
        # qbank_code = exam['qbank_code']
        # qbank = Qbank.objects(qbank_code = qbank_code).first()
        # qbank_easy = qbank['qbank_easy']
        # qbank_medium = qbank['qbank_medium']
        # qbank_hard = qbank['qbank_hard']
        # n_easy = exam['n_easy']
        # n_medium = exam['n_medium']
        # n_hard = exam['n_hard']
        # len_easy = len(qbank_easy)
        # len_medium = len(qbank_medium)
        # len_hard = len(qbank_hard)
        # print(len_easy)
        # choose_easy = sample(range(len_easy), n_easy)
        # choose_medium = sample(range(len_medium), n_medium)
        # choose_hard = sample(range(len_hard), n_hard)
        # exam_questions = []
        # for i in choose_easy:
        #     q = qbank_easy[i]
        #     exam_questions.append(q)
        # for i in choose_medium:
        #     q = qbank_medium[i]
        #     exam_questions.append(q)
        # for i in choose_hard:
        #     q = qbank_hard[i]
        #     exam_questions.append(q)
        # print(exam_questions)
        exam.update(set__exam_questions = exam_questions) 
        print(4)  
    return redirect(url_for('exam_doing', user_id = user_id, class_id= class_id))


@app.route('/student/<user_id>/exam/<class_id>/doing', methods = ['GET', 'POST'])
def exam_doing(user_id, class_id):
    print(2)
    exam = Exam.objects(student_user_id = user_id, class_id = class_id).first()
    exam_questions = exam['exam_questions']
    if request.method == 'GET':
        print('done')
        return render_template('student_exam.html')
    elif request.method == 'POST':
        form = request.form
        return 'abc'

if __name__ == "__main__":
    app.run(debug = True)