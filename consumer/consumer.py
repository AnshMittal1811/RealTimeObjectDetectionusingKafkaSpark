
from flask import Flask, Response, render_template
from kafka import KafkaConsumer

# Fire up the Kafka Consumer
topic = "kafka-video-topic"

consumer = KafkaConsumer(
    topic, 
    bootstrap_servers=['192.168.99.100:9092'])


# Set the consumer in a Flask App
app = Flask(__name__)


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/read_video', methods=['GET'])
def read_video():
    """
    This is the heart of our video display. Notice we set the mimetype to 
    multipart/x-mixed-replace. This tells Flask to replace any old images with 
    new values streaming through the pipeline.
    """
    return Response(
        get_video_stream(), 
        mimetype='multipart/x-mixed-replace; boundary=frame')


def get_video_stream():
    """
    Here is where we recieve streamed images from the Kafka Server and convert 
    them to a Flask-readable format.
    """
    for msg in consumer:
        print("msg ", msg)
        yield (b'--frame\r\n'
               b'Content-Type: image/jpg\r\n\r\n' + msg.value + b'\r\n\r\n')


if __name__ == "__main__":
    app.run(host='0.0.0.0', debug=True)
