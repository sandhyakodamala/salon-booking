from flask import Flask, render_template_string, request, redirect, url_for, session, flash
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
import os
import secrets

app = Flask(__name__)
app.secret_key = secrets.token_hex(16)

# Database Configuration
database_url = os.environ.get('DATABASE_URL', 'postgresql://salon_user:salon_password@db:5432/salon_db')
app.config['SQLALCHEMY_DATABASE_URI'] = database_url
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

# ==================== DATABASE MODELS ====================

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    password = db.Column(db.String(120), nullable=False)
    created_at = db.Column(db.String(50), default=datetime.now().isoformat())

class Appointment(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), nullable=False)
    service = db.Column(db.String(100), nullable=False)
    date = db.Column(db.String(20), nullable=False)
    time = db.Column(db.String(10), nullable=False)
    booked_at = db.Column(db.String(50), default=datetime.now().isoformat())
    status = db.Column(db.String(20), default='active')

# Create tables
with app.app_context():
    db.create_all()

# ==================== HTML TEMPLATES ====================

LOGIN_PAGE = '''
<!DOCTYPE html>
<html>
<head>
    <title>Glamour Salon - Login</title>
    <style>
        * { margin: 0; padding: 0; box-sizing: border-box; }
        body {
            font-family: Arial, sans-serif;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            min-height: 100vh;
            display: flex;
            align-items: center;
            justify-content: center;
        }
        .container {
            background: white;
            padding: 40px;
            border-radius: 15px;
            box-shadow: 0 10px 30px rgba(0,0,0,0.3);
            width: 100%;
            max-width: 400px;
        }
        h1 { color: #2c3e50; text-align: center; }
        .subtitle { text-align: center; color: #7f8c8d; margin-bottom: 30px; }
        .form-group { margin-bottom: 20px; }
        label { display: block; margin-bottom: 5px; color: #34495e; font-weight: 600; }
        input {
            width: 100%;
            padding: 12px;
            border: 2px solid #e0e0e0;
            border-radius: 8px;
            font-size: 14px;
        }
        input:focus { outline: none; border-color: #667eea; }
        .btn {
            width: 100%;
            padding: 12px;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            color: white;
            border: none;
            border-radius: 8px;
            font-size: 16px;
            font-weight: 600;
            cursor: pointer;
        }
        .btn:hover { transform: translateY(-2px); }
        .link { text-align: center; margin-top: 20px; color: #7f8c8d; }
        .link a { color: #667eea; text-decoration: none; font-weight: 600; }
        .flash {
            padding: 12px;
            border-radius: 8px;
            margin-bottom: 20px;
            text-align: center;
        }
        .flash-success { background: #d4edda; color: #155724; }
        .flash-error { background: #f8d7da; color: #721c24; }
        .services-info {
            text-align: center;
            margin-top: 20px;
            padding: 15px;
            background: #f8f9fa;
            border-radius: 8px;
            font-size: 12px;
            color: #6c757d;
        }
    </style>
</head>
<body>
    <div class="container">
        <h1>💇 Glamour Salon</h1>
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
                <input type="text" name="username" placeholder="Enter username" required>
            </div>
            <div class="form-group">
                <label>Password</label>
                <input type="password" name="password" placeholder="Enter password" required>
            </div>
            <button type="submit" class="btn">Login</button>
        </form>
        
        <div class="link">
            Don't have an account? <a href="{{ url_for('signup') }}">Create one</a>
        </div>
        
        <div class="services-info">
            ✂️ Haircut • 🎨 Hair Coloring • 💅 Manicure • 🦶 Pedicure • 
            🧖 Facial • 💆 Massage • 💄 Makeup • 🪒 Waxing
        </div>
    </div>
</body>
</html>
'''

