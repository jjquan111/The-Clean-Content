import pytesseract
from PIL import Image

# 读取 sent.txt 文件中的文字
with open('words.txt', 'r', encoding='utf-8') as file:
    sent_text_list = file.readlines()

# 使用 Tesseract 进行图像文字识别
def recognize_text(image_path):
    image = Image.open(image_path)
    text = pytesseract.image_to_string(image, lang='chi_sim')
    return text

# 指定要识别的图像路径
image_path = 'image.jpg'  # 替换为你的图像路径

# 进行文字识别
recognized_text = recognize_text(image_path)
print(recognized_text)


print('------')

# 判断识别到的文字是否包含在 sent.txt 中
if any(sent_text.strip() in recognized_text for sent_text in sent_text_list):
    print("图像不健康")
else:
    print("图像健康")