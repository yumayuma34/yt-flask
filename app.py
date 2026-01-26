from flask import Flask, request
import subprocess

app = Flask(__name__)

@app.route("/")
def index():
    return """
    <form action="/geturl" method="POST">
        <input type="text" name="videoUrl" placeholder="動画URLを入力">
        <button type="submit">実行</button>
    </form>
    """

@app.route("/geturl", methods=["POST"])
def geturl():
    input_url = request.form.get("videoUrl")

    try:
        result = subprocess.check_output(
            ["yt-dlp", "--no-warnings", "--get-url", "-f", "18", input_url],
            stderr=subprocess.STDOUT,
            text=True
        )

        direct_url = result.strip()
        return f"取得したURL<br><a href='{direct_url}' target='_blank'>{direct_url}</a>"

    except subprocess.CalledProcessError as e:
        return f"エラー<br><pre>{e.stdout}</pre>"

if __name__ == "__main__":
    app.run(port=5000, debug=True)