SIGNUP_PAGE = '''
<!DOCTYPE html>
<html>
<head>
    <title>Glamour Salon - Sign Up</title>
    <style>
        * { margin: 0; padding: 0; box-sizing: border-box; }
        body {
            font-family: Arial, sans-serif;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            min-height: 100vh;
            display: flex;
            align-items: center;
            justify-content: center;
        }
        .container {
            background: white;
            padding: 40px;
            border-radius: 15px;
            box-shadow: 0 10px 30px rgba(0,0,0,0.3);
            width: 100%;
            max-width: 400px;
        }
        h1 { color: #2c3e50; text-align: center; }
        .subtitle { text-align: center; color: #7f8c8d; margin-bottom: 30px; }
        .form-group { margin-bottom: 20px; }
        label { display: block; margin-bottom: 5px; color: #34495e; font-weight: 600; }
        input {
            width: 100%;
            padding: 12px;
            border: 2px solid #e0e0e0;
            border-radius: 8px;
            font-size: 14px;
        }
        input:focus { outline: none; border-color: #667eea; }
        .btn {
            width: 100%;
            padding: 12px;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            color: white;
            border: none;
            border-radius: 8px;
            font-size: 16px;
            font-weight: 600;
            cursor: pointer;
        }
        .btn:hover { transform: translateY(-2px); }
        .link { text-align: center; margin-top: 20px; color: #7f8c8d; }
        .link a { color: #667eea; text-decoration: none; font-weight: 600; }
        .flash {
            padding: 12px;
            border-radius: 8px;
            margin-bottom: 20px;
            text-align: center;
        }
        .flash-success { background: #d4edda; color: #155724; }
        .flash-error { background: #f8d7da; color: #721c24; }
        .requirements { font-size: 12px; color: #6c757d; margin-top: 5px; }
    </style>
</head>
<body>
    <div class="container">
        <h1>✍️ Create Account</h1>
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
                <input type="text" name="username" placeholder="Choose username" required>
            </div>
            <div class="form-group">
                <label>Password</label>
                <input type="password" name="password" placeholder="Create password" required>
                <div class="requirements">Password must be at least 4 characters</div>
            </div>
            <div class="form-group">
                <label>Confirm Password</label>
                <input type="password" name="confirm" placeholder="Confirm password" required>
            </div>
            <button type="submit" class="btn">Sign Up</button>
        </form>
        
        <div class="link">
            Already have an account? <a href="{{ url_for('login') }}">Login</a>
        </div>
    </div>
</body>
</html>
'''

DASHBOARD_PAGE = '''
<!DOCTYPE html>
<html>
<head>
    <title>Glamour Salon - Dashboard</title>
    <style>
        * { margin: 0; padding: 0; box-sizing: border-box; }
        body { font-family: Arial, sans-serif; background: #f0f2f5; }
        .header {
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            color: white;
            padding: 20px 40px;
            display: flex;
            justify-content: space-between;
            align-items: center;
        }
        .btn {
            padding: 8px 20px;
            border: none;
            border-radius: 6px;
            font-size: 14px;
            font-weight: 600;
            cursor: pointer;
            text-decoration: none;
            display: inline-block;
        }
        .btn-success { background: #27ae60; color: white; }
        .btn-danger { background: #e74c3c; color: white; }
        .btn-success:hover { background: #229954; }
        .btn-danger:hover { background: #c0392b; }
        .container { max-width: 1200px; margin: 30px auto; padding: 0 20px; }
        .actions { display: flex; gap: 15px; margin-bottom: 30px; }
        .card {
            background: white;
            border-radius: 10px;
            padding: 25px;
            box-shadow: 0 2px 10px rgba(0,0,0,0.05);
        }
        .card h2 { color: #2c3e50; margin-bottom: 20px; }
        table { width: 100%; border-collapse: collapse; }
        th {
            background: #f8f9fa;
            padding: 12px;
            text-align: left;
            border-bottom: 2px solid #e0e0e0;
        }
        td {
            padding: 12px;
            border-bottom: 1px solid #e0e0e0;
        }
        .badge {
            display: inline-block;
            padding: 3px 10px;
            border-radius: 20px;
            font-size: 12px;
            font-weight: 600;
        }
        .badge-active { background: #d4edda; color: #155724; }
        .badge-cancelled { background: #f8d7da; color: #721c24; }
        .no-data { text-align: center; padding: 40px; color: #7f8c8d; }
        .flash {
            padding: 12px 20px;
            border-radius: 8px;
            margin-bottom: 20px;
        }
        .flash-success { background: #d4edda; color: #155724; }
        .flash-error { background: #f8d7da; color: #721c24; }
        .footer { text-align: center; margin-top: 40px; padding: 20px; color: #7f8c8d; }
        .user { font-size: 14px; opacity: 0.9; }
        @media (max-width: 768px) {
            .header { flex-direction: column; gap: 10px; text-align: center; }
            .actions { flex-direction: column; }
            .actions .btn { width: 100%; text-align: center; }
        }
    </style>
</head>
<body>
    <div class="header">
        <h1>💇 Glamour Salon</h1>
        <div>
            <span class="user">👋 Welcome, {{ username }}!</span>
            <a href="{{ url_for('logout') }}" class="btn btn-danger">Logout</a>
        </div>
    </div>
    
    <div class="container">
        {% with messages = get_flashed_messages(with_categories=true) %}
            {% if messages %}
                {% for category, message in messages %}
                    <div class="flash flash-{{ category }}">{{ message }}</div>
                {% endfor %}
            {% endif %}
        {% endwith %}
        
        <div class="actions">
            <a href="{{ url_for('book') }}" class="btn btn-success">📅 Book New Appointment</a>
        </div>
        
        <div class="card">
            <h2>📋 Your Appointments</h2>
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
                            <td>{{ app.service }}</td>
                            <td>{{ app.date }}</td>
                            <td>{{ app.time }}</td>
                            <td><span class="badge badge-{{ app.status }}">{{ app.status }}</span></td>
                            <td>
                                {% if app.status == 'active' %}
                                    <a href="{{ url_for('cancel', id=app.id) }}" class="btn btn-danger" style="padding: 5px 12px; font-size: 12px;" onclick="return confirm('Cancel this appointment?')">Cancel</a>
                                {% else %}
                                    <span style="color: #7f8c8d; font-size: 12px;">Cancelled</span>
                                {% endif %}
                            </td>
                        </tr>
                        {% endfor %}
                    {% else %}
                        <tr>
                            <td colspan="5">
                                <div class="no-data">
                                    No appointments booked yet.<br>
                                    <a href="{{ url_for('book') }}" class="btn btn-success" style="margin-top: 10px;">Book your first appointment</a>
                                </div>
                            </td>
                        </tr>
                    {% endif %}
                </tbody>
            </table>
        </div>
        
        <div class="footer">
            <p>💇 Glamour Salon - Your beauty, our priority</p>
        </div>
    </div>
</body>
</html>
'''

