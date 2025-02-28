import io
import asyncio
import base64
from flask import Flask, request, jsonify, send_file
from pyppeteer import launch

app = Flask(__name__)

async def render_svg(svg_data):
    """Convert SVG to PNG using Headless Chromium (Pyppeteer)"""
    browser = await launch(headless=True, args=["--no-sandbox"])
    page = await browser.newPage()
    
    # Set the viewport to match SVG dimensions
    await page.setContent(f'<html><body>{svg_data}</body></html>')
    element = await page.querySelector("svg")
    if not element:
        await browser.close()
        raise Exception("No SVG element found!")

    # Capture the screenshot of SVG
    png_bytes = await element.screenshot()
    await browser.close()
    
    return png_bytes

@app.route("/convert", methods=["POST"])
def convert_svg():
    try:
        data = request.json
        if not data or "svg" not in data:
            return jsonify({"error": "SVG data is required"}), 400

        svg_data = data["svg"]
        png_bytes = asyncio.run(render_svg(svg_data))

        return send_file(io.BytesIO(png_bytes), mimetype="image/png")
    
    except Exception as e:
        return jsonify({"error": "Conversion failed", "details": str(e)}), 500

# Required for Vercel
def handler(event, context):
    return app(event, context)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
