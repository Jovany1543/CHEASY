from flask import Blueprint, render_template_string, request, redirect, make_response, jsonify
import os

dashboard_bp = Blueprint('dashboard', __name__)

ADMIN_PASSWORD = os.getenv('ADMIN_PASSWORD')
base_url = os.getenv('BACKEND_URL')

LOGIN_TEMPLATE = '''
<!DOCTYPE html>
<html>
<head>
    <title>CHEASY Admin Login</title>
    <style>
        body { font-family: Arial, sans-serif; display: flex; justify-content: center; align-items: center; height: 100vh; margin: 0; background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); }
        .container { background: white; padding: 40px; border-radius: 10px; box-shadow: 0 10px 25px rgba(0,0,0,0.2); width: 300px; }
        h1 { text-align: center; color: #333; }
        input { width: 100%; padding: 10px; margin: 10px 0; border: 1px solid #ddd; border-radius: 5px; box-sizing: border-box; }
        button { width: 100%; padding: 10px; background: #667eea; color: white; border: none; border-radius: 5px; cursor: pointer; font-weight: bold; }
        button:hover { background: #764ba2; }
        .error { color: red; text-align: center; margin-bottom: 10px; }
    </style>
</head>
<body>
    <div class="container">
        <h1>CHEASY Admin</h1>
        {% if error %}<div class="error">{{ error }}</div>{% endif %}
        <form method="POST">
            <input type="password" name="password" placeholder="Password" required autofocus>
            <button type="submit">Login</button>
        </form>
    </div>
</body>
</html>
'''

DASHBOARD_TEMPLATE = '''
<!DOCTYPE html>
<html>
<head>
    <title>CHEASY Backend Dashboard</title>
    <style>
        body { font-family: Arial, sans-serif; margin: 0; background: #f5f5f5; }
        .navbar { background: #333; color: white; padding: 15px; display: flex; justify-content: space-between; align-items: center; }
        .container { max-width: 1000px; margin: 20px auto; padding: 20px; }
        h1 { color: #333; }
        .section { background: white; padding: 20px; margin: 20px 0; border-radius: 8px; box-shadow: 0 2px 4px rgba(0,0,0,0.1); }
        .section h2 { color: #667eea; margin-top: 0; }
        .endpoint-list { list-style: none; padding: 0; }
        .endpoint-list li { padding: 10px; background: #f9f9f9; margin: 5px 0; border-left: 4px solid #667eea; border-radius: 3px; }
        .endpoint-list a { color: #667eea; text-decoration: none; font-weight: bold; }
        .endpoint-list a:hover { text-decoration: underline; }
        .admin-link { display: inline-block; margin: 10px 0; padding: 10px 20px; background: #667eea; color: white; text-decoration: none; border-radius: 5px; }
        .admin-link:hover { background: #764ba2; }
        .logout { background: #e74c3c; }
        .logout:hover { background: #c0392b; }
    </style>
</head>
<body>
    <div class="navbar">
        <h1>CHEASY Backend Dashboard</h1>
        <div>
            <a href="{{ base_url }}/admin/" class="admin-link">Admin Panel</a>
            <a href="/admin-logout" class="admin-link logout">Logout</a>
        </div>
    </div>
    
    <div class="container">
        <div class="section">
            <h2>Public Endpoints (No Auth Required)</h2>
            <ul class="endpoint-list">
                <li><a href="{{ base_url }}/api/ping" target="_blank">GET /api/ping</a> - Health check</li>
                <li><a href="{{ base_url }}/api/users" target="_blank">GET /api/users</a> - List all users</li>
            </ul>
        </div>

        <div class="section">
            <h2>Auth Endpoints</h2>
            <ul class="endpoint-list">
                <li><strong>POST /api/auth/register</strong> - Register new user</li>
                <li><strong>POST /api/auth/login</strong> - Login and get JWT token</li>
                <li><strong>GET /api/auth/protected</strong> - Protected endpoint (JWT required)</li>
            </ul>
        </div>

        <div class="section">
            <h2>Items Endpoints (JWT Required)</h2>
            <ul class="endpoint-list">
                <li><strong>GET /api/items</strong> - List all items</li>
                <li><strong>POST /api/items</strong> - Create new item</li>
            </ul>
        </div>

        <div class="section">
            <h2>Database Management</h2>
            <p><a href="{{ base_url }}/admin/" class="admin-link">Go to Admin Panel</a> - Manage users and items in the database</p>
        </div>
    </div>
</body>
</html>
'''

@dashboard_bp.route('/', methods=['GET'])
def index():
    # Check if user is authenticated
    if request.cookies.get('admin_authenticated'):
        return render_template_string(DASHBOARD_TEMPLATE, base_url=base_url)
    return redirect('/admin-login')

@dashboard_bp.route('/admin-login', methods=['GET', 'POST'])
def admin_login():
    error = None
    if request.method == 'POST':
        password = request.form.get('password', '')
        if password == ADMIN_PASSWORD:
            response = make_response(redirect('/'))
            response.set_cookie('admin_authenticated', 'true', max_age=86400)  # 24 hours
            return response
        else:
            error = 'Invalid password'
    
    return render_template_string(LOGIN_TEMPLATE, error=error)

@dashboard_bp.route('/admin-logout', methods=['GET'])
def admin_logout():
    response = make_response(redirect('/admin-login'))
    response.delete_cookie('admin_authenticated')
    return response