BOOK_PAGE = '''
<!DOCTYPE html>
<html>
<head>
    <title>Glamour Salon - Book Appointment</title>
    <style>
        * { margin: 0; padding: 0; box-sizing: border-box; }
        body {
            font-family: Arial, sans-serif;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            min-height: 100vh;
            display: flex;
            align-items: center;
            justify-content: center;
            padding: 20px;
        }
        .container {
            background: white;
            padding: 40px;
            border-radius: 15px;
            box-shadow: 0 10px 30px rgba(0,0,0,0.3);
            width: 100%;
            max-width: 500px;
        }
        h1 { color: #2c3e50; text-align: center; }
        .subtitle { text-align: center; color: #7f8c8d; margin-bottom: 30px; }
        .form-group { margin-bottom: 20px; }
        label { display: block; margin-bottom: 5px; color: #34495e; font-weight: 600; }
        select, input {
            width: 100%;
            padding: 12px;
            border: 2px solid #e0e0e0;
            border-radius: 8px;
            font-size: 14px;
        }
        select:focus, input:focus { outline: none; border-color: #667eea; }
        .btn {
            width: 100%;
            padding: 12px;
            background: linear-gradient(135deg, #27ae60 0%, #2ecc71 100%);
            color: white;
            border: none;
            border-radius: 8px;
            font-size: 16px;
            font-weight: 600;
            cursor: pointer;
        }
        .btn:hover { transform: translateY(-2px); }
        .btn-secondary {
            background: linear-gradient(135deg, #6c757d 0%, #495057 100%);
            margin-top: 10px;
        }
        .link { text-align: center; margin-top: 20px; color: #7f8c8d; }
        .link a { color: #667eea; text-decoration: none; font-weight: 600; }
        .flash {
            padding: 12px;
            border-radius: 8px;
            margin-bottom: 20px;
            text-align: center;
        }
        .flash-success { background: #d4edda; color: #155724; }
        .flash-error { background: #f8d7da; color: #721c24; }
        .date-hint { font-size: 12px; color: #6c757d; margin-top: 5px; }
    </style>
</head>
<body>
    <div class="container">
        <h1>📅 Book Appointment</h1>
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
                <label>Service</label>
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
            
            <div class="form-group">
                <label>Date</label>
                <input type="text" name="date" value="{{ today }}" placeholder="YYYY-MM-DD" required>
                <div class="date-hint">Format: YYYY-MM-DD (e.g., 2026-07-09)</div>
            </div>
            
            <div class="form-group">
                <label>Time</label>
                <input type="text" name="time" value="10:00" placeholder="HH:MM" required>
                <div class="date-hint">Format: HH:MM (24-hour, e.g., 14:30)</div>
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
            flash(f'Welcome back, {username}!', 'success')
            return redirect(url_for('dashboard'))
        else:
            flash('Invalid username or password', 'error')
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
        
        flash(f'Account created! Please login, {username}', 'success')
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
