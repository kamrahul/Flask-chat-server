from flask import Flask, render_template
from flask_socketio import SocketIO
from flask_socketio import SocketIO, emit, disconnect
async_mode = None
app = Flask(__name__)
socket_ = SocketIO(app,  cors_allowed_origins="*",async_mode=async_mode)
@app.route('/')
def index():
    return render_template('index.html',
                           sync_mode=socket_.async_mode)


@socket_.on('my_event', namespace='/test')
def test_message(message):
    session={'receive_count':1}
    session['receive_count'] = 1
    emit('my_response',
         {'data': message['data'], 'count': session['receive_count']})


if __name__ == '__main__':
    socket_.run(app, debug=True,port=8000)