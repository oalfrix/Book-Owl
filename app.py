from flask import Flask, render_template, request, send_file
import os
from PyPDF2 import PdfFileReader
from gtts import gTTS
from pydub import AudioSegment
import io

app = Flask(__name__)

def pdf_to_text(pdf_file):
    pdf_reader = PdfFileReader(pdf_file)
    text = ""
    for page_num in range(pdf_reader.numPages):
        page = pdf_reader.getPage(page_num)
        text += page.extract_text()
    return text

def text_to_audio(text, lang='en'):
    tts = gTTS(text=text, lang=lang)
    audio_io = io.BytesIO()
    tts.write_to_fp(audio_io)
    audio_io.seek(0)
    return audio_io

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        if 'file' not in request.files:
            return "No file part"
        file = request.files['file']
        if file.filename == '':
            return "No selected file"
        if file and file.filename.endswith('.pdf'):
            text = pdf_to_text(file)
            audio_io = text_to_audio(text)
            return send_file(audio_io, as_attachment=True, download_name='audiobook.mp3', mimetype='audio/mp3')
    return render_template('index.html')

if __name__ == '__main__':
    app.run(debug=True)
