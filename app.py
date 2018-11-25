from flask import Flask, render_template, request, redirect, url_for
import mlab
from all_functions import verify_code, verify_email
from all_classes import Question, Qbank, User, Updateqbank, Deletedqbank, Deletedquestion, Verifyuser, Exam
from random import *

app = Flask(__name__)
mlab.connect()

@app.route('/student/score_print/<user_id>', methods = ['GET', 'POST'])
def score_print(user_id):
    user = User.objects().with_id(user_id)
    if request.method == 'GET':
        return render_template('score_print.html', scores = [])
    if request.method == 'POST':
        form = request.form
        student_id = form['student_id'].upper()
        class_id = form['class_id'].upper()
        exams = Exam.objects(class_id = class_id, student_id= student_id)
        scores = []
        for exam in exams:
            student_id = exam['student_id']
            student_name = exam['student_name']
            exam_questions = exam['exam_questions']
            answer = exam['answer']
            count_right = 0
            for i in range(len(answer)):
                q = exam_questions[i]
                ra = q['right_answer'].upper()
                a = answer[i].upper()
                if a == ra:
                    count_right += 1
            if len(exam_questions) == 0:
                score = float("{0:.2f}".format(0))
            else:
                score = float("{0:.2f}".format(10*count_right/len(exam_questions)))
            student_score = {
                'student_id': student_id,
                'student_name': student_name,
                'class_id': class_id,
                'score': score
            }
            scores.append(student_score)
        return render_template('score_print.html', scores = scores)


@app.route('/teacher/exam_print/<user_id>', methods = ['GET', 'POST'])
def exam_print(user_id):
    user = User.objects().with_id(user_id)
    if request.method == 'GET':
        return render_template('exam_print.html', exams_questions = [], answers = [])
    if request.method == 'POST':
        form = request.form
        teacher_id = form['teacher_id']
        student_id = form['student_id'].upper()
        class_id = form['class_id'].upper()
        exams = Exam.objects(class_id = class_id, teacher_id= teacher_id, student_id= student_id)
        exams_questions = []
        answers = []
        for exam in exams:
            exam_questions = exam['exam_questions']
            answer = exam['answer']
            print(answer)
            exams_questions.append(exam_questions)
            answers.append(answer)
        return render_template('exam_print.html', exams_questions = exams_questions, answers = answers)

@app.route('/teacher/scores_export/<user_id>', methods = ['GET', 'POST'])
def scores_export(user_id):
    user = User.objects().with_id(user_id)
    if request.method == 'GET':
        return render_template('scores_export.html', scores = [])
    if request.method == 'POST':
        form = request.form
        class_id = form['class_id'].upper()
        qbank_code = form['qbank_code']
        exams = Exam.objects(class_id = class_id, qbank_code = qbank_code)
        scores = []
        for exam in exams:
            student_id = exam['student_id']
            student_name = exam['student_name']
            exam_questions = exam['exam_questions']
            answer = exam['answer']
            count_right = 0
            for i in range(len(answer)):
                q = exam_questions[i]
                ra = q['right_answer'].upper()
                a = answer[i].upper()
                if a == ra:
                    count_right += 1
            if len(exam_questions) == 0:
                score = float("{0:.2f}".format(0))
            else:
                score = float("{0:.2f}".format(10*count_right/len(exam_questions)))
            student_score = {
                'student_id': student_id,
                'student_name': student_name,
                'class_id': class_id,
                'score': score
            }
            scores.append(student_score)
        return render_template('scores_export.html', scores = scores)

@app.route('/teacher/qbanks/<user_id>', methods = ['GET', 'POST'])
def qbanks(user_id):
    user = User.objects().with_id(user_id)
    qbanks = user['qbanks']
    return render_template('qbanks.html', user = user, qbanks = qbanks)

@app.route('/teacher/create_qbank/<user_id>', methods = ['GET', 'POST'])
def create_qbank(user_id):
    user = User.objects().with_id(user_id)
    qbanks = Qbank.objects()
    if request.method == 'GET':
        return render_template('qbank_code.html', error = "")
    if request.method == 'POST':
        form = request.form
        qbank_code = form['qbank_code'].upper()
        qbank_list = []
        for qb in qbanks:
            qbank_list.append(qb['qbank_code'])
        if qbank_code in qbank_list:
            error = "Question bank code is already existed, please choose another Question bank code"
            return render_template('qbank_code.html', error = error)
        else:
            new_qbank = Qbank(
                qbank_code = qbank_code, 
                qbank_easy = [],
                qbank_medium = [],
                qbank_hard = [],
            )
            new_qbank.save()
            user.update(push__qbanks = new_qbank)
            return redirect(url_for('qbank_code', user_id = user_id, qbank_code = qbank_code))

