import os

from django.http import HttpResponse, JsonResponse
from django.shortcuts import render
from sklearn.tree import DecisionTreeClassifier


from django.shortcuts import render
from django.http import HttpResponseRedirect

from dal import models
import pdfkit



def news_list(request):
    news = models.news.objects.all()
    print(news)
    return render(request, 'news.html', {'news': news})



def tree(times,length):
    # train
    # 训练数据
    X_train = [[2, 10], [1, 8], [1, 12], [3, 15], [0, 10], [0, 80]]  # 特征: [关键词出现次数, 字符串长度]
    y_train = [1, 1, 1, 1, 0, 0]  # 标签: 0 表示非问题链接，1 表示问题链接
    # 创建决策树分类器并拟合数据
    clf = DecisionTreeClassifier()
    clf.fit(X_train, y_train)

    def is_question_link(times, length):
        X_test = [[times, length]]
        y_pred = clf.predict(X_test)
        return bool(y_pred)


    return is_question_link(times,length)

def garorder_list(request):
    garorder = models.garorder.objects.all()

    # for obj in garorder:
    #     # 获取对象的id
    #     object_id = obj.id
    #     # 打印id
    #     print(object_id)
    # print(garorder['id'])

    # 获取最后一项对象
    last_object = garorder.last()

    # 获取最后一项对象的id
    last_object_id = last_object.id
    print(last_object_id)
    return render(request, 'garorder.html', {'garorder': garorder})

def submitorder(request):
    if request.method == 'POST':
        # 获取表单数据
        form_data = request.POST
        # 或者使用以下方式获取某个字段的值
        # field_value = request.POST['field_name']
        print(form_data)
        ordercontent=request.POST['ordercontent']
        try:
            message = {}
            models.garorder.objects.create(ordercaptain=ordercontent)

            message['code'] = 200
            message['message'] = "发起订单成功"
            garorder = models.garorder.objects.all()
            print(garorder)
            return render(request, 'garorder.html', {'garorder': garorder})
        except Exception as e:
            print(e)

        # 返回响应或重定向到其他页面
        return HttpResponse('表单')

def updatepassage(request):
    if request.method == 'POST':
        print(request.POST['message'])

        passage_content=request.POST['message']

        fo=open('passage_update.txt','w',encoding='utf-8')
        fo.write(passage_content)
        fo.close()

        print("开始传输文本")
        os.system('python predict.py')


        detects = models.detects.objects.all()
        print(detects)
        return render(request, 'file-update.html', {'detects': detects})




    if request.method == 'GET':
        detects = models.detects.objects.all()
        print(detects)
        return render(request, 'file-update.html', {'detects': detects})


def updatefile(request):
    if request.method == 'POST':

        # get id

        detecinfo = models.detects.objects.all()
        print(detecinfo)

        # for obj in garorder:
        #     # 获取对象的id
        #     object_id = obj.id
        #     # 打印id
        #     print(object_id)
        # print(garorder['id'])

        # 获取最后一项对象
        last_object = detecinfo.last()
        print(last_object)

        # 获取最后一项对象的id
        fileid = (last_object.id)+1
        print(fileid)

        print("FILES:", request.FILES)
        print("POST:", request.POST)
        myFile = request.FILES.get("upload_file_form", None)
        if not myFile:
            return HttpResponse("no files for upload")

        import os

        # 指定要创建的文件夹路径
        folder_path = 'static\\output\\'+str(fileid)

        # 使用os.makedirs()函数递归地创建文件夹
        os.makedirs(folder_path)

        # 打开特定的文件进行二进制的写操作
        f = open(folder_path+'\\upload.mp4', "wb+")
        # 分块写入文件
        try:
            for chunk in myFile.chunks():
                f.write(chunk)
            f.close()
        except:
            pass

        os.system("copy static\output\\" + str(fileid) + "\\upload.mp4 .")

        models.detects.objects.create(detectcontent=folder_path+'\\upload.mp4',detectresult=folder_path+'\\output.mp4')

        # 识别

        os.system("conda activate torch1.10 && python demo.py")
        # 转码
        os.system("ffmpeg -i runs/detect/predict/upload.avi static/output/"+str(fileid)+"/output.mp4")

        detects = models.detects.objects.all()
        print(detects)
        return render(request, 'file-update.html', {'detects': detects})
        # return HttpResponse("<script>window.location.replace('http://127.0.0.1:8000/href/FileUpdate/')</script>")

    if request.method == 'GET':
        detects = models.detects.objects.all()
        print(detects)
        return render(request, 'file-update.html', {'detects': detects})




def uploadwordfile(request):


    if request.method == 'POST':
        file = request.FILES['file']

        with open('words.txt', 'wb+') as destination:
           for chunk in file.chunks():
               destination.write(chunk)
    return HttpResponse('success')

def uploadmainfile(request):
    def save_webpage_as_pdf(url, output_pdf):
        try:
            # 使用wkhtmltopdf将网页保存为PDF
            pdfkit.from_url(url, output_pdf)
            print("网页已成功保存为PDF！")
        except Exception as e:
            print(f"保存PDF时出现错误：{e}")


    if request.method == 'POST':

        url = request.POST['url']
        if url=='':
            print('urlnull')
            file = request.FILES['file']

            with open('static/file.pdf', 'wb+') as destination:
               for chunk in file.chunks():
                   destination.write(chunk)


        else:
        # print(request.POST['message'])


            try:
                url = request.POST['url']
                # url:
                # 要保存的网页URL
                # 输出的PDF文件路径
                output_pdf = "static/file.pdf"
                try:
                    os.remove(output_pdf)
                except Exception as e:
                    print(e)

                save_webpage_as_pdf(url, output_pdf)
            except Exception as e:
                print(e)

        os.system("python testpdf.py")
        return render(request, 'download.html')


def updatefilejpg(request):
    if request.method == 'POST':
        addword=request.POST['word']
        fo=open('words.txt','a',encoding='utf-8')
        fo.write("\n"+addword)
        fo.close()


        fo=open("words.txt",'r',encoding='utf-8')
        allwords=str(fo.readlines())
        fo.close()






        return render(request, 'word-update.html',{'allwords': allwords})
        # return HttpResponse("<script>window.location.replace('http://127.0.0.1:8000/href/FileUpdate/')</script>")

    if request.method == 'GET':
        fo=open("words.txt",'r',encoding='utf-8')
        allwords=str(fo.readlines())
        fo.close()




        return render(request, 'word-update.html', {'allwords': allwords})
