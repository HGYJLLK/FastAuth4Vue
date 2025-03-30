# Flask Auth API

一个轻量级的 Flask 认证后端，提供用户注册、登录、密码重置和密保验证功能，适合搭配 Vue.js 等前端框架快速构建认证系统。

## 功能特性

- ✅ 用户注册（用户名、密码、密保问题）
- ✅ 用户登录（基础认证）
- ✅ 密码重置功能
- ✅ 密保问题验证
- 🚀 简洁的 RESTful API 设计
- 📦 使用 MySQL 数据库存储用户数据

## 快速开始

### 前置要求

- Python 3.7+
- MySQL 5.7+
- Flask 及相关依赖

### 安装步骤

1. 克隆仓库或下载代码
   ```bash
   git clone [你的仓库地址]
   cd flask-auth-api
   ```

2. 安装依赖
   ```bash
   pip install flask flask-cors mysql-connector-python
   ```

3. 配置数据库
   - 创建 MySQL 数据库 `user_auth`
   - 修改 `main.py` 中的数据库配置：
     ```python
     DB_CONFIG = {
         'host': 'localhost',
         'user': 'root',
         'password': '2333',  # 改为你的MySQL密码
         'port': 3306,
         'database': 'user_auth'
     }
     ```

4. 创建用户表
   ```sql
   CREATE TABLE users (
       id INT AUTO_INCREMENT PRIMARY KEY,
       username VARCHAR(50) UNIQUE NOT NULL,
       password VARCHAR(255) NOT NULL,
       security_question VARCHAR(255) NOT NULL,
       security_answer VARCHAR(255) NOT NULL,
       created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
   );
   ```

5. 启动服务
   ```bash
   python main.py
   ```

## API 文档

### 用户注册

**Endpoint:** `POST /register`

**请求示例:**
```json
{
    "username": "testuser",
    "password": "test123",
    "security_question": "你的出生城市是？",
    "security_answer": "北京"
}
```

**成功响应:**
```json
{
    "message": "User registered successfully"
}
```

### 用户登录

**Endpoint:** `POST /login`

**请求示例:**
```json
{
    "username": "testuser",
    "password": "test123"
}
```

**成功响应:**
```json
{
    "message": "Login successful",
    "user": {
        "username": "testuser",
        "security_question": "你的出生城市是？"
    }
}
```

### 密码重置

**Endpoint:** `POST /reset-password`

**请求示例:**
```json
{
    "username": "testuser",
    "new_password": "newpassword123"
}
```

**成功响应:**
```json
{
    "message": "Password reset successful"
}
```

### 密保验证

1. 获取密保问题
   ```json
   {
       "username": "testuser"
   }
   ```

2. 验证密保答案
   ```json
   {
       "username": "testuser",
       "security_answer": "北京"
   }
   ```

## 项目结构

```
flask-auth-api/
├── main.py                # 主程序文件，包含所有API端点
├── text.py                # 早期测试代码（可忽略）
└── README.md              # 本文件
```

## 注意事项

1. 当前版本使用明文存储密码，生产环境请务必添加密码哈希（如使用 `werkzeug.security`）
2. 建议添加 JWT 认证以增强安全性
3. 可根据需要扩展用户模型（如添加邮箱、手机号等字段）

## 前端对接建议

此API设计为与前端框架（如Vue.js）无缝对接，返回格式均为JSON，包含标准HTTP状态码。

示例Vue.js Axios调用：
```javascript
async function register(userData) {
    try {
        const response = await axios.post('http://localhost:5000/register', userData);
        return response.data;
    } catch (error) {
        throw error.response.data;
    }
}
```

## 许可证

MIT License - 自由使用和修改