@app.route('/teacher/qbanks/<user_id>/<qbank_code>/save')
def save_qbank(user_id, qbank_code):
    user = User.objects().with_id(user_id)
    qbanks = user['qbanks']
    qbank = Qbank.objects(qbank_code=qbank_code).first()
    user.update(pull__qbanks = qbank)
    user.update(push__qbanks = qbank)
    return render_template('qbanks.html', user = user, qbanks = qbanks)

@app.route('/teacher/qbanks/<user_id>/<qbank_code>/new', methods = ['GET', 'POST']) #them cau hoi cho qbank moi
def qbank_code(user_id, qbank_code):
    user = User.objects().with_id(user_id)
    qbanks = user['qbanks']
    qbank = Qbank.objects(qbank_code=qbank_code).first()
    qlist=[]
    for q in qbank['qbank_easy']:
        qlist.append(q['question'])
    for q in qbank['qbank_medium']:
        qlist.append(q['question'])
    for q in qbank['qbank_hard']:
        qlist.append(q['question'])
    if request.method == 'GET':
        return render_template('qbank.html', user_id = user_id, qbank_code = qbank_code, error = "")
    if request.method == 'POST':
        form = request.form
        question_type = form['question_type']
        question = form['question']
        optiona = form['optiona']
        optionb = form['optionb']
        optionc = form['optionc']
        optiond = form['optiond']
        right_answer = form.get('right_answer')
        if question in qlist:
            return render_template('qbank.html', user_id = user_id, qbank_code = qbank_code, error = "Đã tồn tại câu hỏi, làm ơn nhập câu hỏi tiếp theo")
        else:
            new_question = Question(
                question_type = question_type,
                question = question,
                optiona = optiona,
                optionb = optionb,
                optionc = optionc,
                optiond = optiond,
                right_answer = right_answer,
            )
            new_question.save()
            if question_type == "Dễ":
                qbank.update(push__qbank_easy = new_question)
            elif question_type == "Trung bình":
                qbank.update(push__qbank_medium = new_question)
            elif question_type == "Khó":
                qbank.update(push__qbank_hard = new_question)
            return redirect(url_for('qbank_code', user_id = user_id, qbank_code = qbank_code))

@app.route('/teacher/qbanks/<user_id>/<qbank_code>/update', methods = ['GET', 'POST'])
def update_qbank(user_id, qbank_code):
    user = User.objects().with_id(user_id)
    qbank = Qbank.objects(qbank_code=qbank_code).first()
    return render_template('update_qbank.html', user = user, qbank = qbank)

@app.route('/teacher/qbanks/<user_id>/<qbank_code>/update_question/<question_id>', methods = ['GET', 'POST'])
def update_question(user_id, qbank_code, question_id):
    user = User.objects().with_id(user_id)
    old_question = Question.objects().with_id(question_id)
    qbank = Qbank.objects(qbank_code=qbank_code).first()
    if request.method == 'GET':
        return render_template('update_question.html', question = old_question)
    if request.method == 'POST':
        form = request.form
        question_type = form['question_type']
        question = form['question']
        optiona = form['optiona']
        optionb = form['optionb']
        optionc = form['optionc']
        optiond = form['optiond']
        right_answer = form.get('right_answer')
        old_question.update(
            set__question_type = question_type,
            set__question = question,
            set__optiona = optiona,
            set__optionb = optionb,
            set__optionc = optionc,
            set__optiond = optiond,
            set__right_answer = right_answer,
        )
        user = User.objects().with_id(user_id)
        old_question = Question.objects().with_id(question_id)
        qbank = Qbank.objects(qbank_code=qbank_code).first()
        return render_template('update_qbank.html', user = user, qbank = qbank)

