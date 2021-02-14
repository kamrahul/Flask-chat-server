from flask import Flask, render_template
from flask_socketio import SocketIO
from flask_socketio import SocketIO, emit, disconnect
from flask_socketio import join_room, leave_room

async_mode = None
app = Flask(__name__)
socket_ = SocketIO(app,  cors_allowed_origins="*",async_mode=async_mode)

agents=0
clients=0

@app.route('/')
def index():
    return render_template('index.html',
                           sync_mode=socket_.async_mode)



@socket_.on('new_agent', namespace='/test')
def new_agent(message):
    join_room('agents_room')
    f_agents= agents +1
    emit('my_response',{'data': 'Agents connected'} )


@socket_.on('new_client', namespace='/test')
def new_client(message):
    #Join client room
    join_room('clients_room')

    emit('my_response',{'data': 'Clients connected'})

@socket_.on('my_event', namespace='/test')
def test_message(message):
    session={'receive_count':1}
    session['receive_count'] = 1
    emit('my_response',
         {'data': message['data'], 'count': session['receive_count']})


@socket_.on('send_support', namespace='/test')
def send_support(message):
    #fetching client user id
    client_id = message['client_id']
    join_room(client_id)

    emit('provide_support',{'data': message['data']},room='agents_room')


@socket_.on('my_broadcast_event', namespace='/test')
def test_broadcast_message(message):

    emit('my_response',{'data': message['data']},broadcast=True)


if __name__ == '__main__':
    socket_.run(app, debug=True,port=8000)