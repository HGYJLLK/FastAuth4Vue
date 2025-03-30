from flask import Flask, request, jsonify
from flask_cors import CORS
# pip install mysql-connector-python
import mysql.connector
# from flask_sqlalchemy import SQLAlchemy
# from werkzeug.security import generate_password_hash, check_password_hash
# import jwt
# from datetime import datetime, timedelta

app = Flask(__name__)
CORS(app)

config = {
    'host':'localhost',
    'user':'root',
    'password':'2333',
    'port':3306,
    'database':'user_auth'
}

def create_connection():
    try:
        conn = mysql.connector.connect(**config)
        cursor = conn.cursor()
        print("连接MySQL数据库成功")
        # cursor.execute('''
        #     insert into users(
        #         username,
        #         password,
        #         security_question,
        #         security_answer
        #     ) values(%s,%s,%s,%s)
        # ''',('test','test','test','test'))
        conn.commit()
        print('创建账号成功')
        cursor.execute('select * from users')
        result = cursor.fetchone()
        print(result)
        print('查询账号成功')
        return conn
    except Exception as e:
        print('mysql connect error:',e)
        return None
    finally:
        if 'cursor' in locals():
            cursor.close()
        if 'connection' in locals() and conn.is_connected():
            conn.close()

# # 配置数据库连接
# app.config['SECRET_KEY'] = 'your-secret-key'
# app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://root:2333@localhost/user_auth'
# app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
#
# db = SQLAlchemy(app)

# # 用户模型
# class User(db.Model):
#     __tablename__ = 'users'
#     id = db.Column(db.Integer, primary_key=True)
#     username = db.Column(db.String(50), unique=True, nullable=False)
#     password = db.Column(db.String(255), nullable=False)
#     security_question = db.Column(db.String(255), nullable=False)
#     security_answer = db.Column(db.String(255), nullable=False)
#     created_at = db.Column(db.TIMESTAMP, server_default=db.func.current_timestamp())



# 路由定义...（与之前相同）
@app.route('/register',methods=['POST'])
def register():
    print("register test!!!")
    return "test"

if __name__ == '__main__':
    create_connection()

    # app.run(debug=True)