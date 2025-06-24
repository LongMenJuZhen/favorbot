import base64
import os

from flask import Flask, render_template, request, jsonify
from llmClient.doubaoClient import DoubaoClient

app = Flask(__name__)
UPLOAD_FOLDER = 'uploads'
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

@app.route("/")
def home():
    return render_template("index.html")


@app.route("/api/chat", methods=["POST"])
def chat():
    user_message = request.form.get("message", "")
    image_file = request.files.get("image")

    image_info = ""
    if image_file:
        # 保存图片或处理图片
        filename = os.path.join(UPLOAD_FOLDER, image_file.filename)
        image_file.save(filename)

        # 可以在这里添加图片处理逻辑
        # 例如：将图片转为base64或调用视觉API
        with open(filename, "rb") as img_file:
            image_b64 = base64.b64encode(img_file.read()).decode('utf-8')
        image_info = f"[收到图片: {image_file.filename}]"

    messages = [
        {"role": "system", "content": "你是一个智能收藏夹助手，帮助用户管理网络收藏。"},
        {"role": "user", "content": f"{user_message} {image_info}"}
    ]

    client = DoubaoClient()
    reply = client.call(messages)

    return jsonify({"reply": reply})


if __name__ == "__main__":
    app.run(debug=True)