from flask import Flask, render_template_string, request, redirect, url_for, session, flash
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
import os
import secrets
import time

app = Flask(__name__)
app.secret_key = secrets.token_hex(16)

# Database Configuration
database_url = os.environ.get('DATABASE_URL', 'postgresql://salon_user:salon_password@db:5432/salon_db')
app.config['SQLALCHEMY_DATABASE_URI'] = database_url
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_ENGINE_OPTIONS'] = {
    'pool_size': 10,
    'pool_recycle': 300,
    'pool_pre_ping': True,
}

db = SQLAlchemy(app)

# ==================== DATABASE MODELS ====================

class User(db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    password = db.Column(db.String(120), nullable=False)
    created_at = db.Column(db.String(50), default=datetime.now().isoformat())

class Appointment(db.Model):
    __tablename__ = 'appointments'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), nullable=False)
    service = db.Column(db.String(100), nullable=False)
    date = db.Column(db.String(20), nullable=False)
    time = db.Column(db.String(10), nullable=False)
    booked_at = db.Column(db.String(50), default=datetime.now().isoformat())
    status = db.Column(db.String(20), default='active')

# ==================== CREATE TABLES ====================

def init_db():
    max_retries = 30
    retry_delay = 2
    
    for attempt in range(max_retries):
        try:
            print(f"Attempting to connect to database (attempt {attempt + 1}/{max_retries})...")
            with app.app_context():
                db.create_all()
                print("✅ Database tables created successfully!")
                return True
        except Exception as e:
            print(f"❌ Database connection failed: {e}")
            if attempt < max_retries - 1:
                print(f"Retrying in {retry_delay} seconds...")
                time.sleep(retry_delay)
            else:
                print("❌ Failed to connect to database after all retries")
                return False

init_db()

# ==================== HTML TEMPLATES ====================

