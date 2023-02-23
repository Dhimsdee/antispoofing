from flask import Flask, request, render_template, Response
import aktif

app = Flask(__name__)

@app.route("/activenessnet")
def activenessnet():
    def generate():
        while True:
            frame = aktif.capture_frame()
            liveness = aktif.activenessnet(frame)
            yield (b'--frame\r\n'
                   b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n\r\n')
    return Response(generate(),
                    mimetype='multipart/x-mixed-replace; boundary=frame')

if __name__ == "__main__":
    app.run(debug=True)