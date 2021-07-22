from django.shortcuts import render,redirect
import requests as rq
from django.conf import settings
from django.utils import timezone
from bs4 import BeautifulSoup as bs
from .models import *
from django.core.files.storage import FileSystemStorage
from subprocess import PIPE,Popen,TimeoutExpired
from .forms import studentForm
import time
import os
import glob
import logging
# Create your views here.
def deault_view(request):
    return redirect('login')
def register_view(request):
    form = studentForm(request.POST or None)
    if form.is_valid():
        form.save()
        form = studentForm()
    content = {
        'form' : form
    }
    return render(request,'register.html',content)
def login_view(request,errorMessage=""):
    if(request.session.get('id')):
        return redirect('selectCourse')
    if(request.POST):
        # print('id=',request.POST['id'])
        id = request.POST['id']
        password = request.POST['password']
        try:
            studentObj = Student.objects.get(studentId=id)
            print(studentObj)
        except:
            studentObj= ""
            errorMessage = "此帳號不存在"  
        passwordCheck = False 
        if(studentObj):
            studentPassword = studentObj.password
            if(studentPassword == password):
                passwordCheck = True
                request.session['id'] = id
                request.session['name'] = studentObj.studentName
                request.session.set_expiry(7200) # 兩小時後登出
                print("登入成功")
            else:
                errorMessage="密碼錯誤"
                print("密碼錯誤")
            if(studentObj.isFirstLogin and passwordCheck):
                return redirect('changePassword')
            if(request.session.get('id')):
                return redirect('selectCourse')
    content = {
        'errorMessage' : errorMessage,
    }
        
    return render(request,'login.html',content)

def change_password_view(request,errorMessage=""):
    try:
        if not(request.session.get('id')):
            return redirect('login')
    except KeyError:
        return redirect('login')
    studentObj = Student.objects.get(studentId=request.session.get('id'))
    if(studentObj.isFirstLogin):
        errorMessage = "首次登入請修改密碼"
    if(request.POST):
        if (request.POST['password']== request.POST['passwordCheck'] and request.POST['password']):
       
            
            studentObj.password = request.POST['password']
            studentObj.isFirstLogin = False
            studentObj.save()
            return redirect('selectCourse')
        else:
            errorMessage = "兩次輸入不同！"
    content = {
        'errorMessage' : errorMessage
    }
    return render(request,'changePassword.html',content)
#選擇課程
def select_course_view(request):
    try:
        if not(request.session.get('id')):
            return redirect('login')
    except KeyError:
        return redirect('login')
    
    id = request.session.get('id')
    name = request.session.get('name')
    studentObj = Student.objects.get(studentId=id)
    if(studentObj.isFirstLogin):
            return redirect('changePassword')
    courselist = list(Course_Student.objects.filter(student_id=id))
    coursenamelist = []
    for i in courselist:
        coursenamelist.append(i.course)
    content = {
        'coursenamelist' : coursenamelist

    }


    return render(request,'select_course.html',content)

def list_homework_view(request):
    try:
        if not(request.session.get('id')):
            return redirect('login')
    except KeyError:
        return redirect('login')
    course_id = request.GET['course']
    obj = Homework.objects.filter(course_id=course_id)
    now = timezone.now()
    # obj = Homework.objects.get(homeworkId='1')
    content = {
        'obj' : obj,
        'timeNow' : now
    }
    return render(request,'listHomework.html',content)


def list_problem_view(request,homeworkId):
    try:
        if not(request.session.get('id')):
            return redirect('login')
    except KeyError:
        return redirect('login')
    homeworkObj = Homework.objects.get(homeworkId = homeworkId)
    problemObj = Problem.objects.filter(homework_id=homeworkId)
    now = timezone.now()
    if (homeworkObj.endDateTime <= now):
        return redirect('selectCourse')
    resultList = []
    for i in problemObj:
        resultObj = Result.objects.filter(student_id=request.session.get('id'),problem=i.problemId)
        if resultObj.first():
            if resultObj.first().result:
                resultList.append("已通過")
            else:
                resultList.append("未通過")
        else:
            resultList.append("未繳交")
    content={
        'homeworkId' : homeworkId,
        'problemList' : problemObj,
        'resultList' : resultList,
        'iterList' : zip(problemObj,resultList)

    }
    return render(request,'listProblem.html',content)

def problem_view(request,problemId,errMessage=""):
    try:
        if not(request.session.get('id')):
            return redirect('login')
    except KeyError:
        return redirect('login')
    ldapId = request.session.get('id')
    resultObj = Result.objects.get_or_create(problem_id=problemId,student_id=ldapId)[0]
    problemObj = Problem.objects.get(problemId=problemId)
    homeworkObj = problemObj.homework
    now = timezone.now()
    if(resultObj.result):
        return redirect(list_problem_view,homeworkId=problemObj.homework.homeworkId)
    if (homeworkObj.endDateTime <= now):
        return redirect('selectCourse')

    problem = Problem.objects.filter(problemId=problemId)
    
    content={
        'problem':problem[0],
        'problemId' : problemId,
        'errMessage':errMessage
    }
    return render(request,'problem.html',content)


