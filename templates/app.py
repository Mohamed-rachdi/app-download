from flask import Flask, render_template, request, Response
from pytube import YouTube
import io

app = Flask(__name__)

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        video_url = request.form.get('url')
        resolution = request.form.get('resolution')

        try:
            # Create a YouTube object
            yt = YouTube(video_url)
            # Find the stream with the chosen resolution
            stream = yt.streams.filter(res=resolution, progressive=True).first()
            if not stream:
                stream = yt.streams.filter(res=resolution).first()
            
            # Create a buffer to hold the streamed data
            buffer = io.BytesIO()
            # Stream the video content directly to the buffer
            stream.stream_to_buffer(buffer)
            # Set the buffer's cursor to the beginning
            buffer.seek(0)
            
            # Stream the video content directly to the user's browser
            return Response(buffer, mimetype='video/mp4', headers={"Content-Disposition": "attachment; filename=video.mp4"})

        except Exception as e:
            return str(e)

    return render_template('index.html')

if __name__ == '__main__':
    app.run(debug=True)
