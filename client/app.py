from flask import Flask, render_template, request, redirect, url_for,Response
import socket
from modules.fetch import Fetch
from flask import jsonify

HOST = "127.0.0.1"
PORT = 3000
apiUrl = f"http://{HOST}:{PORT}"

app = Flask(__name__)

@app.route('/upload', methods=['POST'])
def upload():
    file = request.files['file']
    blob = file.read()
    video = {
        "title": 'Flask Sended Video',
        "blob": blob,
        "size": len(blob)
    }
    response = Fetch.post(f'{apiUrl}/video', video)
    return "File uploaded successfully! You can now upload another file.", response
@app.route('/stream')
def stream():
    video_id = request.args.get('id')
    video = Fetch.post(f'{apiUrl}/video/id', {
        "id": video_id
    })
    return Response(video, content_type='video/mp4')

@app.route('/videos', methods=['GET'])
def list():
    videos = Fetch.get(f'{apiUrl}/videos')
    response = jsonify({"result": videos})
    response.headers.add("Access-Control-Allow-Origin", "*")
    return response

@app.route('/video', methods=['DELETE'])
def delete():
    video_id = request.args.get('id')
    video = Fetch.delete(f'{apiUrl}/video', {
        "id": video_id
    })
    return video
    # client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    # client.connect((HOST, PORT))
    # header = f"STREAM {video_name} "
    # client.send(f"{header: <1024}".encode())
    
    # def generate(client):
    #     chunk_size = 4096
    #     while True:
    #         data = client.recv(chunk_size)
    #         if not data:
    #             break
    #         yield data
    #     client.close()
    # return Response(generate(client), content_type='video/mp4')

if __name__ == '__main__':
    app.run(debug=True, port=5000)
