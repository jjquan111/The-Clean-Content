import os

from django.http import HttpResponse, JsonResponse
from django.shortcuts import render
from sklearn.tree import DecisionTreeClassifier
from django.shortcuts import redirect
from django.views.decorators.http import require_POST

@require_POST
def delete_all_words(request):
    # Path to the words file
    words_file_path = 'words.txt'
    # Clear the text file
    open(words_file_path, 'w').close()

    # Assuming you have a model named 'Word' that stores the words
    # You should adjust this part according to your actual model
    from .models import Word
    Word.objects.all().delete()

    # Redirect to a confirmation page or back to the main page
    return redirect('your_redirect_url_name')  # Adjust the URL name as per your URLconf


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
    X_train = [[2, 10], [1, 8], [1, 12], [3, 15], [0, 10], [0, 80]]  
    y_train = [1, 1, 1, 1, 0, 0] 
    clf = DecisionTreeClassifier()
    clf.fit(X_train, y_train)

    def is_question_link(times, length):
        X_test = [[times, length]]
        y_pred = clf.predict(X_test)
        return bool(y_pred)


    return is_question_link(times,length)

def garorder_list(request):
    garorder = models.garorder.objects.all()


    last_object = garorder.last()

    last_object_id = last_object.id
    print(last_object_id)
    return render(request, 'garorder.html', {'garorder': garorder})

def submitorder(request):
    if request.method == 'POST':
        form_data = request.POST
        print(form_data)
        ordercontent=request.POST['ordercontent']
        try:
            message = {}
            models.garorder.objects.create(ordercaptain=ordercontent)

            message['code'] = 200
            message['message'] = "success"
            garorder = models.garorder.objects.all()
            print(garorder)
            return render(request, 'garorder.html', {'garorder': garorder})
        except Exception as e:
            print(e)

        return HttpResponse('site')

def updatepassage(request):
    if request.method == 'POST':
        print(request.POST['message'])

        passage_content=request.POST['message']

        fo=open('passage_update.txt','w',encoding='utf-8')
        fo.write(passage_content)
        fo.close()

        print("start passing")
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

        last_object = detecinfo.last()
        print(last_object)

        fileid = (last_object.id)+1
        print(fileid)

        print("FILES:", request.FILES)
        print("POST:", request.POST)
        myFile = request.FILES.get("upload_file_form", None)
        if not myFile:
            return HttpResponse("no files for upload")

        import os

        folder_path = 'static\\output\\'+str(fileid)

        os.makedirs(folder_path)

        f = open(folder_path+'\\upload.mp4', "wb+")
        try:
            for chunk in myFile.chunks():
                f.write(chunk)
            f.close()
        except:
            pass

        os.system("copy static\output\\" + str(fileid) + "\\upload.mp4 .")

        models.detects.objects.create(detectcontent=folder_path+'\\upload.mp4',detectresult=folder_path+'\\output.mp4')

        os.system("conda activate torch1.10 && python demo.py")
        os.system("ffmpeg -i runs/detect/predict/upload.avi static/output/"+str(fileid)+"/output.mp4")

        detects = models.detects.objects.all()
        print(detects)
        return render(request, 'file-update.html', {'detects': detects})

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

            try:
                url = request.POST['url']
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

    if request.method == 'GET':
        fo=open("words.txt",'r',encoding='utf-8')
        allwords=str(fo.readlines())
        fo.close()




        return render(request, 'word-update.html', {'allwords': allwords})
