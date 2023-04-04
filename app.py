from flask import Flask, request, render_template, redirect, session
from werkzeug.security import generate_password_hash, check_password_hash
from flask_httpauth import HTTPBasicAuth
import pymysql

# 连接数据库



app = Flask(__name__)
app.secret_key = 'mysecretkey'

users = {}

folders = '/folders/'

auth = HTTPBasicAuth()

@app.route('/')
def index():
    return render_template('index.html')

#注册
@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        # 从数据中获取用户信息
        # user = User.query.filter_by(username=username).first()
        # if user:
        #     return render_template('register.html', message='该用户名已被注册')


        if not username or not password:
            return render_template('register.html', message='请填写完整信息')
        if username in users:
            return render_template('register.html', message='该用户名已被注册')
        users[username] = generate_password_hash(password)
        session['username'] = username
        return redirect('/dashboard')
    return render_template('register.html')

#登录
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        if not username or not password:
            return render_template('login.html', message='请填写完整信息')
        if username not in users:
            return render_template('login.html', message='用户名不存在')
        if not check_password_hash(users[username], password):
            return render_template('login.html', message='密码不正确')
        session['username'] = username
        return redirect('/dashboard')
    return render_template('login.html')

#主页
@app.route('/dashboard')
@auth.login_required
def dashboard():
    if 'username' not in session:
        return redirect('/')
    return render_template('dashboard.html', username=session['username'])

#登出
@app.route('/logout')
def logout():
    session.pop('username', None)
    return redirect('/')

#验证
@auth.verify_password
def verify_password(username, password):
    if username in users:
        return check_password_hash(users.get(username), password)
    return False


if __name__ == '__main__':
    app.run(debug=True)
