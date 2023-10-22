from flask import Flask, render_template
from flask_mqtt import Mqtt
from flask_socketio import SocketIO, send, emit
app = Flask(__name__)
app.config['SECRET'] = 'my secret key'
app.config['TEMPLATES_AUTO_RELOAD'] = True
app.config['MQTT_BROKER_URL'] = 'broker.hivemq.com'
app.config['MQTT_BROKER_PORT'] = 1883
app.config['MQTT_USERNAME'] = ''
app.config['MQTT_PASSWORD'] = ''
app.config['MQTT_KEEPALIVE'] = 5
app.config['MQTT_TLS_ENABLED'] = False
app.config['MQTT_CLEAN_SESSION'] = True

mqtt = Mqtt(app)
socketio = SocketIO(app)
tmpData = ""
@app.route('/')
def index():
    return render_template('index.html')

#MQTT
@mqtt.on_connect()
def handle_connect(client, userdata, flags, rc):
        mqtt.subscribe('home/Pub')

@mqtt.on_message()
def handle_mqtt_message(client, userdata, message):
    data = dict(
        topic=message.topic,
        payload=message.payload.decode()
    )
    socketio.emit('receive', data['payload'])
    print(data['payload'])
    global tmpData
    tmpData = data['payload']

# Socket
@socketio.on('event') 
def handle_event(message):
    print('Received event: ' + str(message))
    if "Connected" in str(message):
         socketio.emit('receive', tmpData)
@socketio.on('send')
def handle_receive(message):
     print('Receive from client: '+ str(message))

@socketio.on_error() 
def handle_error(error):
    return render_template('404.html'), 404

if __name__ == '__main__':
    socketio.run(app, use_reloader=False, debug=True)