import cv2
from flask import Flask, Response, request
from ultralytics import YOLO

app = Flask(__name__)
model = YOLO('./best.pt')

# Function for capturing and processing the video stream
def generate_frames(rtsp_url):
    if rtsp_url is None:
        username = "admin"
        password = "A1234567"

        rtsp_url = f"rtsp://{username}:{password}@188.170.176.190:8028/Streaming/Channels/101?transportmode=unicast&profile=Profile_1"

    video_url = rtsp_url

    cap = cv2.VideoCapture(video_url)
    while True:
        # Capture a frame
        success, frame = cap.read()
        if not success:
            break

        # Process the frame (your processing logic here)
        result = model.track(source=frame,
                         conf=0.25,
                         tracker='botsort.yaml')

        # Convert the frame to JPEG format
        ret, buffer = cv2.imencode('.jpg', frame)
        frame = buffer.tobytes()

        # Return the frame for display on the front-end
        yield (b'--frame\r\n'
               b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')


@app.route('/upload', methods=['POST'])
def upload_file():
    if 'file' not in request.files:
        return 'No file part'

    file = request.files['file']

    if file.filename == '':
        return 'No selected file'

    if file:
        # Save the file to a folder
        file.save('./uploads/' + file.filename)
        return 'File uploaded successfully'

    generate_frames('uploads/' + file.filename)


@app.route('/video_feed', methods=['GET'])
def video_feed():
    rtsp_url = request.args.get('rtsp_url')

    # if rtsp_url is None:
    #     return "Error: Please provide an RTSP URL as a query parameter", 400

    return Response(generate_frames(rtsp_url), content_type='multipart/x-mixed-replace; boundary=frame')


if __name__ == "__main__":
    # Run the Flask application
    app.run(debug=True)
