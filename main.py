from flask import Flask, request, jsonify
from flask_cors import CORS
import mysql.connector
from datetime import datetime
import logging

app = Flask(__name__)
CORS(app)

# Database configuration
DB_CONFIG = {
    'host': 'localhost',
    'user': 'root',
    'password': '2333',
    'port': 3306,
    'database': 'user_auth'
}

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class DatabaseManager:
    @staticmethod
    def get_connection():
        try:
            conn = mysql.connector.connect(**DB_CONFIG)
            return conn
        except Exception as e:
            logger.error(f"Database connection error: {e}")
            return None

    @staticmethod
    def execute_query(query, params=None, fetch=False):
        conn = None
        cursor = None
        try:
            conn = DatabaseManager.get_connection()
            if not conn:
                return None

            cursor = conn.cursor(dictionary=True)
            cursor.execute(query, params or ())

            if fetch:
                result = cursor.fetchall()
            else:
                conn.commit()
                result = cursor.rowcount

            return result
        except Exception as e:
            logger.error(f"Query execution error: {e}")
            if conn:
                conn.rollback()
            return None
        finally:
            if cursor:
                cursor.close()
            if conn:
                conn.close()


class UserService:
    @staticmethod
    def create_user(username, password, security_question, security_answer):
        query = """
            INSERT INTO users (username, password, security_question, security_answer)
            VALUES (%s, %s, %s, %s)
        """
        params = (username, password, security_question, security_answer)
        return DatabaseManager.execute_query(query, params)

    @staticmethod
    def get_user_by_username(username):
        query = "SELECT * FROM users WHERE username = %s"
        params = (username,)
        result = DatabaseManager.execute_query(query, params, fetch=True)
        return result[0] if result else None

    @staticmethod
    def update_password(username, new_password):
        query = "UPDATE users SET password = %s WHERE username = %s"
        params = (new_password, username)
        return DatabaseManager.execute_query(query, params)


@app.route('/register', methods=['POST'])
def register():
    try:
        data = request.get_json()
        username = data.get('username')
        password = data.get('password')
        security_question = data.get('security_question')
        security_answer = data.get('security_answer')

        # Validate input
        if not all([username, password, security_question, security_answer]):
            return jsonify({'error': 'Missing required fields'}), 400

        # Check if username already exists
        existing_user = UserService.get_user_by_username(username)
        if existing_user:
            return jsonify({'error': 'Username already exists'}), 409

        # Create new user
        result = UserService.create_user(username, password, security_question, security_answer)
        if result is not None:
            return jsonify({'message': 'User registered successfully'}), 201
        else:
            return jsonify({'error': 'Registration failed'}), 500

    except Exception as e:
        logger.error(f"Registration error: {e}")
        return jsonify({'error': 'Internal server error'}), 500


@app.route('/login', methods=['POST'])
def login():
    try:
        data = request.get_json()
        username = data.get('username')
        password = data.get('password')

        # Validate input
        if not all([username, password]):
            return jsonify({'error': 'Missing credentials'}), 400

        # Get user
        user = UserService.get_user_by_username(username)
        if not user:
            return jsonify({'error': 'User not found'}), 404

        # Verify password (in a real application, use proper password hashing)
        if user['password'] != password:
            return jsonify({'error': 'Invalid password'}), 401

        return jsonify({
            'message': 'Login successful',
            'user': {
                'username': user['username'],
                'security_question': user['security_question']
            }
        }), 200

    except Exception as e:
        logger.error(f"Login error: {e}")
        return jsonify({'error': 'Internal server error'}), 500


@app.route('/reset-password', methods=['POST'])
def reset_password():
    try:
        data = request.get_json()
        username = data.get('username')
        new_password = data.get('new_password')

        # Validate input
        if not all([username, new_password]):
            return jsonify({'error': 'Missing required fields'}), 400

        # Get user
        user = UserService.get_user_by_username(username)
        if not user:
            return jsonify({'error': 'User not found'}), 404

        # Update password
        result = UserService.update_password(username, new_password)
        if result is not None:
            return jsonify({'message': 'Password reset successful'}), 200
        else:
            return jsonify({'error': 'Password reset failed'}), 500

    except Exception as e:
        logger.error(f"Password reset error: {e}")
        return jsonify({'error': 'Internal server error'}), 500

@app.route('/verify-security', methods=['POST'])
def verify_security():
    try:
        data = request.get_json()
        username = data.get('username')
        security_answer = data.get('security_answer')

        # Get user and return security question
        user = UserService.get_user_by_username(username)
        if not user:
            return jsonify({'error': 'User not found'}), 404

        # 如果没有提供security_answer,说明只是获取密保问题
        if not security_answer:
            return jsonify({
                'security_question': user['security_question']
            }), 200

        # 如果提供了security_answer,则验证答案
        if user['security_answer'] != security_answer:
            return jsonify({'error': 'Invalid security answer'}), 401

        return jsonify({
            'message': 'Security answer verified',
            'verified': True
        }), 200

    except Exception as e:
        logger.error(f"Security verification error: {e}")
        return jsonify({'error': 'Internal server error'}), 500


if __name__ == '__main__':
    app.run(debug=True)