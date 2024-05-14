import pytesseract
from PIL import Image

with open('words.txt', 'r', encoding='utf-8') as file:
    sent_text_list = file.readlines()
    
def recognize_text(image_path):
    image = Image.open(image_path)
    text = pytesseract.image_to_string(image, lang='chi_sim')
    return text

image_path = 'image.jpg'

recognized_text = recognize_text(image_path)
print(recognized_text)


print('------')

if any(sent_text.strip() in recognized_text for sent_text in sent_text_list):
    print("image not good")
else:
    print("image good")