# LOGIN PAGE - Modern & Attractive
LOGIN_PAGE = '''
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Glamour Salon - Login</title>
    <style>
        @import url('https://fonts.googleapis.com/css2?family=Poppins:wght@300;400;600;700&display=swap');
        
        * {
            margin: 0;
            padding: 0;
            box-sizing: border-box;
        }
        
        body {
            font-family: 'Poppins', sans-serif;
            min-height: 100vh;
            display: flex;
            align-items: center;
            justify-content: center;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            background-attachment: fixed;
            padding: 20px;
        }
        
        .container {
            background: rgba(255, 255, 255, 0.95);
            backdrop-filter: blur(20px);
            padding: 50px 40px;
            border-radius: 24px;
            box-shadow: 0 20px 60px rgba(0,0,0,0.3);
            width: 100%;
            max-width: 420px;
            animation: slideUp 0.6s ease-out;
            border: 1px solid rgba(255,255,255,0.2);
        }
        
        @keyframes slideUp {
            from {
                opacity: 0;
                transform: translateY(30px);
            }
            to {
                opacity: 1;
                transform: translateY(0);
            }
        }
        
        .logo {
            text-align: center;
            margin-bottom: 10px;
        }
        
        .logo-icon {
            font-size: 48px;
            display: block;
            margin-bottom: 5px;
        }
        
        h1 {
            color: #2c3e50;
            text-align: center;
            font-size: 28px;
            font-weight: 700;
            margin-bottom: 5px;
        }
        
        .subtitle {
            text-align: center;
            color: #7f8c8d;
            font-size: 14px;
            margin-bottom: 30px;
            font-weight: 300;
        }
        
        .form-group {
            margin-bottom: 20px;
        }
        
        label {
            display: block;
            margin-bottom: 8px;
            color: #34495e;
            font-weight: 600;
            font-size: 13px;
            letter-spacing: 0.5px;
        }
        
        .input-group {
            position: relative;
        }
        
        .input-group .icon {
            position: absolute;
            left: 14px;
            top: 50%;
            transform: translateY(-50%);
            color: #95a5a6;
            font-size: 18px;
        }
        
        input {
            width: 100%;
            padding: 14px 14px 14px 48px;
            border: 2px solid #e0e0e0;
            border-radius: 12px;
            font-size: 14px;
            font-family: 'Poppins', sans-serif;
            transition: all 0.3s ease;
            background: #f8f9fa;
        }
        
        input:focus {
            outline: none;
            border-color: #667eea;
            background: white;
            box-shadow: 0 0 0 4px rgba(102, 126, 234, 0.1);
        }
        
        .btn {
            width: 100%;
            padding: 14px;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            color: white;
            border: none;
            border-radius: 12px;
            font-size: 16px;
            font-weight: 600;
            font-family: 'Poppins', sans-serif;
            cursor: pointer;
            transition: all 0.3s ease;
            position: relative;
            overflow: hidden;
        }
        
        .btn:hover {
            transform: translateY(-2px);
            box-shadow: 0 10px 30px rgba(102, 126, 234, 0.4);
        }
        
        .btn:active {
            transform: translateY(0);
        }
        
        .btn-secondary {
            background: linear-gradient(135deg, #6c757d 0%, #495057 100%);
        }
        
        .btn-secondary:hover {
            box-shadow: 0 10px 30px rgba(108, 117, 125, 0.4);
        }
        
        .link {
            text-align: center;
            margin-top: 20px;
            color: #7f8c8d;
            font-size: 14px;
        }
        
        .link a {
            color: #667eea;
            text-decoration: none;
            font-weight: 600;
            transition: color 0.3s;
        }
        
        .link a:hover {
            color: #764ba2;
            text-decoration: underline;
        }
        
        .flash {
            padding: 14px;
            border-radius: 12px;
            margin-bottom: 20px;
            text-align: center;
            font-size: 14px;
            font-weight: 500;
            animation: fadeIn 0.5s ease;
        }
        
        @keyframes fadeIn {
            from { opacity: 0; transform: translateY(-10px); }
            to { opacity: 1; transform: translateY(0); }
        }
        
        .flash-success {
            background: #d4edda;
            color: #155724;
            border: 1px solid #c3e6cb;
        }
        
        .flash-error {
            background: #f8d7da;
            color: #721c24;
            border: 1px solid #f5c6cb;
        }
        
        .services-info {
            text-align: center;
            margin-top: 25px;
            padding: 15px;
            background: #f8f9fa;
            border-radius: 12px;
            font-size: 12px;
            color: #6c757d;
            line-height: 1.8;
            border: 1px solid #e9ecef;
        }
        
        .services-info span {
            display: inline-block;
            margin: 0 4px;
        }
        
        .footer-text {
            text-align: center;
            margin-top: 15px;
            font-size: 11px;
            color: #adb5bd;
        }
        
        @media (max-width: 480px) {
            .container {
                padding: 30px 20px;
            }
        }
    </style>
</head>
<body>
    <div class="container">
        <div class="logo">
            <span class="logo-icon">💇</span>
        </div>
        <h1>Glamour Salon</h1>
        <p class="subtitle">Book your appointment today!</p>
        
        {% with messages = get_flashed_messages(with_categories=true) %}
            {% if messages %}
                {% for category, message in messages %}
                    <div class="flash flash-{{ category }}">{{ message }}</div>
                {% endfor %}
            {% endif %}
        {% endwith %}
        
        <form method="POST">
            <div class="form-group">
                <label>Username</label>
                <div class="input-group">
                    <span class="icon">👤</span>
                    <input type="text" name="username" placeholder="Enter your username" required>
                </div>
            </div>
            <div class="form-group">
                <label>Password</label>
                <div class="input-group">
                    <span class="icon">🔒</span>
                    <input type="password" name="password" placeholder="Enter your password" required>
                </div>
            </div>
            <button type="submit" class="btn">Sign In</button>
        </form>
        
        <div class="link">
            Don't have an account? <a href="{{ url_for('signup') }}">Create one</a>
        </div>
        
        <div class="services-info">
            ✂️ Haircut &nbsp;•&nbsp; 🎨 Hair Coloring &nbsp;•&nbsp; 💅 Manicure &nbsp;•&nbsp; 🦶 Pedicure &nbsp;•&nbsp;
            🧖 Facial &nbsp;•&nbsp; 💆 Massage &nbsp;•&nbsp; 💄 Makeup &nbsp;•&nbsp; 🪒 Waxing
        </div>
        <div class="footer-text">✨ Your beauty, our priority ✨</div>
    </div>
</body>
</html>
'''

