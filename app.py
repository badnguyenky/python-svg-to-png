import base64
import requests
import io
import cairosvg
from flask import Flask, request, jsonify, send_file

app = Flask(__name__)

@app.route("/convert", methods=["POST"])
def convert_svg():
    try:
        data = request.json
        if not data or "svg" not in data:
            return jsonify({"error": "SVG data or URL is required"}), 400

        # Fetch SVG if a URL is provided
        if data["svg"].startswith("http"):
            response = requests.get(data["svg"])
            if response.status_code != 200:
                return jsonify({"error": "Failed to fetch SVG"}), 400
            svg_data = response.text
        else:
            svg_data = data["svg"]

        # Convert SVG to PNG
        png_bytes = cairosvg.svg2png(bytestring=svg_data.encode("utf-8"))

        # Return PNG as a response
        return send_file(io.BytesIO(png_bytes), mimetype="image/png")

    except Exception as e:
        return jsonify({"error": "Conversion failed", "details": str(e)}), 500

# Required for Vercel
def handler(event, context):
    return app(event, context)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
