from django.db import models
from django.contrib.auth.models import AbstractUser
import datetime
from django.utils import timezone
import os

#独自ユーザーテーブル
class User(AbstractUser):
    pass

#ファイルテーブル
class File(models.Model):

    file = models.FileField(upload_to='media/')

    def return_file(self):
        return self.file.url

#インフォテーブル
class Info(models.Model):
    owner = models.ForeignKey("User",on_delete=models.CASCADE,related_name="info_owner")
    title = models.CharField(max_length = 100)
    content = models.TextField(max_length=1000)
    sub_content = models.TextField(max_length=200)
    pub_date = models.DateField(default=timezone.now)

    def __str__(self):
        return str(self.pub_date) + str(self.content) + "(" + str(self.owner) + ")"

    class Meta:
        ordering = ('-pub_date',)

#Todoテーブル
class Todo(models.Model):
    owner = models.ForeignKey("User",on_delete=models.CASCADE,related_name="todo_owner")
    pub_date = models.DateField(default=timezone.now)
    deadline = models.DateField()
    title = models.CharField(max_length = 100)
    content = models.TextField(max_length=1000)
    status = models.BooleanField(default=False)
    group = models.ForeignKey("ItemGroup",on_delete=models.CASCADE,null=True,blank=True)


    def __str__(self):
        return "期日:" + str(self.deadline) +str(self.content) + "(" + str(self.owner) + ")"

    class Meta:
        ordering = ('deadline',)

#スケジュールテーブル
class Schedule(models.Model):
    #owner = models.ForeignKey("User",on_delete=models.CASCADE,related_name="schedule_owner")
    summary = models.CharField('概要', max_length=50)
    description = models.TextField('詳細な説明', blank=True)
    start_time = models.TimeField('開始時間', default=datetime.time(7, 0, 0))
    end_time = models.TimeField('終了時間', default=datetime.time(7, 0, 0))
    date = models.DateField('日付')
    created_at = models.DateTimeField('作成日', default=timezone.now)

    def __str__(self):
        return self.summary



class ItemGroup(models.Model):
    owner = models.ForeignKey("User",on_delete=models.CASCADE,related_name="itemgroup_owner")
    title = models.CharField(max_length = 100)
    content = models.TextField(max_length=1000,null=True,blank=True)

    def __str__(self):
        return str(self.title)