# SIGNUP PAGE - Modern & Attractive
SIGNUP_PAGE = '''
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Glamour Salon - Sign Up</title>
    <style>
        @import url('https://fonts.googleapis.com/css2?family=Poppins:wght@300;400;600;700&display=swap');
        
        * {
            margin: 0;
            padding: 0;
            box-sizing: border-box;
        }
        
        body {
            font-family: 'Poppins', sans-serif;
            min-height: 100vh;
            display: flex;
            align-items: center;
            justify-content: center;
            background: linear-gradient(135deg, #f093fb 0%, #f5576c 100%);
            background-attachment: fixed;
            padding: 20px;
        }
        
        .container {
            background: rgba(255, 255, 255, 0.95);
            backdrop-filter: blur(20px);
            padding: 50px 40px;
            border-radius: 24px;
            box-shadow: 0 20px 60px rgba(0,0,0,0.3);
            width: 100%;
            max-width: 420px;
            animation: slideUp 0.6s ease-out;
        }
        
        @keyframes slideUp {
            from { opacity: 0; transform: translateY(30px); }
            to { opacity: 1; transform: translateY(0); }
        }
        
        .logo-icon {
            font-size: 48px;
            display: block;
            text-align: center;
            margin-bottom: 5px;
        }
        
        h1 {
            color: #2c3e50;
            text-align: center;
            font-size: 28px;
            font-weight: 700;
        }
        
        .subtitle {
            text-align: center;
            color: #7f8c8d;
            font-size: 14px;
            margin-bottom: 30px;
            font-weight: 300;
        }
        
        .form-group {
            margin-bottom: 20px;
        }
        
        label {
            display: block;
            margin-bottom: 8px;
            color: #34495e;
            font-weight: 600;
            font-size: 13px;
        }
        
        .input-group {
            position: relative;
        }
        
        .input-group .icon {
            position: absolute;
            left: 14px;
            top: 50%;
            transform: translateY(-50%);
            color: #95a5a6;
            font-size: 18px;
        }
        
        input {
            width: 100%;
            padding: 14px 14px 14px 48px;
            border: 2px solid #e0e0e0;
            border-radius: 12px;
            font-size: 14px;
            font-family: 'Poppins', sans-serif;
            transition: all 0.3s ease;
            background: #f8f9fa;
        }
        
        input:focus {
            outline: none;
            border-color: #f5576c;
            background: white;
            box-shadow: 0 0 0 4px rgba(245, 87, 108, 0.1);
        }
        
        .btn {
            width: 100%;
            padding: 14px;
            background: linear-gradient(135deg, #f093fb 0%, #f5576c 100%);
            color: white;
            border: none;
            border-radius: 12px;
            font-size: 16px;
            font-weight: 600;
            font-family: 'Poppins', sans-serif;
            cursor: pointer;
            transition: all 0.3s ease;
        }
        
        .btn:hover {
            transform: translateY(-2px);
            box-shadow: 0 10px 30px rgba(245, 87, 108, 0.4);
        }
        
        .btn-secondary {
            background: linear-gradient(135deg, #6c757d 0%, #495057 100%);
        }
        
        .btn-secondary:hover {
            box-shadow: 0 10px 30px rgba(108, 117, 125, 0.4);
        }
        
        .link {
            text-align: center;
            margin-top: 20px;
            color: #7f8c8d;
            font-size: 14px;
        }
        
        .link a {
            color: #f5576c;
            text-decoration: none;
            font-weight: 600;
        }
        
        .link a:hover {
            text-decoration: underline;
        }
        
        .flash {
            padding: 14px;
            border-radius: 12px;
            margin-bottom: 20px;
            text-align: center;
            font-size: 14px;
            font-weight: 500;
            animation: fadeIn 0.5s ease;
        }
        
        @keyframes fadeIn {
            from { opacity: 0; transform: translateY(-10px); }
            to { opacity: 1; transform: translateY(0); }
        }
        
        .flash-success {
            background: #d4edda;
            color: #155724;
            border: 1px solid #c3e6cb;
        }
        
        .flash-error {
            background: #f8d7da;
            color: #721c24;
            border: 1px solid #f5c6cb;
        }
        
        .requirements {
            font-size: 11px;
            color: #6c757d;
            margin-top: 5px;
            padding-left: 5px;
        }
    </style>
</head>
<body>
    <div class="container">
        <span class="logo-icon">✍️</span>
        <h1>Create Account</h1>
        <p class="subtitle">Join Glamour Salon family!</p>
        
        {% with messages = get_flashed_messages(with_categories=true) %}
            {% if messages %}
                {% for category, message in messages %}
                    <div class="flash flash-{{ category }}">{{ message }}</div>
                {% endfor %}
            {% endif %}
        {% endwith %}
        
        <form method="POST">
            <div class="form-group">
                <label>Username</label>
                <div class="input-group">
                    <span class="icon">👤</span>
                    <input type="text" name="username" placeholder="Choose a username" required>
                </div>
            </div>
            <div class="form-group">
                <label>Password</label>
                <div class="input-group">
                    <span class="icon">🔒</span>
                    <input type="password" name="password" placeholder="Create a password" required>
                </div>
                <div class="requirements">🔑 Password must be at least 4 characters</div>
            </div>
            <div class="form-group">
                <label>Confirm Password</label>
                <div class="input-group">
                    <span class="icon">✅</span>
                    <input type="password" name="confirm" placeholder="Confirm your password" required>
                </div>
            </div>
            <button type="submit" class="btn">Create Account</button>
        </form>
        
        <div class="link">
            Already have an account? <a href="{{ url_for('login') }}">Sign In</a>
        </div>
    </div>
</body>
</html>
'''

