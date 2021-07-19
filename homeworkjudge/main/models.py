from django.db import models
from django.urls import reverse
from multiselectfield import MultiSelectField
# Create your models here.
from django.conf import settings

import os
class Course(models.Model):
    courseId = models.AutoField(primary_key=True)
    courseName = models.CharField(verbose_name="課程名稱",max_length=100)
    studentList = models.FileField(upload_to='studentlist',null=False,verbose_name="學生名單(學號+姓名)")
    def __str__(self):
        return self.courseName
    


class Student(models.Model):
    studentId= models.CharField(primary_key=True,max_length=20,verbose_name="帳號")
    studentName = models.CharField(max_length=20,verbose_name="姓名")
    
    password = models.CharField(max_length=100,verbose_name="密碼", default="password")
    def __str__(self):
        return self.studentName

class Course_Student(models.Model):
    student = models.ForeignKey(Student,on_delete=models.CASCADE)
    course = models.ForeignKey(Course,on_delete=models.CASCADE)
    def __str__(self):
        return self.student.studentName

LANGUAGEOPTION = (
    ('java','java'),
    ('py','python'))
class Homework(models.Model):
    homeworkId = models.AutoField(primary_key=True)
    course = models.ForeignKey(Course,on_delete=models.CASCADE)
    title = models.CharField(max_length=20,default='標題',verbose_name='標題')
    description = models.CharField(max_length=100,default='無描述',null=True,verbose_name='描述')
    languageOption = MultiSelectField(choices=LANGUAGEOPTION,default='java',max_length=10,max_choices=10,verbose_name='開放語言')
    startDateTime = models.DateTimeField(verbose_name='開始時間')
    endDateTime = models.DateTimeField(verbose_name="結束時間")
    attachment = models.FileField(upload_to='homework_attachment/',null=True,blank=True,verbose_name='附件')
    def __str__(self):
        return self.title

class Problem(models.Model):
    problemId = models.AutoField(primary_key=True)
    problemName = models.CharField(max_length=20,null=True,default=1,verbose_name="問題名稱")
    homework = models.ForeignKey(Homework,on_delete=models.CASCADE,default=1)
    timeout = models.IntegerField(verbose_name='限制時間',default=5)
    sampleIn = models.FileField(upload_to='problem/',verbose_name='輸入測資',null=True)
    sampleOut = models.FileField(upload_to='problem/',verbose_name='輸出測資',null=True)
    def __str__(self):
        return self.problemName



class Result(models.Model):
    id = models.AutoField(primary_key=True)
    student = models.ForeignKey(Student,on_delete=models.CASCADE)
    problem = models.ForeignKey(Problem,on_delete=models.CASCADE)
    result = models.BooleanField(default=False,verbose_name="通過")
    language = models.CharField(max_length=25,default='未選擇',verbose_name='使用語言')
    def __str__(self):
        tempStr = f" 學生： {str(self.student.studentName)} 問題： {str(self.problem.problemName)} 是否通過： {str(self.result)}"
        return tempStr

