# Flask app
from flask import Flask, jsonify, render_template, request, Response
from flask_cors import CORS
from main import livenessnet
from camera import VideoCamera
from flask_socketio import SocketIO, emit

app = Flask(__name__)
CORS(app)

app.config['SECRET_KEY'] = 'secret!'
socketio = SocketIO(app)

video_camera = None
global_frame = None

@app.route('/')
def gen(camera):
    while True:
        frame = camera.get_frame()
        yield (b'--frame\r\n'
               b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n\r\n')

@app.route('/video_feed')
def video_feed():
    return Response(gen(VideoCamera()), mimetype='multipart/x-mixed-replace; boundary=frame')

@socketio.on('connect')
def on_connect():
    global video_camera
    video_camera = VideoCamera()
    print('Client connected')

@socketio.on('disconnect')
def on_disconnect():
    global video_camera
    video_camera.stop()
    print('Client disconnected')

@socketio.on('request_frame')
def request_frame():
    global video_camera, global_frame
    if video_camera != None:
        global_frame = video_camera.get_frame()
    emit('response_frame', {'data': global_frame})

@app.route('/livenessnet', methods=['POST'])
def liveness_detection():
    data = request.json
    modelPath = data['modelPath']
    le_path = data['le_path']
    detector_folder = data['detector_folder']
    confidence = data.get('confidence', 0.5)
    label = livenessnet(modelPath, le_path, detector_folder, confidence)
    response = {
        'label': label
    }
    return jsonify(response)

if __name__ == '__main__':
    socketio.run(app, debug=True)