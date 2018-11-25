import mongoengine

#mongodb://<dbuser>:<dbpassword>@ds155823.mlab.com:55823/smart_exam_trial

host = "ds155823.mlab.com"
port = 55823
db_name = "smart_exam_trial"
user_name = "admin"
password = "admin123"


def connect():
    mongoengine.connect(db_name, host=host, port=port, username=user_name, password=password)

def list2json(l):
    import json
    return [json.loads(item.to_json()) for item in l]


def item2json(item):
    import json
    return json.loads(item.to_json())