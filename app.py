from flask import Flask, render_template, request
import requests
from PIL import Image
from io import BytesIO
import base64
import os
from dotenv import load_dotenv

load_dotenv()

app = Flask(__name__)

API_KEY = os.getenv("STABILITY_API_KEY")

# ✅ Stability API endpoint
API_URL = "https://api.stability.ai/v2beta/stable-image/generate/core"

headers = {
    "Authorization": f"Bearer {API_KEY}",
    "Accept": "image/*"
}

@app.route("/", methods=["GET", "POST"])
def index():
    image_data = None
    error = None

    if request.method == "POST":
        prompt = request.form.get("prompt")

        response = requests.post(
            API_URL,
            headers=headers,
            files={
                "prompt": (None, prompt),
                "output_format": (None, "png")
            }
        )

        if response.status_code != 200:
            error = response.text
        else:
            image = Image.open(BytesIO(response.content))

            buffer = BytesIO()
            image.save(buffer, format="PNG")
            image_data = base64.b64encode(buffer.getvalue()).decode()

    return render_template("index.html", image=image_data, error=error)

if __name__ == "__main__":
       port = int(os.environ.get("PORT", 8080))
       app.run(host="0.0.0.0", port=port)