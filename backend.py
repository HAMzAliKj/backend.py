from flask import Flask,  request, jsonify
from youtube_transcript_api import YouTubeTranscriptApi as yt
from youtube_transcript_api._errors import NoTranscriptFound
from langchain_google_genai import ChatGoogleGenerativeAI
from flask_cors import CORS
from youtube_transcript_api._errors import NoTranscriptFound, TranscriptsDisabled
import os

app = Flask(__name__)
CORS(app)

llm = ChatGoogleGenerativeAI(model="gemini-1.5-flash", api_key='AIzaSyBT7otzDr-MQ8ZS1JCP4Q0hTxnKHQ2ZDf0')

@app.route("/transcript", methods=["GET"])
def get_transcript():
    video_id = request.args.get("video_id")

    try:
        transcripts = yt.list_transcripts(video_id)
        manual_transcripts = [t for t in transcripts if not t.is_generated]
        if manual_transcripts:
            transcript = manual_transcripts[0]
        else:
            generated_transcripts = [t for t in transcripts if t.is_generated]
            if generated_transcripts:
                transcript = generated_transcripts[0]
        

        new = llm.invoke(f"You just give me video language just like hi or en no other thing {transcript}")
        # print(new.content)
        text = yt.get_transcript(video_id=video_id,languages=[new.content])
        return text
    except NoTranscriptFound:
        return jsonify({"error": "No subtitles found for this video"}), 404
    except TranscriptsDisabled:
        return jsonify({"error": "Subtitles are disabled for this video"}), 403
    except Exception as e:
        return jsonify({"error": str(e)})

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 5000)))
