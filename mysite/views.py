from django.shortcuts import render

# Create your views here.
from django.shortcuts import render,redirect
from django.http import HttpResponse
from .models import User,Info,Todo,Schedule,ItemGroup,File
from .forms import InfoForm,TodoForm,BS4ScheduleForm,GroupSelectForm,GroupForm,FileUploadForm
from . import mixins
import datetime
from django.views import generic
from django.core.paginator import Paginator
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin

#base
def base(request):
    return render(request,'mysite/base.html')



#info
#-----------------------------------------------------------------------------------------------------
@login_required
def index(request):
    infolist = Info.objects.all().order_by("-pub_date")[0:5]
    todolist = Todo.objects.filter(status = 0).order_by("deadline")[0:5]
    login_user = request.user
    params ={
        "infolist":infolist,
        'todolist':todolist,
        'login_user':login_user,
    }
    return render(request,"mysite/index.html",params)


@login_required
def info_top(request):
    infolist = Info.objects.all()
    params = {
    'infolist':infolist,
    }
    return render(request,'mysite/info/top.html',params)


@login_required
def info_new(request):
    info_obj = Info()
    params = {
    "InfoForm":InfoForm}
    if (request.method =="POST"):
        title = request.POST["title"]
        content = request.POST["content"]
        sub_content = request.POST["sub_content"]
        owner = request.user
        info = Info(owner = owner,content = content,title = title,sub_content = sub_content)
        info.save()
        params = {
        "title":title,
        'content':content,
        'sub_content':sub_content,
        }
        return render(request,'mysite/info/edit_comp.html',params)

    return render(request,'mysite/info/new.html',params)


@login_required
def info_detail(request,num):
    info = Info.objects.get(id = num)
    params = {
    'info':info,
    }
    return render(request,"mysite/info/detail.html",params)

@login_required
def info_edit_comp(request):
    return render(request,"mysite/info/edit_comp.html")


@login_required
def info_edit(request,num):
    obj = Info.objects.get(id = num)
    if request.method == "POST":
        info = InfoForm(request.POST,instance=obj)
        info.save()
        title = request.POST["title"]
        content = request.POST["content"]
        sub_content = request.POST["sub_content"]
        param = {
        "title":title,
        'content':content,
        'sub_content':sub_content,
        }
        return redirect(to = "mysite:info_edit_comp")
    params = {
    'title':"Infoを編集します",
    "id":num,
    "form":InfoForm(instance=obj)
    }
    return render(request,"mysite/info/edit.html",params)


@login_required
def info_edit_comp(request):
    return render(request,"mysite/info/edit_comp.html")



@login_required
def info_delete(request,num):
    info = Info.objects.get(id = num)
    if(request.method == "POST"):
        info.delete()
        return redirect(to = "mysite:info_edit_comp")
    params = {
        'title':"以下の項目を削除します",
        "id":num,
        "info":info,
    }
    return render(request,"mysite/info/delete.html",params)



#Todo
#-----------------------------------------------------------------------------------------------------

#新規案件登録
@login_required
def todo_new(request):
    todo_obj = Todo()
    params = {
    "TodoForm":TodoForm,
    "GroupSelectForm":GroupSelectForm()}
    if (request.method =="POST"):
        title = request.POST["title"]
        content = request.POST["content"]
        deadline = request.POST["deadline"]
        group = request.POST["group"]
        if group == '':
            owner = request.user
            todo = Todo(owner = owner,content = content,title = title,deadline = deadline)
            todo.save()
        else:
            sel_group = ItemGroup.objects.get(id = group)
            owner = request.user
            todo = Todo(owner = owner,content = content,title = title,deadline = deadline,group=sel_group)
            todo.save()

        params = {
        "title":title,
        'content':content,
        'deadline': deadline,
        }
        return render(request,'mysite/todo/comp.html',params)

    return render(request,'mysite/todo/new.html',params)


@login_required
def todo_edit(request,num):
        obj = Todo.objects.get(id = num)
        if request.method == "POST":
            todo = TodoForm(request.POST,instance=obj)
            todo.save()
            title = request.POST["title"]
            content = request.POST["content"]
            deadline = request.POST["deadline"]
            param = {
            "title":title,
            'content':content,
            'deadline':deadline,
            }
            return redirect(to = "mysite:todo_comp")
        params = {
        'title':"Todoを編集します",
        "id":num,
        "form":TodoForm(instance=obj)
        }
        return render(request,"mysite/todo/edit.html",params)



@login_required
def todo_delete(request,num):
    todo = Todo.objects.get(id = num)
    if(request.method == "POST"):
        todo.delete()
        return redirect(to = "mysite:todo_comp")
    params = {
        'title':"以下の項目を削除します",
        "id":num,
        "obj":todo,
    }
    return render(request,"mysite/todo/delete.html",params)



@login_required
def todo_status(request,num):
    todo = Todo.objects.get(id = num)
    if(request.method == "POST"):
        if(todo.status==0):
            todo.status = 1
            todo.save()
            return redirect(to = "mysite:todo_comp")
        else:
            todo.status = 0
            todo.save()
            return redirect(to = "mysite:todo_comp")
    params = {
        'title':"案件ステータスを変更します",
        "id":num,
        "obj":todo,
    }
    return render(request,"mysite/todo/status_change.html",params)



@login_required
def todo_comp(request):
    return render(request,"mysite/todo/comp.html")



@login_required
def todo_hist(request):
    todolist = Todo.objects.all().filter(status = 1)
    params = {
    "title":"完了案件一覧",
    'todolist':todolist,
    }
    return render(request,"mysite/todo/hist.html",params)