def judge(request,problemId):
    try:
        if not(request.session.get('id')):
            return redirect('login')
    except KeyError:
        return redirect('login')
    ldapId = request.session.get('id')
    resultObj = Result.objects.get_or_create(problem_id=problemId,student_id=ldapId)[0]
    problemObj = Problem.objects.get(problemId=problemId)
    homeworkObj = problemObj.homework
    now = timezone.now()
    if(resultObj.result):
        return redirect(list_problem_view,homeworkId=problemObj.homework.homeworkId)
    if (homeworkObj.endDateTime <= now):
        return redirect('selectCourse')
    if not request.FILES.get('file'):
        return render(request,'problem.html',{'problemId':problemId})
    
    languageUsed = request.POST.get('language')
    print(request.session.get('id'),'upload for:',problemId)
    file = request.FILES['file']
    fileName = file.name
    fs = FileSystemStorage()
    directory = os.path.abspath(os.path.join(settings.BASE_DIR,'studentUpLoad',request.session['id'],str(problemId)))
    fileAbsPath = os.path.abspath(os.path.join(directory, file.name))
    if not os.path.exists(directory):
        os.makedirs(directory)
    #
    fileDeletes = glob.glob(os.path.join(directory,"*"))
    for fileDelete in fileDeletes:
        os.remove(fileDelete)
    #

    # if os.path.exists(fileAbsPath):
    #     os.remove(fileAbsPath)
    fs.save(fileAbsPath, file)
    #
    cmd = {'language':'java','complieCmd':['javac','-encoding','UTF-8',fileAbsPath],'runCmd':['java','-cp',directory,fileName.replace('.java','')]}
    problemObj = Problem.objects.get(problemId=problemId)
    sampleInPath = os.path.abspath(os.path.join(settings.BASE_DIR,problemObj.sampleIn.__str__()))
    sampleInFile = open(sampleInPath,'r') 
    sampleOutPath = os.path.abspath(os.path.join(settings.BASE_DIR,problemObj.sampleOut.__str__()))
    sampleOutFile=open(sampleOutPath,'r')
    timeout= problemObj.timeout
    #
    result , errMessage = runCommand(cmd,sampleInFile,sampleOutFile,timeout)
   
    # resultObj = Result.objects.get_or_create(student_id=studentId,problem_id=problemId)
    if (result and errMessage=="pass"):
        resultObj.result = True
        resultObj.save()
        print('pass!')
        return redirect(list_problem_view,homeworkId=problemObj.homework.homeworkId)
    problem = Problem.objects.filter(problemId=problemId)
    content = {
        'problem':problem[0],
        'problemId':problemId,
        'errMessage':errMessage
    }
    return render(request,'problem.html',content)



def runCommand(cmd,sampleInFile,sampleOutFile,timeout):
    try:
        spComplie = Popen(cmd['complieCmd'],stdout=PIPE,stderr=PIPE)
        complieOut , complieErr = spComplie.communicate(timeout=timeout)
    except TimeoutExpired:
        spComplie.kill()
        print("編譯時間超過")
        return "","編譯時間超過%d 秒，強制中斷"%timeout
    except Exception as e:
        print('complie err')
        return "","complie err:%s"%e
    complieErr = complieErr.decode('UTF-8')
    print('complie sussess?:', complieErr == "")
    print('complie output:',complieOut,'complie err:',complieErr)
    if not(complieErr == ""):
        return '',"complie error,錯誤代碼:%s"%complieErr
    time.sleep(1)
    
    try:  
        spRun = Popen(cmd['runCmd'],stdin=sampleInFile,stdout=PIPE,stderr=PIPE)
        runOut,runErr = spRun.communicate(timeout=timeout)
        runErr = runErr.decode('UTF-8')
        runOut = runOut.decode('UTF-8')
        sampleOut = "".join(sampleOutFile.readlines())
        print('runOut:',runOut,'runErr:',runErr)
        if (sampleOut== runOut) and runErr=="":
            return (True,'pass')
        elif (runErr):
            return '','執行錯誤,錯誤代碼：%s'%runErr
        else:
            return '','執行結果為：你的輸出與測資不同!'

    except TimeoutExpired:
        spRun.kill()      
        print('執行時間已超過%d'%timeout)
        return '','執行時間已超過%d秒(TLE)'%timeout
    except Exception as e:
        return '','run error %s'%e
    
    
def view_result(request,homeworkId):
    try:
        if not(request.session.get('id')):
            return redirect('login')
    except KeyError:
        return redirect('login')
    homeworkObj = Homework.objects.get(homeworkId = homeworkId)
    problemObj = Problem.objects.filter(homework_id=homeworkId)
    resultList = []
    for i in problemObj:
        resultObj = Result.objects.filter(student_id=request.session.get('id'),problem=i.problemId)
        if resultObj.first():
            if resultObj.first().result:
                resultList.append("已通過")
            else:
                resultList.append("未通過")
        else:
            resultList.append("未繳交")
    content={
        'homeworkId' : homeworkId,
        'problemList' : problemObj,
        'resultList' : resultList,
        'iterList' : zip(problemObj,resultList)

    }
    return render(request,'listResult.html',content)


def logout(request):
    try:
        del request.session['id']
        del request.session['name']
    except KeyError:
        pass
    return redirect('login')
