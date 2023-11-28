from flask import Flask, render_template, Response
import cv2
import threading
import time

app = Flask(__name__)
@app.route('/js/<path:filename>')
def serve_js(filename):
    return send_from_directory('static/js', filename)
class VideoRecorder:
    def __init__(self):
        self.camera = cv2.VideoCapture(0)
        self.recording = False
        self.fourcc = cv2.VideoWriter_fourcc(*'mp4v')  # Changement de codec en mp4v
        self.out = None
        self.record_interval = 4  # Intervalle d'enregistrement en secondes
        self.last_record_time = time.time()

    def start_recording(self):
        self.recording = True
        while self.recording:
            current_time = time.time()
            if current_time - self.last_record_time >= self.record_interval:
                self.out = cv2.VideoWriter(f'output_{int(current_time)}.mp4', self.fourcc, 20.0, (640, 480))
                success, frame = self.camera.read()
                if success:
                    self.out.write(frame)
                    self.last_record_time = current_time
                self.out.release()
                cv2.destroyAllWindows()

    def stop_recording(self):
        self.recording = False

recorder = VideoRecorder()

def record_video():
    if not recorder.recording:
        threading.Thread(target=recorder.start_recording).start()

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/record_video')
def start_record():
    record_video()
    return '/Recording started'

@app.route('/stop_record')
def stop_record():
    recorder.stop_recording()
    return 'Recording stopped'

@app.route('/video_feed')
def video_feed():
    def generate_frames():
        while True:
            success, frame = recorder.camera.read()
            if not success:
                break
            else:
                ret, buffer = cv2.imencode('.jpg', frame)
                frame = buffer.tobytes()
                yield (b'--frame\r\n'
                       b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')

    return Response(generate_frames(), mimetype='multipart/x-mixed-replace; boundary=frame')

if __name__ == '__main__':
    app.run(debug=True)