@login_required
#未完了案件一蘭の表示
def todo_top(request):
    todolist = Todo.objects.all().filter(status = 0)
    params = {
    "title":"未完了案件一覧",
    'todolist':todolist,
    }
    return render(request,"mysite/todo/top.html",params)


@login_required
#案件詳細の表示
def todo_detail(request,num):
    todo = Todo.objects.get(id = num)
    params = {
    "title":"案件詳細",
    'todo':todo,
    }
    return render(request,"mysite/todo/detail.html",params)



@login_required
#新規案件グループの作成
def create_itemgroup(request):
    item_group = ItemGroup()
    params = {
    "GroupForm":GroupForm}
    if (request.method =="POST"):
        title = request.POST["title"]
        content = request.POST["content"]
        owner = request.user
        item_group= ItemGroup(owner = owner,content = content,title = title)
        item_group.save()
        params = {
        "title":title,
        'content':content,
        }
        return render(request,'mysite/todo/comp.html',params)

    return render(request,'mysite/todo/create_group.html',params)


@login_required
#案件グループ一覧の表示
def todo_group(request):
    grouplist = ItemGroup.objects.all().filter()
    params ={
    'title':'案件グループ一覧',
    'grouplist':grouplist,
    }
    return render(request,'mysite/todo/group.html',params)


@login_required
#案件グループに表示されている案件一覧の表示
def todo_groupdetail(request,num):
    todolist = Todo.objects.filter(id = num)
    #todolist = Todo.objects.filter(group = group)
    params = {
    "todolist":todolist
    }
    return render(request,"mysite/todo/group_detail.html",params)





@login_required
def file_category(request):

    filelist = File.objects.all()
    params = {
    'filelist':filelist
    }
    return render(request,'mysite/upload/category.html',params)



def file_upload(request):
    params = {
    "FileUploadForm":FileUploadForm,
    }
    if request.method == 'POST':
        form = FileUploadForm(request.POST, request.FILES)
        if not form.is_valid():
            raise ValueError('invalid form')

        file = File()
        file.file = form.cleaned_data['file_data']
        file.save()
        input_data = file.return_file()
        return redirect(to = 'mysite:category_comp')
    return render(request,'mysite/upload/upload.html',params)

@login_required
def category_comp(request):
    return render(request,"mysite/upload/comp.html")

@login_required
def file_detail(request,num):
    file = File.objects.all().filter(id = num)
    file_url = File.objects.get(id=num)
    #file_url = file_url.return_fileurl()
    params = {
    'file':file,
    'file_url':file_url,
    }
    return render(request,'mysite/upload/file_detail.html',params)

@login_required
def file_delete(request,num):
    file = File.objects.get(id = num)
    if(request.method == "POST"):
        file.delete()
        return redirect(to = "mysite:file_comp")
    params = {
        'title':"以下の項目を削除します",
        "file":file,

    }
    return render(request,"mysite/upload/file_delete.html",params)

@login_required
def filedelete_comp(request):
    return render(request,"mysite/upload/comp.html")




#メール
#-----------------------------------------------------------------------------------------------------

@login_required
def mail_top(request):
    return render(request,'mysite/mail/top.html')




#経費精算
#-----------------------------------------------------------------------------------------------------
@login_required
def accounting_top(request):
    return render(request,'mysite/accounting/top.html')









#スケジュール
#-----------------------------------------------------------------------------------------------------


class MonthCalendar(LoginRequiredMixin,mixins.MonthCalendarMixin, generic.TemplateView):
    """月間カレンダーを表示するビュー"""
    template_name = 'mysite/schedule/month.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        calendar_context = self.get_month_calendar()
        context.update(calendar_context)
        return context

class WeekCalendar(LoginRequiredMixin,mixins.WeekCalendarMixin, generic.TemplateView):
    """週間カレンダーを表示するビュー"""
    template_name = 'mysite/schedule/app/week.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        calendar_context = self.get_week_calendar()
        context.update(calendar_context)
        return context

class WeekWithScheduleCalendar(LoginRequiredMixin,mixins.WeekWithScheduleMixin, generic.TemplateView):
    """スケジュール付きの週間カレンダーを表示するビュー"""
    template_name = 'mysite/schedule/week_with_schedule.html'
    model = Schedule
    date_field = 'date'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        calendar_context = self.get_week_calendar()
        context.update(calendar_context)
        return context

class MonthWithScheduleCalendar(LoginRequiredMixin,mixins.MonthWithScheduleMixin, generic.TemplateView):
    """スケジュール付きの月間カレンダーを表示するビュー"""
    template_name = 'mysite/schedule/month_with_schedule.html'
    model = Schedule
    date_field = 'date'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        calendar_context = self.get_month_calendar()
        context.update(calendar_context)
        return context



class MyCalendar(LoginRequiredMixin,mixins.MonthCalendarMixin, mixins.WeekWithScheduleMixin, generic.CreateView):
    """月間カレンダー、週間カレンダー、スケジュール登録画面のある欲張りビュー"""
    template_name = "mysite/schedule/mycalendar.html"
    model = Schedule
    date_field = 'date'
    form_class = BS4ScheduleForm

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        week_calendar_context = self.get_week_calendar()
        month_calendar_context = self.get_month_calendar()
        context.update(week_calendar_context)
        context.update(month_calendar_context)
        return context

    def form_valid(self, form):

        month = self.kwargs.get('month')
        year = self.kwargs.get('year')
        day = self.kwargs.get('day')
        if month and year and day:
            date = datetime.date(year=int(year), month=int(month), day=int(day))
        else:
            date = datetime.date.today()
        schedule = form.save(commit=False)
        schedule.date = date
        schedule.save()
        return redirect('mysite:mycalendar', year=date.year, month=date.month, day=date.day)