# DASHBOARD PAGE - Modern & Attractive
DASHBOARD_PAGE = '''
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Glamour Salon - Dashboard</title>
    <style>
        @import url('https://fonts.googleapis.com/css2?family=Poppins:wght@300;400;600;700&display=swap');
        
        * {
            margin: 0;
            padding: 0;
            box-sizing: border-box;
        }
        
        body {
            font-family: 'Poppins', sans-serif;
            background: #f0f2f5;
            min-height: 100vh;
        }
        
        .navbar {
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            color: white;
            padding: 18px 40px;
            display: flex;
            justify-content: space-between;
            align-items: center;
            box-shadow: 0 4px 20px rgba(0,0,0,0.15);
            position: sticky;
            top: 0;
            z-index: 100;
        }
        
        .navbar-brand {
            display: flex;
            align-items: center;
            gap: 12px;
            font-size: 22px;
            font-weight: 700;
        }
        
        .navbar-brand span {
            font-size: 28px;
        }
        
        .navbar-actions {
            display: flex;
            align-items: center;
            gap: 20px;
        }
        
        .user-greeting {
            font-size: 14px;
            opacity: 0.9;
            font-weight: 400;
        }
        
        .btn {
            padding: 10px 24px;
            border: none;
            border-radius: 10px;
            font-size: 14px;
            font-weight: 600;
            font-family: 'Poppins', sans-serif;
            cursor: pointer;
            transition: all 0.3s ease;
            text-decoration: none;
            display: inline-block;
        }
        
        .btn-logout {
            background: rgba(255,255,255,0.2);
            color: white;
            backdrop-filter: blur(10px);
            border: 1px solid rgba(255,255,255,0.3);
        }
        
        .btn-logout:hover {
            background: rgba(255,255,255,0.3);
            transform: translateY(-2px);
        }
        
        .container {
            max-width: 1200px;
            margin: 30px auto;
            padding: 0 20px;
        }
        
        .actions {
            display: flex;
            gap: 15px;
            margin-bottom: 30px;
            flex-wrap: wrap;
        }
        
        .btn-primary {
            background: linear-gradient(135deg, #27ae60 0%, #2ecc71 100%);
            color: white;
            padding: 14px 32px;
            font-size: 15px;
        }
        
        .btn-primary:hover {
            transform: translateY(-3px);
            box-shadow: 0 10px 30px rgba(39, 174, 96, 0.4);
        }
        
        .card {
            background: white;
            border-radius: 16px;
            padding: 30px;
            box-shadow: 0 4px 20px rgba(0,0,0,0.06);
            border: 1px solid #e9ecef;
        }
        
        .card-header {
            display: flex;
            justify-content: space-between;
            align-items: center;
            margin-bottom: 20px;
        }
        
        .card-header h2 {
            color: #2c3e50;
            font-size: 20px;
        }
        
        .card-header .badge {
            background: #667eea;
            color: white;
            padding: 4px 14px;
            border-radius: 20px;
            font-size: 13px;
            font-weight: 600;
        }
        
        table {
            width: 100%;
            border-collapse: collapse;
        }
        
        th {
            background: #f8f9fa;
            padding: 14px 16px;
            text-align: left;
            color: #34495e;
            font-weight: 600;
            font-size: 13px;
            border-bottom: 2px solid #e0e0e0;
        }
        
        td {
            padding: 14px 16px;
            border-bottom: 1px solid #e9ecef;
            color: #2c3e50;
            font-size: 14px;
        }
        
        tr:hover {
            background: #f8f9fa;
        }
        
        .status-badge {
            display: inline-block;
            padding: 4px 14px;
            border-radius: 20px;
            font-size: 12px;
            font-weight: 600;
        }
        
        .status-active {
            background: #d4edda;
            color: #155724;
        }
        
        .status-cancelled {
            background: #f8d7da;
            color: #721c24;
        }
        
        .btn-danger {
            background: #e74c3c;
            color: white;
            padding: 6px 16px;
            font-size: 12px;
            border-radius: 8px;
        }
        
        .btn-danger:hover {
            background: #c0392b;
            transform: translateY(-2px);
            box-shadow: 0 5px 15px rgba(231, 76, 60, 0.4);
        }
        
        .no-data {
            text-align: center;
            padding: 50px 20px;
            color: #7f8c8d;
        }
        
        .no-data .icon {
            font-size: 64px;
            display: block;
            margin-bottom: 15px;
        }
        
        .no-data p {
            font-size: 16px;
        }
        
        .flash {
            padding: 14px 20px;
            border-radius: 12px;
            margin-bottom: 20px;
            font-size: 14px;
            font-weight: 500;
            animation: slideDown 0.4s ease;
        }
        
        @keyframes slideDown {
            from { opacity: 0; transform: translateY(-20px); }
            to { opacity: 1; transform: translateY(0); }
        }
        
        .flash-success {
            background: #d4edda;
            color: #155724;
            border: 1px solid #c3e6cb;
        }
        
        .flash-error {
            background: #f8d7da;
            color: #721c24;
            border: 1px solid #f5c6cb;
        }
        
        .footer {
            text-align: center;
            margin-top: 40px;
            padding: 20px;
            color: #adb5bd;
            font-size: 14px;
        }
        
        @media (max-width: 768px) {
            .navbar {
                flex-direction: column;
                gap: 12px;
                padding: 15px 20px;
                text-align: center;
            }
            
            .navbar-actions {
                flex-direction: column;
                width: 100%;
            }
            
            .btn {
                width: 100%;
                text-align: center;
            }
            
            .actions {
                flex-direction: column;
            }
            
            .actions .btn {
                width: 100%;
                text-align: center;
            }
            
            table {
                font-size: 13px;
            }
            
            th, td {
                padding: 10px 12px;
            }
            
            .card {
                padding: 20px;
                overflow-x: auto;
            }
        }
    </style>
</head>
<body>
    <nav class="navbar">
        <div class="navbar-brand">
            <span>💇</span> Glamour Salon
        </div>
        <div class="navbar-actions">
            <span class="user-greeting">👋 Welcome, {{ username }}!</span>
            <a href="{{ url_for('logout') }}" class="btn btn-logout">🚪 Logout</a>
        </div>
    </nav>
    
    <div class="container">
        {% with messages = get_flashed_messages(with_categories=true) %}
            {% if messages %}
                {% for category, message in messages %}
                    <div class="flash flash-{{ category }}">{{ message }}</div>
                {% endfor %}
            {% endif %}
        {% endwith %}
        
        <div class="actions">
            <a href="{{ url_for('book') }}" class="btn btn-primary">📅 Book New Appointment</a>
        </div>
        
        <div class="card">
            <div class="card-header">
                <h2>📋 Your Appointments</h2>
                <span class="badge">{{ appointments|length }} total</span>
            </div>
            <table>
                <thead>
                    <tr>
                        <th>Service</th>
                        <th>Date</th>
                        <th>Time</th>
                        <th>Status</th>
                        <th>Action</th>
                    </tr>
                </thead>
                <tbody>
                    {% if appointments %}
                        {% for app in appointments %}
                        <tr>
                            <td>
                                {% if app.service == 'Haircut' %}✂️
                                {% elif app.service == 'Hair Coloring' %}🎨
                                {% elif app.service == 'Manicure' %}💅
                                {% elif app.service == 'Pedicure' %}🦶
                                {% elif app.service == 'Facial' %}🧖
                                {% elif app.service == 'Massage' %}💆
                                {% elif app.service == 'Makeup' %}💄
                                {% elif app.service == 'Waxing' %}🪒
                                {% endif %}
                                {{ app.service }}
                            </td>
                            <td>📅 {{ app.date }}</td>
                            <td>🕐 {{ app.time }}</td>
                            <td><span class="status-badge status-{{ app.status }}">{{ app.status|title }}</span></td>
                            <td>
                                {% if app.status == 'active' %}
                                    <a href="{{ url_for('cancel', id=app.id) }}" class="btn btn-danger" onclick="return confirm('Are you sure you want to cancel this appointment?')">Cancel</a>
                                {% else %}
                                    <span style="color: #7f8c8d; font-size: 13px;">❌ Cancelled</span>
                                {% endif %}
                            </td>
                        </tr>
                        {% endfor %}
                    {% else %}
                        <tr>
                            <td colspan="5">
                                <div class="no-data">
                                    <span class="icon">📭</span>
                                    <p>No appointments booked yet.</p>
                                    <a href="{{ url_for('book') }}" class="btn btn-primary" style="margin-top: 15px; display: inline-block;">Book your first appointment</a>
                                </div>
                            </td>
                        </tr>
                    {% endif %}
                </tbody>
            </table>
        </div>
        
        <div class="footer">
            💇 Glamour Salon — Your beauty, our priority ✨
        </div>
    </div>
</body>
</html>
'''

