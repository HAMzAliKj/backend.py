from flask import Flask, jsonify, request
from youtube_transcript_api import YouTubeTranscriptApi
from flask_cors import CORS

app = Flask(__name__)
CORS(app)  # Allow requests from your Streamlit app

@app.route("/transcript", methods=["GET"])
def get_transcript():
    # Get the video ID from the request
    video_id = request.args.get("video_id")
    if not video_id:
        return jsonify({"error": "video_id is required"}), 400

    try:
        # Fetch the transcript using youtube-transcript-api
        transcript = YouTubeTranscriptApi.get_transcript(video_id)
        return jsonify(transcript)
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)