from flask import Flask, render_template, request, make_response, send_from_directory, url_for
import io
import os
from weasyprint import HTML
import re
import fitz  # PyMuPDF for extracting text from PDF
from zipfile import ZipFile, ZIP_DEFLATED

app = Flask(__name__)

TMP_DIR = os.path.join(os.getcwd(), 'tmp')
if not os.path.exists(TMP_DIR):
    os.makedirs(TMP_DIR)

def load_bad_words(file_path='en.txt'):
    with open(file_path, 'r', encoding='utf-8') as file:
        return {line.strip().lower() for line in file if line.strip()}

def highlight_text(text, bad_words):
    for word in bad_words:
        pattern = re.compile(r'\b(' + re.escape(word) + r')\b', re.IGNORECASE)
        text = pattern.sub(r'<span style="background-color: yellow;">\1</span>', text)
    return text

def filter_text(text, bad_words):
    for word in bad_words:
        pattern = re.compile(r'\b' + re.escape(word) + r'\b', re.IGNORECASE)
        text = pattern.sub("*" * len(word), text)
    return text

def extract_text_from_pdf(file):
    pdf = fitz.open(stream=file.read(), filetype="pdf")
    text = ""
    for page in pdf:
        text += page.get_text()
    pdf.close()
    return text

def generate_pdf(html_content):
    return HTML(string=html_content).write_pdf()

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        file = request.files.get('file')
        if file and file.filename.endswith('.pdf'):
            bad_words = load_bad_words()
            text = extract_text_from_pdf(file)
            highlighted_html = f"<html><body>{highlight_text(text, bad_words)}</body></html>"
            filtered_html = f"<html><body>{filter_text(text, bad_words)}</body></html>"
            
            highlighted_pdf = generate_pdf(highlighted_html)
            filtered_pdf = generate_pdf(filtered_html)
            
            zip_buffer = io.BytesIO()
            with ZipFile(zip_buffer, 'w', ZIP_DEFLATED) as zip_file:
                zip_file.writestr("highlighted_content.pdf", highlighted_pdf)
                zip_file.writestr("filtered_content.pdf", filtered_pdf)
            zip_buffer.seek(0)
            
            zip_filename = "processed_texts.zip"
            zip_path = os.path.join(TMP_DIR, zip_filename)
            with open(zip_path, 'wb') as f:
                f.write(zip_buffer.getvalue())
            
            return render_template('download.html', zip_filename=zip_filename)
    return render_template('index.html')

@app.route('/download/<filename>')
def download_file(filename):
    return send_from_directory(TMP_DIR, filename, as_attachment=True)

if __name__ == '__main__':
    app.run(debug=True)
