from flask import Flask, render_template, request, redirect, url_for, session, jsonify
import os
import json

app = Flask(__name__)
app.secret_key = 'your_secret_key_here'  # 设置会话密钥

# 数据存储文件
DATA_FILE = 'christmas_trees.json'

# 初始化数据文件
if not os.path.exists(DATA_FILE):
    with open(DATA_FILE, 'w') as f:
        json.dump({}, f)

# 登录验证
@app.route('/', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        if username == 'test' and password == 'admin':
            session['logged_in'] = True
            return redirect(url_for('christmas_tree'))
        else:
            return render_template('login.html', error='账号或密码错误')
    return render_template('login.html')

# 圣诞树生成页面
@app.route('/christmas-tree', methods=['GET', 'POST'])
def christmas_tree():
    if not session.get('logged_in'):
        return redirect(url_for('login'))
    
    if request.method == 'POST':
        name = request.form.get('name', '').strip()
        if name:
            # 保存数据
            with open(DATA_FILE, 'r') as f:
                data = json.load(f)
            data[name] = {'name': name}
            with open(DATA_FILE, 'w') as f:
                json.dump(data, f, indent=4)
            return render_template('christmas_tree.html', name=name)
    
    return render_template('christmas_tree.html')

# 检查姓名是否已存在
@app.route('/check-name', methods=['POST'])
def check_name():
    name = request.form.get('name', '').strip()
    if not name:
        return jsonify({'exists': False})
    
    with open(DATA_FILE, 'r') as f:
        data = json.load(f)
    
    return jsonify({'exists': name in data})

# 获取已保存的姓名列表
@app.route('/get-names', methods=['GET'])
def get_names():
    with open(DATA_FILE, 'r') as f:
        data = json.load(f)
    return jsonify(list(data.keys()))

# 退出登录
@app.route('/logout')
def logout():
    session.pop('logged_in', None)
    return redirect(url_for('login'))

if __name__ == '__main__':
    app.run(debug=True, port=5001, host='0.0.0.0')
