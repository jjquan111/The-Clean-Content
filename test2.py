import pdfkit

def save_webpage_as_pdf(url, output_pdf):
        pdfkit.from_url(url, output_pdf)
        print("Save as PDF success！")
    except Exception as e:
        print(f"error：{e}")

url = "https://arxiv.org/abs/2203.01927"
output_pdf = "file.pdf"

save_webpage_as_pdf(url, output_pdf)
