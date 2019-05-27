from flask import Flask, render_template, redirect, url_for
from flask_socketio import SocketIO,emit

async_mode = None
app = Flask(__name__)
app.config['SECRET_KEY'] = 'secret!'
socketio = SocketIO(app,async_mode=async_mode)


# 登入頁面
@app.route('/')
def index():
    return render_template('index.html', async_mode=socketio.async_mode)

# 主夜面
@app.route('/index1')
def index1():
	return render_template('index1.html', async_mode=socketio.async_mode)

# 使用者名稱登入
@socketio.on('user_login',namespace='/test')
def login(name):
	global json_username
	json_username = name['username'].encode('latin-1').decode('utf-8')
	emit('redirect', {'url': url_for('index1')})


# 回傳使用者名稱
@socketio.on('login_username',namespace='/test')
def get_username():
	user_name=json_username
	emit('get_username',user_name)


# 主聊天室
@socketio.on('major_chat', namespace='/test')
def test_message(message):
    # print('123')
    json_data = message['data'].encode('latin-1').decode('utf-8')
    major_name=	message['user_name'].encode('latin-1').decode('utf-8')
    emit('major_response',{'data':json_data,'user_name':major_name },broadcast=True)


#閒聊聊天室
@socketio.on('gossip_chat', namespace='/test')
def test_message(message):
    json_data = message['data'].encode('latin-1').decode('utf-8')
    gossip_name=message['user_name'].encode('latin-1').decode('utf-8')
    emit('gossip_response',{'data':json_data,'user_name':gossip_name},broadcast=True)



	
if __name__ == '__main__':
    socketio.run(app,debug=True)