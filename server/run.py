from flask import Flask, jsonify,abort,make_response
import sqlite3

NAME_BD = "../DB_of_tests.db"
app = Flask(__name__)


@app.route('/')
def index():
    return "Hello, World!"


@app.route('/testsystem/api/v1.0/users', methods=['GET'])
def get_users():
    sql = """SELECT id, login, access_level FROM users"""
    answer = make_sql_query(sql)
    return jsonify({"users": answer})


@app.route('/testsystem/api/v1.0/users/<int:user_id>', methods=['GET'])
def get_user(user_id):
    sql = '''SELECT id,login, access_level FROM users WHERE id=''' + str(user_id)
    answer = make_sql_query(sql)
    if answer:
        return jsonify({"users": answer})
    else:
        return abort(404)

def make_sql_query(sql):
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
