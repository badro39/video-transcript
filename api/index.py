from flask import Flask, request, jsonify, Response
from youtube_transcript_api import YouTubeTranscriptApi

app = Flask(__name__)

@app.route('/debug-installed')
def debug_installed():
    try:
        import pkg_resources
        packages = sorted([f"{d.project_name}=={d.version}" for d in pkg_resources.working_set])
        return jsonify(packages)
    except Exception as e:
        import traceback
        return jsonify({
            "error": str(e),
            "traceback": traceback.format_exc()
        }), 500


@app.route('/generate-vtt', methods=['GET'])
def generate_vtt():
    video_id = request.args.get('video_id')

    if not video_id:
        return jsonify({'error': 'Missing video_id'}), 400
    if not isinstance(video_id, str):
        return jsonify({'error': 'video_id must be a string'}), 400

    try:
        transcript = YouTubeTranscriptApi.get_transcript(video_id, languages=["ar"])

        formatted_transcript = []
        for item in transcript:
            start = round(item['start'], 3)
            end = round(item['start'] + item['duration'], 3)
            text = item['text'].strip()
            formatted_line = f"[{start} --> {end}] {text}"
            formatted_transcript.append(formatted_line)

        formatted_output = "\n".join(formatted_transcript)

        return Response(
            response=formatted_output,
            content_type='text/plain; charset=utf-8'
        )

    except Exception as e:
        return jsonify({'error': str(e)}), 500

#app.run(host='0.0.0.0', port=5000, debug=True)
