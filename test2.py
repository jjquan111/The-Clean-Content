import pdfkit

# 将网页保存为PDF
def save_webpage_as_pdf(url, output_pdf):
    try:
        # 使用wkhtmltopdf将网页保存为PDF
        pdfkit.from_url(url, output_pdf)
        print("网页已成功保存为PDF！")
    except Exception as e:
        print(f"保存PDF时出现错误：{e}")

# 要保存的网页URL
url = "https://arxiv.org/abs/2203.01927"
# 输出的PDF文件路径
output_pdf = "file.pdf"

# 调用函数保存网页为PDF
save_webpage_as_pdf(url, output_pdf)