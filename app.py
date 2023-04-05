import os
from flask import Flask, request, render_template, redirect, session, make_response, send_from_directory, flash
from werkzeug.security import generate_password_hash, check_password_hash
from flask_httpauth import HTTPBasicAuth
import mysql.connector as connector


# 连接数据库
db_netdisk = connector.connect(
    host="localhost",
    port="3306",
    username = "root",
    password = "root",
    database = "netdisk"
)

# 创建游标
cousor = db_netdisk.cursor()

app = Flask(__name__)
app.secret_key = 'mysecretkey'

# 设置文件夹路径
folders = 'folders/'

# 设置登录验证
auth = HTTPBasicAuth()
@auth.verify_password
def verify_password(username, password):
    # 读取数据库的用户信息
    cousor.execute('use netdisk')
    cousor.execute('select * from user')
    userlist = cousor.fetchall()
    users = {}
    for i in userlist:
        users[i[0]] = i[1]

    # 如果用户名不存在，返回False
    if username not in users:
        return False
    # 如果密码不正确，返回False
    if not check_password_hash(users.get(username), password):
        return False
    return True


@app.route('/')
def index():
    if 'username' in session:
        return render_template('home.html', username = auth.username())
    return render_template('index.html')

#注册
@app.route('/register', methods=['GET', 'POST'])
def register():

    # 读取数据库的用户信息
    cousor.execute('use netdisk')
    cousor.execute('select * from user')
    userlist = cousor.fetchall()
    users = {} 
    for i in userlist:
        users[i[0]] = i[1]

    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        # 如果数据库中有该用户，返回无法注册
        if username in users:
            return render_template('register.html', message='该用户已存在')
        # 如果用户名或密码为空，返回无法注册
        if not username or not password:
            return render_template('register.html', message='请填写完整信息')
        # 将用户名和密码加密后存入数据库
        users[username] = generate_password_hash(password)
        cousor.execute('insert into user values(%s, %s)', (username, users[username]))
        db_netdisk.commit()
        return redirect('/login')
    return render_template('register.html')

# logout
@app.route('/logout')
@auth.login_required
def logout():
    return redirect('/')

# 登录
@app.route('/login')
@auth.login_required
def home():
    # 获取文件列表
    cousor.execute('select * from file where username = %s',(auth.username(),))
    files = cousor.fetchall()
    fileslist = []
    for i in files:
        items = {'filename':i[1], 'filepath':i[2]}
        fileslist.append(items)
    
    return render_template('home.html',files = fileslist)
        
# 上传文件
@app.route('/upload', methods=['GET', 'POST'])
@auth.login_required
def upload():
    # 获取这个用户的文件列表
    pass
 
    # 获取上传的文件
    file = request.files['file']
    if request.method == 'POST':
        # 将文件存入数据库
        # 获取文件的保存路径，并将路径保存到数据库中
        filepath = folders + file.filename
        cousor.execute('insert into file values(%s, %s, %s)', (auth.username(),file.filename, filepath, ))
        db_netdisk.commit()
        # 将文件存入文件夹
        file.save(filepath)
        return render_template('home.html',username = auth.username(), files = file.filename, message='上传成功')
    redirect('/')
    return render_template('home.html',username = auth.username(), files = file.filename, message='上传失败')
        
# 下载文件
@app.route('/download/<filename>')
@auth.login_required
def download(filename):
    # debug
    print(filename)
    # 获取这个用户的文件
    cousor.execute('select filepath from file where username = %s and filename = %s', (auth.username(), filename))
    filepath = cousor.fetchone()
    print(filepath)

    
    #测试
    
    # 将文件下载
    directory = folders # 修改为你的文件存储目录
    return send_from_directory(directory, filename, as_attachment=True)

# 删除文件
@app.route('/delete/<filename>')
@auth.login_required
def delete(filename):
    # 获取这个用户的文件
    files = cousor.execute('delete from file where username = %s and filename = %s', (auth.username(), filename))
    db_netdisk.commit()
    # 将文件从文件夹中删除
    import os
    os.remove(folders + filename)
    redirect(request.url)
    return render_template('home.html',username = auth.username(), files = files, message='删除成功')


if __name__ == '__main__':
    app.run(debug=True)
