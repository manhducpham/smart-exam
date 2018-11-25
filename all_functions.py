from gmail import GMail, Message
from random import choice, randint

def verify_code():
    alphabetical = 'abcdefghijklmnopqrstuvwxyz123456789'
    code = ''
    for i in range(8):
        rancha = choice(alphabetical).upper()
        code += rancha
    return code
    
def verify_email(reveive_email, name, code):
    mail = GMail("smartexam.c4e22", "Sm@rt123456")
    body = '''
    <div>
    <div>Dear {0},</div>
    <div>You have just signed up for Smart-Exam. Well done!</div>
    <div>Would you mind just validating that this is really your email address?</div>
    <div>Here is the verify code: {1}</div>
    <div>For additional help, please feel free to contact us via smartexam.c4e22@gmail.com.</div>
    </div>
    '''.format(name, code)

    msg = Message("Smart-Exam confirmation email", to = reveive_email, html = body)
    mail.send(msg)