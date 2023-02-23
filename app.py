# Flask app
from flask import Flask, request, jsonify, Response
from flask_cors import CORS
from livenessnet.pasif import livenessnet
from activenessnet.aktif import capture_frame, activenessnet
import cv2

app = Flask(__name__)
CORS(app)

def generate_frames():
    cap = cv2.VideoCapture(0)
    while True:
        success, frame = cap.read()
        if not success:
            break
        else:
            ret, buffer = cv2.imencode('.jpg', frame)
            frame = buffer.tobytes()
            yield (b'--frame\r\n'
                    b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')

@app.route('/video_feed')
def video_feed():
    return Response(generate_frames(), mimetype='multipart/x-mixed-replace; boundary=frame')

@app.route('/livenessnet', methods=['POST'])
def liveness_detection():
    data = request.json
    model_Path = data['model_Path']
    le_path = data['le_path']
    detector_folder = data['detector_folder']
    confidence = data['confidence'] 
    label = livenessnet(model_Path, le_path, detector_folder, confidence)
    response = {
        'label': label
    }
    return jsonify(response)

@app.route("/activenessnet", methods=['POST'])
def activenessnet():
    def generate():
        while True:
            frame = capture_frame()
            liveness = activenessnet(frame)
            yield (b'--frame\r\n'
                   b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n\r\n')
    return Response(generate(),
                    mimetype='multipart/x-mixed-replace; boundary=frame')

if __name__ == '__main__':
    app.run(debug=True)