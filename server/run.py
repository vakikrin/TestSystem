from flask import Flask, jsonify,abort,make_response,request
import sqlite3

NAME_BD = "../DB_of_tests.db"
app = Flask(__name__)


@app.route('/')
def index():
    return "Hello, World!"


@app.route('/testsystem/api/v1.0/users', methods=['GET'])
def get_users():
    sql = """SELECT id, login, access_level FROM users"""
    answer = make_sql_query_select(sql)
    return jsonify({"users": answer})


@app.route('/testsystem/api/v1.0/users/<int:user_id>', methods=['GET'])
def get_user(user_id):
    sql = '''SELECT id,login, access_level FROM users WHERE id=''' + str(user_id)
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
            value = (login,psw,access_lvl,0)
            make_sql_query_insert(sql,value)
            return jsonify({"Answer":"Successfully"}), 201
    else:
        return abort(401)

def make_sql_query_insert(sql, val):
    """

    :param sql:
    :return:
    """
    with sqlite3.connect(NAME_BD) as con:
        cur = con.cursor()
        response = cur.execute(sql,val).fetchall()
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
    return make_response(jsonify({"error":"Not Found"}),404)

if __name__ == '__main__':
    app.run(debug=True)