# BOOKING PAGE - Modern & Attractive
BOOK_PAGE = '''
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Glamour Salon - Book Appointment</title>
    <style>
        @import url('https://fonts.googleapis.com/css2?family=Poppins:wght@300;400;600;700&display=swap');
        
        * {
            margin: 0;
            padding: 0;
            box-sizing: border-box;
        }
        
        body {
            font-family: 'Poppins', sans-serif;
            min-height: 100vh;
            display: flex;
            align-items: center;
            justify-content: center;
            background: linear-gradient(135deg, #a8edea 0%, #fed6e3 100%);
            background-attachment: fixed;
            padding: 20px;
        }
        
        .container {
            background: rgba(255, 255, 255, 0.95);
            backdrop-filter: blur(20px);
            padding: 50px 40px;
            border-radius: 24px;
            box-shadow: 0 20px 60px rgba(0,0,0,0.15);
            width: 100%;
            max-width: 500px;
            animation: slideUp 0.6s ease-out;
        }
        
        @keyframes slideUp {
            from { opacity: 0; transform: translateY(30px); }
            to { opacity: 1; transform: translateY(0); }
        }
        
        .logo-icon {
            font-size: 48px;
            display: block;
            text-align: center;
            margin-bottom: 5px;
        }
        
        h1 {
            color: #2c3e50;
            text-align: center;
            font-size: 28px;
            font-weight: 700;
        }
        
        .subtitle {
            text-align: center;
            color: #7f8c8d;
            font-size: 14px;
            margin-bottom: 30px;
            font-weight: 300;
        }
        
        .form-group {
            margin-bottom: 22px;
        }
        
        label {
            display: block;
            margin-bottom: 8px;
            color: #34495e;
            font-weight: 600;
            font-size: 13px;
        }
        
        .input-group {
            position: relative;
        }
        
        .input-group .icon {
            position: absolute;
            left: 14px;
            top: 50%;
            transform: translateY(-50%);
            color: #95a5a6;
            font-size: 18px;
            z-index: 1;
        }
        
        select, input {
            width: 100%;
            padding: 14px 14px 14px 48px;
            border: 2px solid #e0e0e0;
            border-radius: 12px;
            font-size: 14px;
            font-family: 'Poppins', sans-serif;
            transition: all 0.3s ease;
            background: #f8f9fa;
            appearance: none;
            -webkit-appearance: none;
            cursor: pointer;
        }
        
        select {
            background-image: url("data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' width='12' height='12' viewBox='0 0 12 12'%3E%3Cpath fill='%2395a5a6' d='M6 8L1 3h10z'/%3E%3C/svg%3E");
            background-repeat: no-repeat;
            background-position: right 14px center;
            padding-right: 40px;
        }
        
        select:focus, input:focus {
            outline: none;
            border-color: #667eea;
            background: white;
            box-shadow: 0 0 0 4px rgba(102, 126, 234, 0.1);
        }
        
        .btn {
            width: 100%;
            padding: 14px;
            background: linear-gradient(135deg, #27ae60 0%, #2ecc71 100%);
            color: white;
            border: none;
            border-radius: 12px;
            font-size: 16px;
            font-weight: 600;
            font-family: 'Poppins', sans-serif;
            cursor: pointer;
            transition: all 0.3s ease;
            margin-top: 5px;
        }
        
        .btn:hover {
            transform: translateY(-2px);
            box-shadow: 0 10px 30px rgba(39, 174, 96, 0.4);
        }
        
        .btn-secondary {
            background: linear-gradient(135deg, #6c757d 0%, #495057 100%);
            margin-top: 10px;
        }
        
        .btn-secondary:hover {
            box-shadow: 0 10px 30px rgba(108, 117, 125, 0.4);
        }
        
        .link {
            text-align: center;
            margin-top: 20px;
            color: #7f8c8d;
            font-size: 14px;
        }
        
        .link a {
            color: #667eea;
            text-decoration: none;
            font-weight: 600;
        }
        
        .link a:hover {
            text-decoration: underline;
        }
        
        .flash {
            padding: 14px;
            border-radius: 12px;
            margin-bottom: 20px;
            text-align: center;
            font-size: 14px;
            font-weight: 500;
            animation: fadeIn 0.5s ease;
        }
        
        @keyframes fadeIn {
            from { opacity: 0; transform: translateY(-10px); }
            to { opacity: 1; transform: translateY(0); }
        }
        
        .flash-success {
            background: #d4edda;
            color: #155724;
            border: 1px solid #c3e6cb;
        }
        
        .flash-error {
            background: #f8d7da;
            color: #721c24;
            border: 1px solid #f5c6cb;
        }
        
        .date-hint {
            font-size: 11px;
            color: #6c757d;
            margin-top: 5px;
            padding-left: 5px;
        }
        
        .service-option {
            display: flex;
            align-items: center;
            gap: 8px;
        }
    </style>
</head>
<body>
    <div class="container">
        <span class="logo-icon">📅</span>
        <h1>Book Appointment</h1>
        <p class="subtitle">Choose your service and schedule</p>
        
        {% with messages = get_flashed_messages(with_categories=true) %}
            {% if messages %}
                {% for category, message in messages %}
                    <div class="flash flash-{{ category }}">{{ message }}</div>
                {% endfor %}
            {% endif %}
        {% endwith %}
        
        <form method="POST">
            <div class="form-group">
                <label>💇 Service</label>
                <div class="input-group">
                    <span class="icon">✂️</span>
                    <select name="service" required>
                        <option value="Haircut">✂️ Haircut</option>
                        <option value="Hair Coloring">🎨 Hair Coloring</option>
                        <option value="Manicure">💅 Manicure</option>
                        <option value="Pedicure">🦶 Pedicure</option>
                        <option value="Facial">🧖 Facial</option>
                        <option value="Massage">💆 Massage</option>
                        <option value="Makeup">💄 Makeup</option>
                        <option value="Waxing">🪒 Waxing</option>
                    </select>
                </div>
            </div>
            
            <div class="form-group">
                <label>📆 Date</label>
                <div class="input-group">
                    <span class="icon">📅</span>
                    <input type="text" name="date" value="{{ today }}" placeholder="YYYY-MM-DD" required>
                </div>
                <div class="date-hint">📌 Format: YYYY-MM-DD (e.g., 2026-07-09)</div>
            </div>
            
            <div class="form-group">
                <label>🕐 Time</label>
                <div class="input-group">
                    <span class="icon">⏰</span>
                    <input type="text" name="time" value="10:00" placeholder="HH:MM" required>
                </div>
                <div class="date-hint">📌 Format: HH:MM (24-hour, e.g., 14:30)</div>
            </div>
            
            <button type="submit" class="btn">✅ Book Appointment</button>
        </form>
        
        <div class="link">
            <a href="{{ url_for('dashboard') }}">← Back to Dashboard</a>
        </div>
    </div>
</body>
</html>
'''

