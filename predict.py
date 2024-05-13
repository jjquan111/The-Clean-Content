

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

    # 解码base64图像数据
    image_data = base64.b64decode(sentence)


    # 将图像数据转换为PIL Image对象
    img = Image.open(io.BytesIO(image_data))

    # 保存图像到本地文件系统
    img.save('image.jpg')

    # 读取 sent.txt 文件中的文字
    with open('words.txt', 'r', encoding='utf-8') as file:
        sent_text_list = file.readlines()

    # 使用 Tesseract 进行图像文字识别
    def recognize_text(image_path):

        from PIL import Image

        # 读取图像
        image = Image.open(image_path)

        # 将图像转换为灰度图像
        gray_image = image.convert('L')

        # 进行二值化处理
        threshold = 127
        binary_image = gray_image.point(lambda x: 0 if x < threshold else 255, '1')


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

    sentence=recognized_text




    file_path = "words.txt"  # 文件路径
    string_to_check = sentence  # 待检查的字符串

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
    'user': 'root',  # 替换为你的数据库用户名
    'password': 'root',  # 替换为你的数据库密码
    'db': 'wordtext',  # 数据库名
    'cursorclass': pymysql.cursors.DictCursor
}

connection = pymysql.connect(**config)

try:
    with connection.cursor() as cursor:
        # 创建插入SQL语句
        sql = "INSERT INTO `detectinfo` (`detectresult`, `detectcontent`) VALUES (%s, %s)"

        # 执行sql语句，并传入参数
        cursor.execute(sql, (result, sent))

        # 提交事务
        connection.commit()

finally:
    # 关闭连接
    connection.close()