@app.route('/teacher/qbanks/<user_id>/<qbank_code>/delete_question/<question_id>')
def del_question(user_id, qbank_code, question_id):
    user = User.objects().with_id(user_id)
    old_question = Question.objects().with_id(question_id)
    qbank = Qbank.objects(qbank_code=qbank_code).first()
    old_qbank_code = qbank_code
    question_type = old_question['question_type']
    question = old_question['question']
    optiona = old_question['optiona']
    optionb = old_question['optionb']
    optionc = old_question['optionc']
    optiond = old_question['optiond']
    right_answer = old_question['right_answer']
    deletedquestion = Deletedquestion(
        old_qbank_code = old_qbank_code,
        question_type = question_type,
        question = question,
        optiona = optiona,
        optionb = optionb,
        optionc = optionc,
        optiond = optiond,
        right_answer = right_answer,
    )
    if question_type == "Dễ":
        qbank.update(pull__qbank_easy = old_question)
    elif question_type == "Trung bình":
        qbank.update(pull__qbank_medium = old_question)
    elif question_type == "Khó":
        qbank.update(pull__qbank_hard = old_question)
    deletedquestion.save()
    old_question.delete()
    user = User.objects().with_id(user_id)
    old_question = Question.objects().with_id(question_id)
    qbank = Qbank.objects(qbank_code=qbank_code).first()
    return render_template('update_qbank.html', user = user, qbank = qbank)

@app.route('/teacher/qbanks/<user_id>/<qbank_code>/add_question', methods = ['GET', 'POST']) #them cau hoi cho qbank moi
def add_question(user_id, qbank_code):
    user = User.objects().with_id(user_id)
    qbanks = user['qbanks']
    qbank = Qbank.objects(qbank_code=qbank_code).first()
    qlist=[]
    for q in qbank['qbank_easy']:
        qlist.append(q['question'])
    for q in qbank['qbank_medium']:
        qlist.append(q['question'])
    for q in qbank['qbank_hard']:
        qlist.append(q['question'])
    if request.method == 'GET':
        return render_template('qbank.html', user_id = user_id, qbank_code = qbank_code, error = "")
    if request.method == 'POST':
        form = request.form
        question_type = form['question_type']
        question = form['question']
        optiona = form['optiona']
        optionb = form['optionb']
        optionc = form['optionc']
        optiond = form['optiond']
        right_answer = form.get('right_answer')
        if question in qlist:
            return render_template('qbank.html', user_id = user_id, qbank_code = qbank_code, error = "Đã tồn tại câu hỏi, làm ơn nhập câu hỏi tiếp theo")
        else:
            new_question = Question(
                question_type = question_type,
                question = question,
                optiona = optiona,
                optionb = optionb,
                optionc = optionc,
                optiond = optiond,
                right_answer = right_answer,
            )
            new_question.save()
            if question_type == "Dễ":
                qbank.update(push__qbank_easy = new_question)
            elif question_type == "Trung bình":
                qbank.update(push__qbank_medium = new_question)
            elif question_type == "Khó":
                qbank.update(push__qbank_hard = new_question)
            return redirect(url_for('qbank_code', user_id = user_id, qbank_code = qbank_code))

@app.route('/teacher/qbanks/<user_id>/<qbank_code>/delete')
def delete_qbank(user_id, qbank_code):
    user = User.objects().with_id(user_id)
    old_qbank = Qbank.objects(qbank_code=qbank_code).first()
    deletedqbank = Deletedqbank(
        user_id = user_id,
        qbank_code = qbank_code, 
        qbank_easy = old_qbank['qbank_easy'],
        qbank_medium = old_qbank['qbank_medium'],
        qbank_hard = old_qbank['qbank_hard'],
    )
    deletedqbank.save()
    user.update(pull__qbanks = old_qbank)
    old_qbank.delete()
    user = User.objects().with_id(user_id)
    qbanks = user['qbanks']
    return render_template('qbanks.html', user = user, qbanks = qbanks)

@app.route('/welcome/<user_id>')
def welcome(user_id):
    user = User.objects().with_id(user_id)
    return render_template('home.html', user = user)
    
@app.route('/login', methods = ['GET', 'POST'])
def login():
    if request.method == 'GET':
        return render_template('login.html', error = "")
    elif request.method == 'POST':
        form = request.form
        user_id = form['user_id']
        password = form['password']
        all_users = User.objects()
        error = None
        for u in all_users:
            if u["user_id"] == user_id and u['password'] == password:
                return redirect(url_for('welcome', user_id = u['id']))
            else:
                error = 'Invalid Credentials. Please try again.'
        return render_template('login.html', error = error)

