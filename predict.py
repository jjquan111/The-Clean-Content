

import pymysql

import json

from snownlp import SnowNLP
import base64

import pytesseract
from PIL import Image
import io


def analyze_sentiment(sentence):
    sentence = sentence.split('data:image/jpeg;base64,')[1]

    print(sentence)
    print("readed")
    image_data = base64.b64decode(sentence)


    img = Image.open(io.BytesIO(image_data))

    img.save('image.jpg')

    with open('words.txt', 'r', encoding='utf-8') as file:
        sent_text_list = file.readlines()

    def recognize_text(image_path):

        from PIL import Image
        image = Image.open(image_path)

        gray_image = image.convert('L')

        threshold = 127
        binary_image = gray_image.point(lambda x: 0 if x < threshold else 255, '1')


        text = pytesseract.image_to_string(image, lang='chi_sim')
        return text
        
    image_path = 'image.jpg' 

    recognized_text = recognize_text(image_path)
    print(recognized_text)

    print('------')

    if any(sent_text.strip() in recognized_text for sent_text in sent_text_list):
        print("image good")

    else:
        print("image not good")

    sentence=recognized_text




    file_path = "words.txt" 
    string_to_check = sentence 

    with open(file_path, 'r', encoding='utf-8') as f:
        for line in f:
            if line.strip() in string_to_check:
                string_to_check = string_to_check.replace(line.strip(), "【"+line.strip()+"】")


    return string_to_check


fo=open('passage_update.txt',encoding='utf-8')
sent=str(fo.read())
print(sent)
fo.close()

result=analyze_sentiment(sent)

config = {
    'host': '127.0.0.1',
    'port': 3306,
    'user': 'root', 
    'password': 'root', 
    'db': 'wordtext', 
    'cursorclass': pymysql.cursors.DictCursor
}

connection = pymysql.connect(**config)

try:
    with connection.cursor() as cursor:
        sql = "INSERT INTO `detectinfo` (`detectresult`, `detectcontent`) VALUES (%s, %s)"

        cursor.execute(sql, (result, sent))

        connection.commit()

finally:
    connection.close()

