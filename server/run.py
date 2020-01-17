from flask import Flask, jsonify, abort, make_response, request, url_for,send_from_directory,render_template
import sqlite3
from flask import render_template
from flask_cors import CORS,cross_origin
# -*- coding: utf-8 -*-
NAME_BD = "../DB_of_tests.db"
app = Flask(__name__)
app.config['JSON_AS_ASCII'] = False
cors = CORS(app, resources={r"/testsystem/api/*": {"origins": "*"}})


@app.route('/')
def index():
    return render_template("index.html")


# TODO: Сделать возможность редактировать юзера, и удалять.
# TODO; Get Post Put Delete для всех остальных табличек
# TODO: Tables: Labs, oneOFfour,ChooseFormula,insertNumber
# TODO: Проверить работоспособность АПИ для JS)
# TODO: Посмотреть возможности REACT
def make_public_user(user):
    new_user = {}
    for field in user:
        if field == "id":
            new_user['uri'] = url_for('get_user', user_id=user['id'], _external=True)
        else:
            new_user[field] = user[field]
    return new_user



def get_question_one_of_four(id_lab):
    sql = """SELECT id, textOfQuestion, correctAnswer, incorrectOptions1,incorrectOptions2,incorrectOptions3,lab,typeQuestion FROM Q_one_of_four where lab=""" + str(
        id_lab)
    questions = make_sql_query_select(sql)
    return {"Questions_one_of_four": questions}


def get_question_choose_of_formula(id_lab):
    sql = """SELECT id, textOfQuestion, correctFormula, incorrectOptions1,incorrectOptions2,incorrectOptions3,lab,typeQuestion FROM Q_choose_of_formula where lab=""" + str(
        id_lab)
    questions = make_sql_query_select(sql)
    return {"Questions_choose_of_formula": questions}

def get_question_input_number(id_lab):
    sql = """SELECT id, textOfQuestion, correctAnswer,lab,typeQuestion FROM Q_input_number where lab=""" + str(
        id_lab)
    questions = make_sql_query_select(sql)
    return {"Questions_input_number": questions}


@app.route('/testsystem/api/v1.0/labs/questions', methods=['GET','POST'])
@cross_origin()
def get_question():
    if request.json:
        id = request.json["idTest"]

        return  jsonify(get_question_choose_of_formula(id),get_question_one_of_four(id),get_question_input_number(id))
    else:
        return abort(404)

    
@app.route('/testsystem/api/v1.0/labs', methods=['GET'])
def get_labs():
    sql = """SELECT id, name FROM labs"""
    labs = make_sql_query_select(sql)
    return jsonify({"labs": labs})


@app.route('/testsystem/api/v1.0/labs/<int:id_lab>', methods=['GET'])
def get_lab(id_lab):
    sql = """SELECT id, name FROM labs WHERE id=""" + str(id_lab)
    lab = make_sql_query_select(sql)
    if lab:
        return jsonify({"labs": lab})
    else:
        return abort(404)


@app.route('/testsystem/api/v1.0/users', methods=['GET'])
def get_users():
    sql = """SELECT id, login, access_level FROM users"""
    users = make_sql_query_select(sql)
    users = [make_public_user(x) for x in users]
    return jsonify({"users": users})


@app.route('/testsystem/api/v1.0/users_id/<int:user_id>', methods=['GET'])
def get_user_id(user_id):
    sql = '''SELECT id,login, access_level FROM users WHERE id=''' + str(user_id)
    answer = make_sql_query_select(sql)
    if answer:
        return jsonify({"users": answer})
    else:
        return abort(404)

# TODO: обезопазить пароль
@app.route('/testsystem/api/v1.0/users_name/<string:username>', methods=['GET'])
def get_user_name(username):
    sql = '''SELECT id,login, access_level, password FROM users WHERE login="''' + username + "\""
    answer = make_sql_query_select(sql)
    if answer:
        return jsonify({"users": answer})
    else:
        return abort(404)

@app.route('/testsystem/api/v1.0/users/add', methods=['POST'])
def add_user():
    sql = """INSERT INTO users(login, password, access_level, confirm) VALUES (?,?,?,?)"""
    if request.json:
        login = request.json['login'] if request.json['login'] else None
        psw = request.json['password'] if request.json['password'] else None
        access_lvl = request.json['access_level'] if request.json['access_level'] else None
        if psw and login and access_lvl:
            value = (login, psw, access_lvl, 0)
            make_sql_query_insert(sql, value)
            return jsonify({"Answer": "Successfully"}), 201
    else:
        return abort(401)


def make_sql_query_insert(sql, val):
    """

    :param sql:
    :return:
    """
    with sqlite3.connect(NAME_BD) as con:
        cur = con.cursor()
        response = cur.execute(sql, val).fetchall()


def make_sql_query_select(sql):
    def parse_sql_select(response, description):
        """

        :param response:
        :return:
        """
        rows = [x for x in response]
        cols = [x[0] for x in description]
        answer = []
        for row in rows:
            info = {}
            for key, val in zip(cols, row):
                info[key] = val
            answer.append(info)
        return answer

    with sqlite3.connect(NAME_BD) as con:
        cur = con.cursor()
        response = cur.execute(sql).fetchall()
    answer = parse_sql_select(response, cur.description)
    return answer


@app.errorhandler(404)
def not_found(error):
    return make_response(jsonify({"error": "Not Found"}), 404)

@app.route('/testsystem/api/v1.0/users/<string:username>/<string:password>' , methods=['GET'])
def log_in(username,password):
    sql = '''SELECT password FROM users WHERE login="''' + username + "\""
    answer = make_sql_query_select(sql)
    if answer:
        if answer[0]['password'] == password:
            return jsonify({"log_in": 'Successfully'})
        else:
            return jsonify({'log_in': 'Reject'})
    else:
        return abort(404)

if __name__ == '__main__':
    app.run(debug=True)
