import fitz  # PyMuPDF
import PyPDF2
import docx
import os
# from docx2pdf import convert
import pdfkit  # pip install pdfkit
from pydocx import PyDocX  # pip install pydocx


def highlight_text_in_pdf(pdf_file, word_lists):
    # Open the PDF
    pdf_document = fitz.open(pdf_file)

    for page_num in range(len(pdf_document)):
        page = pdf_document.load_page(page_num)
        for word in word_lists:
            # Search for the word on the page
            instances = page.search_for(word)
            for inst in instances:
                # Highlight the word
                rect = fitz.Rect(inst)
                highlight = page.add_highlight_annot(rect)
                highlight.set_colors(stroke=(0, 0, 0), fill=(1, 1, 0))  # 设置荧光颜色为黄色

    # Save the modified PDF
    # Save the new PDF with highlighted text
    highlighted_pdf_file = "static/highlighted_file.pdf"
    pdf_document.save(highlighted_pdf_file)


if __name__ == "__main__":



    def rename_file(file_path):
        new_file_path = os.path.join(os.path.dirname(file_path), 'test.docx')
        try:
            os.remove(new_file_path)
        except Exception as e:
            print(e)
        os.rename(file_path, new_file_path)
        print(f"File has been renamed to {new_file_path}")


    def detect_and_convert(file_path):
        # 尝试读取PDF文件
        try:
            with open(file_path, 'rb') as file:
                pdf_reader = PyPDF2.PdfReader(file)
                print('File is PDF.')
                return 'pdf'
        except Exception as e:
            pass  # 不是PDF文件

        # 尝试读取DOCX文件
        try:
            doc = docx.Document(file_path)
            print('File is DOCX.')
            rename_file(file_path)

            # 将DOCX转换为PDF
            output_pdf_path = 'static/file.pdf'

            # # 将 Word 文档转换为 PDF
            # convert("static/test.docx", "static/file.pdf")

            html = PyDocX.to_html('static/test.docx')
            f = open('test.html', 'w')
            f.write(html)
            f.close()

            # pdfkit.from_file('html1.html', 'test3.pdf')
            pdfkit.from_string(html, 'static/file.pdf')

            print('DOCX has been converted to PDF:', output_pdf_path)
            return output_pdf_path
        except ValueError:
            pass  # 不是DOCX文件

        print('Unknown file format.')

    file_path = 'static/file.pdf'  # 修改为你的文件路径
    result = detect_and_convert(file_path)





    pdf_file = 'static/file.pdf'



    with open('words.txt', 'r', encoding='utf-8') as file:
        word_lists = file.readlines()
    highlight_text_in_pdf(pdf_file, word_lists)