# ==================== ROUTES ====================

@app.route('/')
def home():
    return redirect(url_for('login'))

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        
        if not username or not password:
            flash('Please fill in all fields', 'error')
            return render_template_string(LOGIN_PAGE)
        
        user = User.query.filter_by(username=username).first()
        if user and user.password == password:
            session['username'] = username
            flash(f'🎉 Welcome back, {username}!', 'success')
            return redirect(url_for('dashboard'))
        else:
            flash('❌ Invalid username or password', 'error')
            return render_template_string(LOGIN_PAGE)
    
    if 'username' in session:
        return redirect(url_for('dashboard'))
    return render_template_string(LOGIN_PAGE)

@app.route('/signup', methods=['GET', 'POST'])
def signup():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        confirm = request.form.get('confirm')
        
        if not username or not password or not confirm:
            flash('All fields are required', 'error')
            return render_template_string(SIGNUP_PAGE)
        
        if password != confirm:
            flash('Passwords do not match', 'error')
            return render_template_string(SIGNUP_PAGE)
        
        if len(password) < 4:
            flash('Password must be at least 4 characters', 'error')
            return render_template_string(SIGNUP_PAGE)
        
        existing_user = User.query.filter_by(username=username).first()
        if existing_user:
            flash(f'Username "{username}" already exists', 'error')
            return render_template_string(SIGNUP_PAGE)
        
        new_user = User(username=username, password=password)
        db.session.add(new_user)
        db.session.commit()
        
        flash(f'🎉 Account created! Please login, {username}', 'success')
        return redirect(url_for('login'))
    
    return render_template_string(SIGNUP_PAGE)

