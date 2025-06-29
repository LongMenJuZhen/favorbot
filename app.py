import base64
import os
import re

from flask import Flask, render_template, request, jsonify

from llmClient import DoubaoClient
from handlers import *


def contains_url(text):
    """检查文本中是否包含 URL"""
    if not isinstance(text, str):
        return False

    url_pattern = re.compile(
        r'https?://'  # http:// 或 https://
        r'(?:[A-Z0-9-]+\.)+[A-Z]{2,6}'  # 域名（如 example.com）
        r'(?::\d+)?'  # 可选端口（如 :8080）
        r'(?:/[\w\-./?%&=]*)?',  # 可选路径/查询参数
        re.IGNORECASE
    )

    return bool(url_pattern.search(text))

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
    image_path = ''



    image_info = ""
    if image_file:
        # 保存图片或处理图片
        image_path = os.path.join(UPLOAD_FOLDER, image_file.filename)
        image_file.save(image_path)

        # 可以在这里添加图片处理逻辑
        # 例如：将图片转为base64或调用视觉API
        with open(image_path, "rb") as img_file:
            image_b64 = base64.b64encode(img_file.read()).decode('utf-8')
        image_info = f"[收到图片: {image_file.filename}]"



    if image_file:
        handler = ImageHandler('multimodal_store.csv')
        resp = handler.handle(image_path, user_message)


        messages = [
            {"role": "system", "content": "你是一个智能收藏夹助手，帮助用户管理文本、图片以及网页收藏。"},
            {"role": "user", "content": f"现在用户将存入一段图片内容。请简要总结用户存入的内容。并告诉用户已经存入该内容"
                                        f"用户存入的内容：{user_message} {image_info}"
                                        f"图片描述：{resp}"}
        ]

        client = DoubaoClient()
        reply = client.call(messages)
    else:
        if contains_url(user_message):
            handler = UrlHandler('multimodal_store.csv')
            resp = handler.handle(user_message)

            messages = [
                {"role": "system", "content": "你是一个智能收藏夹助手，帮助用户管理文本、图片以及网页收藏。"},
                {"role": "user",
                 "content": f"现在用户将存入一个网页内容。请简要总结用户存入的内容。并告诉用户已经存入该内容"
                            f"用户存入的内容：{user_message} "
                            f"网页描述：{resp}"}
            ]

            client = DoubaoClient()
            reply = client.call(messages)

        elif user_message:
            handler = TXTHandler('multimodal_store.csv')
            handler.handle(user_message)

            messages = [
                {"role": "system", "content": "你是一个智能收藏夹助手，帮助用户管理文本、图片以及网页收藏。"},
                {"role": "user", "content": f"现在用户将存入一段文本内容。请简要总结用户存入的内容。并告诉用户已经存入该内容"
                                            f"用户存入的文本内容：{user_message} "}
            ]

            client = DoubaoClient()
            reply = client.call(messages)

        else:
            reply = "未识别到有效内容，试着存入文本、图片或网页吧~"


    return jsonify({"reply": reply})


if __name__ == "__main__":
    app.run(debug=True)