@app.route('/verifyuser/<verifyuser_id>', methods = ['GET', 'POST'])
def verifyuser(verifyuser_id):
    verify_user = Verifyuser.objects().with_id(verifyuser_id)
    if request.method == 'GET':
        return render_template('verify_user.html', verify_user = verify_user)
    elif request.method == 'POST':
        form = request.form
        code = form['code'].upper()
        if code == verify_user['code']:
            user_id = verify_user['user_id']
            full_name = verify_user['full_name']
            email = verify_user['email']
            password = verify_user['password']
            new_user = User(user_id = user_id, full_name = full_name, email = email, password = password)
            new_user.save()
            verify_user.delete()
            return redirect(url_for('login'))
        else:
            return render_template('verify_user.html', verify_user = verify_user)

@app.route('/signup', methods = ['GET', 'POST'])
def signup():
    if request.method == 'GET':
        return render_template('signup.html', error = "")
    elif request.method == 'POST':
        form = request.form
        user_id = form['user_id']
        full_name = form['full_name']
        email = form['email']
        password = form['password']
        code = verify_code()
        all_users = User.objects()
        user_id_list = []
        for u in all_users:
            user_id_list.append(u['user_id'])
        if user_id in user_id_list:
            error = "User ID is already existed, please choose another User ID"
            return render_template('signup.html', error = error)
        else:
            new_verify_user = Verifyuser(user_id = user_id, full_name = full_name, email = email, password = password, code = code)
            new_verify_user.save()        
            verify_email(email, full_name, code)
            return redirect(url_for('verifyuser', verifyuser_id = new_verify_user['id']))


@app.route('/')
def homepage():
    return redirect('/login')

@app.route('/student/<user_id>/exam/student_info', methods = ['GET', 'POST'])
def exam_student_info(user_id):
    user = User.objects().with_id(user_id)
    if request.method == 'GET':
        return render_template('student_info.html')
    if request.method == 'POST':
        form = request.form
        student_user_id = user_id
        student_name = form['student_name']
        class_id= form['class_id'].upper()
        student_id= form['student_id'].upper()
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
        new_exam.save()
        exam = Exam.objects(student_user_id= user_id, student_name= student_name, class_id= class_id, student_id= student_id).first()
        exam_id = exam['id']
        print('student_name')
        return redirect(url_for('exam_teacher_info', exam_id = exam_id, user_id = user_id))

@app.route('/student/<user_id>/exam/<exam_id>/teacher_info', methods = ['GET', 'POST'])
def exam_teacher_info(user_id, exam_id):
    exam = Exam.objects().with_id(exam_id)
    print(exam['id'])
    if request.method == 'GET':
        return render_template('teacher_info.html')
    if request.method == 'POST':
        form = request.form
        teacher_id = form['teacher_id']
        qbank_code = form['qbank_code'].upper()
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
        exam.reload()
        print(exam['id'])
        qbank_code = exam['qbank_code']
        print(qbank_code)
        qbank = Qbank.objects(qbank_code = qbank_code).first()
        qbank_easy = qbank['qbank_easy']
        qbank_medium = qbank['qbank_medium']
        qbank_hard = qbank['qbank_hard']
        n_easy = exam['n_easy']
        n_medium = exam['n_medium']
        n_hard = exam['n_hard']
        len_easy = len(qbank_easy)
        len_medium = len(qbank_medium)
        len_hard = len(qbank_hard)
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
        exam.update(set__exam_questions = exam_questions) 
        return redirect(url_for('exam_waiting', user_id = user_id, exam_id= exam_id))


@app.route('/student/<user_id>/exam/<exam_id>/exam_waiting', methods = ['GET', 'POST'])
def exam_waiting(user_id, exam_id):
    if request.method == 'GET':
        return render_template('waiting.html', user_id = user_id, exam_id= exam_id)
    if request.method == 'POST':
        return redirect(url_for('exam_doing', user_id = user_id, exam_id= exam_id))


@app.route('/student/<user_id>/exam/<exam_id>/doing', methods = ['GET', 'POST'])
def exam_doing(user_id, exam_id):
    exam = Exam.objects().with_id(exam_id)
    qbank_code = exam['qbank_code']
    time = exam['time']
    qbank = Qbank.objects(qbank_code = qbank_code).first()
    exam_questions = exam['exam_questions']
    if request.method == 'GET':
        return render_template('student_exam.html', exam_questions = exam_questions, time = time)
    if request.method == 'POST':
        form = request.form
        answer_list = []
        for i in range(len(exam_questions)):
            i = i + 1
            answer = form[str(i)]
            answer_list.append(answer)
        exam.update(set__answer = answer_list)
        return redirect(url_for('welcome', user_id = user_id))

if __name__ == "__main__":
    app.run(debug = True)