@app.route('/dashboard')
def dashboard():
    if 'username' not in session:
        flash('Please login first', 'error')
        return redirect(url_for('login'))
    
    appointments = Appointment.query.filter_by(
        username=session['username']
    ).order_by(Appointment.date, Appointment.time).all()
    
    return render_template_string(DASHBOARD_PAGE, 
                                 username=session['username'],
                                 appointments=appointments)

@app.route('/book', methods=['GET', 'POST'])
def book():
    if 'username' not in session:
        flash('Please login first', 'error')
        return redirect(url_for('login'))
    
    if request.method == 'POST':
        service = request.form.get('service')
        date = request.form.get('date')
        time = request.form.get('time')
        
        if not service or not date or not time:
            flash('All fields are required', 'error')
            return render_template_string(BOOK_PAGE, today=datetime.now().strftime('%Y-%m-%d'))
        
        try:
            datetime.strptime(date, '%Y-%m-%d')
        except ValueError:
            flash('Invalid date format. Use YYYY-MM-DD', 'error')
            return render_template_string(BOOK_PAGE, today=datetime.now().strftime('%Y-%m-%d'))
        
        try:
            datetime.strptime(time, '%H:%M')
        except ValueError:
            flash('Invalid time format. Use HH:MM (24-hour)', 'error')
            return render_template_string(BOOK_PAGE, today=datetime.now().strftime('%Y-%m-%d'))
        
        existing = Appointment.query.filter_by(
            username=session['username'],
            date=date,
            time=time
        ).first()
        
        if existing:
            flash('You already have an appointment at this time', 'error')
            return render_template_string(BOOK_PAGE, today=datetime.now().strftime('%Y-%m-%d'))
        
        appointment = Appointment(
            username=session['username'],
            service=service,
            date=date,
            time=time,
            status='active'
        )
        db.session.add(appointment)
        db.session.commit()
        
        flash(f'✅ Appointment booked for {service} on {date} at {time}!', 'success')
        return redirect(url_for('dashboard'))
    
    return render_template_string(BOOK_PAGE, today=datetime.now().strftime('%Y-%m-%d'))

@app.route('/cancel/<int:id>')
def cancel(id):
    if 'username' not in session:
        flash('Please login first', 'error')
        return redirect(url_for('login'))
    
    appointment = Appointment.query.get(id)
    if not appointment:
        flash('Appointment not found', 'error')
        return redirect(url_for('dashboard'))
    
    if appointment.username != session['username']:
        flash('You can only cancel your own appointments', 'error')
        return redirect(url_for('dashboard'))
    
    if appointment.status == 'cancelled':
        flash('This appointment is already cancelled', 'error')
        return redirect(url_for('dashboard'))
    
    appointment.status = 'cancelled'
    db.session.commit()
    
    flash(f'❌ Appointment for {appointment.service} on {appointment.date} cancelled', 'success')
    return redirect(url_for('dashboard'))

@app.route('/logout')
def logout():
    session.pop('username', None)
    flash('You have been logged out', 'success')
    return redirect(url_for('login'))

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port, debug=False)
