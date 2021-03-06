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
    # All agents will join here
    join_room('agents_room')
    f_agents= agents +1
    emit('agent_connected',{'data': 'Agents connected'},room='agents_room' )





@socket_.on('new_client', namespace='/test')
def new_client(message):
    #Join client room

    client_id = message['client_id']
    join_room('clients_room')
    emit('client_connected',{'data': 'Clients connected'+client_id ,'client_id':client_id},room='clients_room')

# @socket_.on('my_event', namespace='/test')
# def test_message(message):
#     session={'receive_count':1}
#     session['receive_count'] = 1
#     emit('my_response',
#          {'data': message['data'], 'count': session['receive_count']})


@socket_.on('need_support', namespace='/test')
def need_support(message):
    # Event will trigger support notification in agents room
    #fetching client user id
    #print('-------------------------')
    client_id = message['client_id']
   
    
    join_room(client_id)
    #emit('provide_support_all_agents',{'data': 'Agents connected'},room='agents_room' )
    #emit('provide_support_all_agents',{'data':'sdf'})

    # Emit support team pop up to provide support.
    emit('provide_support_all_agents',{'data': message['data']},room='agents_room')



@socket_.on('support_confirmed', namespace='/test')
def support_confirmed(message):
    # Event will trigger support notification in agents room
    #fetching client user id
    client_id = message['client_id']
    leave_room('agents_room')
    join_room(client_id)

    # Emit support team pop up to provide support.
    emit('setup_private_conversation',{'data': 'I Can help you'},room=client_id)

@socket_.on('private_conversation', namespace='/test')
def private_conversation(message):
    # Event will trigger support notification in agents room
    #fetching client user id
    client_id = message['client_id']
    
    # Emit support team pop up to provide support.
    emit('private_conversation',{'data': message['data']},room=client_id ,include_self=False)


@socket_.on('disconnect_private_conversation', namespace='/test')
def disconnect_private_conversation(message):
    # Event will trigger support notification in agents room
    #fetching client user id
    client_id = message['client_id']
    
    # Emit support team pop up to provide support.
    emit('leave_private_conversation',{'data':'Disconnect...'},room=client_id,include_self=False)
    #leave_room(client_id)

@socket_.on('my_broadcast_event', namespace='/test')
def test_broadcast_message(message):

    emit('my_response',{'data': message['data']},broadcast=True)


if __name__ == '__main__':
    socket_.run(app, debug=True,port=8000)