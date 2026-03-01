from flask import Flask, request, jsonify
from mutagen import File
import requests

app = Flask(__name__)

@app.route("/upload", methods=["POST"])
def upload():
    file = request.files["file"]
    audio = File(file)

    title = audio.get("TIT2")
    artist = audio.get("TPE1")

    search_term = ""
    if title:
        search_term += str(title)
    if artist:
        search_term += " " + str(artist)

    response = requests.get(
        f"https://itunes.apple.com/search?term={search_term}&limit=1"
    )
    data = response.json()

    if data["resultCount"] > 0:
        return jsonify(data["results"][0])
    else:
        return jsonify({"message": "Song not found"})
    
if __name__ == "__main__":
    app.run(debug=True)
