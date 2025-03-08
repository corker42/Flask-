from flask import Flask, request, redirect, abort
import click
app = Flask(__name__)

@app.route('/')
def home():
    return f"Hello, World! {g.name}"

@app.route('/goback/<int:year>')
def greet_and_go_back(year):
    current_year = 2025
    age = current_year - year
    return f"<h1>Hello, human! You are {age} years old.<h1>"

colors = ['Red', 'Blue', 'Green', 'Purple', 'Orange', 'Pink', 'Cyan', 'Magenta', 'Brown', 'Gray', 'Black']
@app.route(f'/color/<any({",".join(colors)}):color>')
def color_page(color):
    return f'''
    <h1 style="color: {color.lower()}">
        The color is {color}!
    </h1>
    '''

@app.route('/re')
def hello1():
    # return '', 302, {'Location': 'https://www.bilibili.com/'}
    return redirect('https://www.bilibili.com/')

@app.cli.command()
def hello():
    click.echo("Hello, Human!")

@app.route('/404')
def not_found():
    abort(404)

from flask import make_response, url_for, session
import os
app.secret_key = os.getenv('SECRET_KEY', 'this-is-a-secret-key')

@app.route('/hello')
def hello_world():
    name = request.args.get('name')
    if name is None:
        name = request.cookies.get('name', 'World')
    # 获取 session 中的信息
    logged_in = session.get('logged_in', False)
    session_data = dict(session)  # 将 session 转为字典方便展示
        # # 构建响应内容
        # return f"""
        # <h1>Hello, {name}!</h1>
        # <h3>Session 信息：</h3>
        # <ul>
        #     <li>登录状态：{'已登录' if logged_in else '未登录'}</li>
        #     <li>Session 内容：{session_data}</li>
        # </ul>
        # """
    response = f"<h1>Hello, {name}!</h1>"
    # 根据用户认证状态返回不同的内容
    if 'logged_in' in session:
        response += '[Authenticated]'
    else:
        response += '[Not Authenticated]'
    return response

@app.route('/set/<name>')
def set_cookie(name):
    response = make_response(redirect(url_for('hello_world')))
    response.set_cookie('name', name)
    return response

@app.route('/login')
def login():
    session['logged_in'] = True
    return redirect(url_for('hello_world'))

@app.route('/admin')
def admin():
    if 'logged_in' not in session:
        abort(403)
    return 'Welcome to admin page.'

@app.route('/logout')
def logout():
    if 'logged_in' in session:
        session.pop('logged_in')
    return redirect(url_for('hello_world'))

from flask import g

@app.before_request
def get_name():
    g.name = request.args.get('name')
import time
@app.route('/foo')
def foo():
    return f'<h1>Foo page</h1><a href="{url_for("do_something", next=request.full_path)}">Do something and redirect</a>'

@app.route('/bar')
def bar():
    return f'<h1>Bar page</h1><a href="{url_for("do_something", next=request.full_path)}">Do something and redirect</a>'

def redirect_back(default='hello_world', **kwargs):
    for target in request.args.get('next'), request.referrer:
        if not target:
            continue
        if is_safe_url(target):
            return redirect(target)
    return redirect(url_for(default, **kwargs))

@app.route('/do_something_and_redirect')
def do_something():
    # do something
    # 获取 next 参数的值
    next_param = request.args.get('next')
    # 获取请求来源页面
    referrer = request.referrer

    # 打印 next 参数和请求来源页面
    print(f"Next 参数的值: {next_param}")
    print(f"请求来源页面: {referrer}")
    time.sleep(1)  # 模拟一个需要跳转的操作
    return redirect_back()

from urllib.parse import urlparse, urljoin

def is_safe_url(target):
    ref_url = urlparse(request.host_url)
    test_url = urlparse(urljoin(request.host_url, target))
    return test_url.scheme in ('http', 'https') and ref_url.netloc == test_url.netloc
