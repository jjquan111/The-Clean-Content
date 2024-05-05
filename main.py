from flask import (
    Flask,
    redirect,
    render_template,
    request,
    send_from_directory,
    url_for,
    session,
    flash,
    send_file,
)
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
import os
import io
import fitz  # PyMuPDF
from docx import Document
from database import db, User, Text
from login import auth
from werkzeug.utils import secure_filename
from content_filter import load_bad_words, highlight_text, filter_text
import logging


def create_app():
    app = Flask(__name__)
    app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///site.db"
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
    app.secret_key = "your_very_secret_key"
    db.init_app(app)
    migrate = Migrate(app, db)

    with app.app_context():
        db.create_all()

    app.register_blueprint(auth, url_prefix="/auth")
    return app


app = create_app()

TMP_DIR = os.path.join(app.instance_path, "tmp")
os.makedirs(TMP_DIR, exist_ok=True)


def create_overlay_pdf(original_pdf, bad_words):
    doc = fitz.open(stream=original_pdf.read(), filetype="pdf")
    overlay_pdf = fitz.open()  # Create a new blank PDF
    for page in doc:
        blank_page = overlay_pdf.new_page(
            width=page.rect.width, height=page.rect.height
        )
        for word in bad_words:
            text_instances = page.search_for(word)
            for inst in text_instances:
                replacement_text = "*" * len(word)
                blank_page.insert_text(
                    (inst[0], inst[1]), replacement_text, fontsize=11, color=(0, 0, 0)
                )
    pdf_bytes = io.BytesIO()
    overlay_pdf.save(pdf_bytes)
    pdf_bytes.seek(0)
    return pdf_bytes


def merge_pdfs(base_pdf_stream, overlay_pdf_stream):
    base_pdf_stream.seek(0)  # Ensure stream is at the start
    overlay_pdf_stream.seek(0)  # Ensure stream is at the start

    base_pdf = fitz.open("pdf", base_pdf_stream.read())  # Open base PDF from bytes
    overlay_pdf = fitz.open(
        "pdf", overlay_pdf_stream.read()
    )  # Open overlay PDF from bytes

    # Create a new PDF to store the merged output
    merged_pdf = fitz.open()
    for base_page in base_pdf:
        # Import the page to the new merged PDF
        merged_page = merged_pdf.new_page(
            width=base_page.rect.width, height=base_page.rect.height
        )
        # First, insert the base page as a layer
        merged_page.show_pdf_page(merged_page.rect, base_pdf, base_page.number)
        # Then, insert the overlay page as a layer
        if base_page.number < len(overlay_pdf):
            merged_page.show_pdf_page(merged_page.rect, overlay_pdf, base_page.number)

    # Write to a BytesIO stream to return
    output_pdf_stream = io.BytesIO()
    merged_pdf.save(output_pdf_stream)
    output_pdf_stream.seek(0)
    return output_pdf_stream


@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST":
        if "user_id" not in session:
            flash("Please log in to start filtering.", "info")
            return redirect(url_for("auth.login"))

        file = request.files.get("file")
        if file and file.filename.lower().endswith(".pdf"):
            file.stream.seek(0)  # Rewind the stream
            bad_words = load_bad_words()
            overlay_pdf_stream = create_overlay_pdf(file.stream, bad_words)
            filtered_pdf_stream = merge_pdfs(file.stream, overlay_pdf_stream)

            filtered_pdf_path = os.path.join(TMP_DIR, secure_filename(file.filename))
            with open(filtered_pdf_path, "wb") as f:
                f.write(filtered_pdf_stream.read())

            session["filtered_pdf_filename"] = filtered_pdf_path
            return render_template(
                "download.html",
                filename=os.path.basename(filtered_pdf_path),
                user_id=session.get("user_id"),
            )
        else:
            flash("Unsupported file type.", "error")
            return render_template("index.html", user_id=session.get("user_id"))

    return render_template("index.html", user_id=session.get("user_id"))


@app.route("/download/<filename>")
def download_file(filename):
    file_path = os.path.join(TMP_DIR, secure_filename(filename))
    if not os.path.exists(file_path):
        flash("File not found.", "error")
        return render_template("404.html"), 404
    return send_file(file_path, as_attachment=True, download_name=filename)


@app.route("/my_documents")
def my_documents():
    if "user_id" not in session:
        flash("Please log in to view this page.", "info")
        return redirect(url_for("auth.login"))
    return render_template("my_documents.html")


if __name__ == "__main__":
    app.run(debug=True)
