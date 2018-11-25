from mongoengine import Document, StringField, ListField, DictField, IntField, ReferenceField, FloatField

class Question(Document):
    question_type = StringField()
    question = StringField()
    optiona = StringField()
    optionb = StringField()
    optionc = StringField()
    optiond = StringField()
    right_answer = StringField()

class Qbank(Document):
    qbank_code = StringField()
    qbank_easy = ListField(ReferenceField(Question))
    qbank_medium = ListField(ReferenceField(Question))
    qbank_hard = ListField(ReferenceField(Question))

class User(Document):
    user_id = StringField()
    full_name = StringField()
    email = StringField()
    password = StringField()
    qbanks = ListField(ReferenceField(Qbank))

class Updateqbank(Document):
    old_qbank_id = StringField()
    old_n_easy = IntField()
    old_n_medium = IntField()
    old_n_hard = IntField()

class Deletedquestion(Document):
    old_qbank_code = StringField()
    question_type = StringField()
    question = StringField()
    optiona = StringField()
    optionb = StringField()
    optionc = StringField()
    optiond = StringField()
    right_answer = StringField()

class Deletedqbank(Document):
    user_id = StringField()
    qbank_code = StringField()
    qbank_easy = ListField(ReferenceField(Question))
    qbank_medium = ListField(ReferenceField(Question))
    qbank_hard = ListField(ReferenceField(Question))

class Verifyuser(Document):
    user_id = StringField()
    full_name = StringField()
    email = StringField()
    password = StringField()
    code = StringField(default = None)

class Score(Document):
    class_id = StringField()
    qbank_code = StringField()
    student_id = StringField()
    student_name = StringField()
    score = FloatField()

class Exam(Document):
    student_user_id = StringField()
    student_name = StringField()
    class_id = StringField()
    student_id = StringField()
    teacher_id = StringField()
    qbank_code = StringField()
    n_easy = IntField()
    n_medium = IntField()
    n_hard = IntField()
    time = IntField()
    exam_questions = ListField()
    answer = ListField()