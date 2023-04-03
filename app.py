from flask import Flask, request, render_template, redirect, session
from werkzeug.security import generate_password_hash, check_password_hash

app = Flask(__name__)
app.secret_key = 'mysecretkey'

users = {}

folders = '/folders/'

@app.route('/')
def index():
    return render_template('index.html')

#注册
@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
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
def dashboard():
    if 'username' not in session:
        return redirect('/')
    return render_template('dashboard.html', username=session['username'])

#登出
@app.route('/logout')
def logout():
    session.pop('username', None)
    return redirect('/')

#创建文件夹
@app.route('/create', methods=['GET', 'POST'])
def create():
    if 'username' not in session:
        return redirect('/')
    if request.method == 'POST':
        foldername = request.form['foldername']
        if not foldername:
            return render_template('create.html', message='请填写完整信息')
        if foldername in folders:
            return render_template('create.html', message='该文件夹已存在')
        folders[foldername] = []
        return redirect('/dashboard')
    return render_template('create.html')

#删除文件夹
@app.route('/delete', methods=['GET', 'POST'])
def delete():
    if 'username' not in session:
        return redirect('/')
    if request.method == 'POST':
        foldername = request.form['foldername']
        if not foldername:
            return render_template('delete.html', message='请填写完整信息')
        if foldername not in folders:
            return render_template('delete.html', message='该文件夹不存在')
        folders.pop(foldername)
        return redirect('/dashboard')
    return render_template('delete.html')

#上传文件
@app.route('/upload', methods=['GET', 'POST'])
def upload():
    if 'username' not in session:
        return redirect('/')
    if request.method == 'POST':
        foldername = request.form['foldername']
        filename = request.form['filename']
        if not foldername or not filename:
            return render_template('upload.html', message='请填写完整信息')
        if foldername not in folders:
            return render_template('upload.html', message='该文件夹不存在')
        folders[foldername].append(filename)
        return redirect('/dashboard')
    return render_template('upload.html')

#下载文件
@app.route('/download', methods=['GET', 'POST'])
def download():
    if 'username' not in session:
        return redirect('/')
    if request.method == 'POST':
        foldername = request.form['foldername']
        filename = request.form['filename']
        if not foldername or not filename:
            return render_template('download.html', message='请填写完整信息')
        if foldername not in folders:
            return render_template('download.html', message='该文件夹不存在')
        if filename not in folders[foldername]:
            return render_template('download.html', message='该文件不存在')
        return render_template('download.html', message='下载成功')
    return render_template('download.html')

#删除文件
@app.route('/deletefile', methods=['GET', 'POST'])
def deletefile():
    if 'username' not in session:
        return redirect('/')
    if request.method == 'POST':
        foldername = request.form['foldername']
        filename = request.form['filename']
        if not foldername or not filename:
            return render_template('deletefile.html', message='请填写完整信息')
        if foldername not in folders:
            return render_template('deletefile.html', message='该文件夹不存在')
        if filename not in folders[foldername]:
            return render_template('deletefile.html', message='该文件不存在')
        folders[foldername].remove(filename)
        return redirect('/dashboard')
    return render_template('deletefile.html')

#查看文件
@app.route('/view', methods=['GET', 'POST'])
def view():
    if 'username' not in session:
        return redirect('/')
    if request.method == 'POST':
        foldername = request.form['foldername']
        filename = request.form['filename']
        if not foldername or not filename:
            return render_template('view.html', message='请填写完整信息')
        if foldername not in folders:
            return render_template('view.html', message='该文件夹不存在')
        if filename not in folders[foldername]:
            return render_template('view.html', message='该文件不存在')
        return render_template('view.html', message='查看成功')
    return render_template('view.html')



if __name__ == '__main__':
    app.run(debug=True)
