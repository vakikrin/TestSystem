import sqlite3
import os

NAME_DB = 'DB_of_tests.db'


def main():
    path = os.path.join(os.path.abspath(os.path.dirname(__file__)), NAME_DB)
    if os.path.exists(path):
        os.remove(path)
    connect_to_BD = sqlite3.connect(NAME_DB)
    DB = connect_to_BD.cursor()
    DB.execute("PRAGMA foreign_keys = ON;")

    DB.execute(""" 
         CREATE TABLE  users(
         id INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT,
         login TEXT NOT NULL,
         password TEXT NOT NULL,
         access_level INTEGER NOT NULL,
         confirm INTEGER
         )
    """)

    DB.execute(""" 
             CREATE TABLE  type_questions(
             id INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT,
             typeQuestion TEXT NOT NULL 
             )
        """)

    DB.execute(""" 
             CREATE TABLE  labs(
             id INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT,
             name TEXT NOT NULL,
             countOfQuestions INTEGER NOT NULL 
             )
        """)

    DB.execute(""" 
             CREATE TABLE  Q_input_number(
             id INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT,
             typeQuestion INTEGER NOT NULL,
             textOfQuestion TEXT,
             correctAnswer REAL,
             lab INTEGER NOT NULL,
             FOREIGN KEY (lab) REFERENCES labs(id),
             FOREIGN KEY (typeQuestion) REFERENCES type_questions(id)
             )
        """)

    DB.execute(""" 
                 CREATE TABLE  Q_one_of_four(
                 id INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT,
                 typeQuestion INTEGER NOT NULL,
                 textOfQuestion TEXT,
                 correctAnswer TEXT,
                 incorrectOptions1 TEXT,
                 incorrectOptions2 TEXT,
                 incorrectOptions3 TEXT,
                 lab INTEGER NOT NULL,
                 FOREIGN KEY (lab) REFERENCES labs(id),
                 FOREIGN KEY (typeQuestion) REFERENCES type_questions(id)
                 )
            """)

    DB.execute(""" 
                     CREATE TABLE  Q_choose_of_formula(
                     id INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT,
                     typeQuestion INTEGER NOT NULL,
                     textOfQuestion TEXT,
                     correctFormula TEXT,
                     incorrectOptions1 TEXT,
                     incorrectOptions2 TEXT,
                     incorrectOptions3 TEXT,
                     lab INTEGER NOT NULL,
                     FOREIGN KEY (lab) REFERENCES labs(id),
                     FOREIGN KEY (typeQuestion) REFERENCES type_questions(id)
                     )
                """)

    add_user(connect_to_BD, ("admin", "admin", 3, 1))
    add_user(connect_to_BD, ("teach1", "teach1", 2, 1))
    add_user(connect_to_BD, ("user1", "user1", 1, 1))
    add_user(connect_to_BD, ("user2", "user2", 1, 1))

    add_type_questions(connect_to_BD, ("4 Вопроса 1 правильный ответ",))
    add_type_questions(connect_to_BD, ("Вставить правильное число",))
    add_type_questions(connect_to_BD, ("Выбрать правильную формулу",))

    add_labs(connect_to_BD, ("Електромеханика", 5))
    add_labs(connect_to_BD, ("Математика", 10))

    add_q_one_of_four(connect_to_BD,("1","Сколько будет 3+1?","4","15","12","12",2))
    add_q_one_of_four(connect_to_BD, ("1", "Сколько будет 3+4?", "7", "15", "12", "12", 2))
    add_q_one_of_four(connect_to_BD, ("1", "Електромеханика это - ", "електрическая механика.", "Наука о данных", \
                                      "Наука про общщество", "Какая-то дичь", "1"))

    add_q_input_number(connect_to_BD,("2","Значения числа ПИ равно:", 3.14,2))
    add_q_input_number(connect_to_BD, ("2", "Значения числа e равно:", 2.17, 2))
    add_q_input_number(connect_to_BD, ("2", "Значения числа 12/2:", 6, 1))

    add_q_choose_of_formula(connect_to_BD,("3","Х во второй степени","{x}^2","{x}_2","\sum {x}_i","\sum {x}_i\cdot \alpha {x}'",2))


def add_user(conn, user):
    """

    :param connector:
    :param user:
    :return:
    """
    print("dsa")
    sql = "INSERT INTO users(login,password,access_level,confirm) VALUES(?,?,?,?)"
    cursor = conn.cursor()
    cursor.execute(sql, user)
    conn.commit()


def add_type_questions(conn, typeQ):
    """

    :param conn:
    :param typeQ:
    :return:
    """
    sql = "INSERT INTO type_questions(typeQuestion) VALUES(?)"
    cursor = conn.cursor()
    cursor.execute(sql, typeQ)
    conn.commit()


def add_labs(conn, labs):
    """

    :param conn:
    :param labs:
    :return:
    """
    sql = "INSERT INTO labs(name,countOfQuestions) VALUES (?,?)"
    cursor = conn.cursor()
    cursor.execute(sql, labs)
    conn.commit()

def add_q_one_of_four(conn, questions):
    """

    :param conn:
    :param questions:
    :return:
    """
    sql = """ 
          INSERT INTO Q_one_of_four (typeQuestion,textOfQuestion, correctAnswer, incorrectOptions1,
          incorrectOptions2, incorrectOptions3, lab) VALUES (?,?,?,?,?,?,?)
          """
    cursor = conn.cursor()
    cursor.execute(sql, questions)
    conn.commit()

def add_q_input_number(conn, questions):
    """

    :param conn:
    :param questions:
    :return:
    """
    sql = """ 
          INSERT INTO Q_input_number (typeQuestion,textOfQuestion, correctAnswer, lab) VALUES (?,?,?,?)
          """
    cursor = conn.cursor()
    cursor.execute(sql, questions)
    conn.commit()

def add_q_choose_of_formula(conn, questions):
    """

    :param conn:
    :param questions:
    :return:
    """
    sql = """ 
          INSERT INTO Q_choose_of_formula (typeQuestion,textOfQuestion, correctFormula,incorrectOptions1,
          incorrectOptions2, incorrectOptions3, lab) VALUES (?,?,?,?,?,?,?)
          """
    cursor = conn.cursor()
    cursor.execute(sql, questions)
    conn.commit()
if __name__ == '__main__':
    main()
