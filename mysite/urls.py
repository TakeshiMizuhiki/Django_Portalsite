from django.urls import path,include
from . import views

app_name = "mysite"

urlpatterns = [
    path('', views.index,name="index"),
    #Schedule
    #---------------------------------------------------------------------------------------------------------------------------------
    path('mycalendar/', views.MyCalendar.as_view(), name='mycalendar'),
    path('mycalendar/<int:year>/<int:month>/<int:day>/', views.MyCalendar.as_view(), name='mycalendar'),
    path('month/', views.MonthCalendar.as_view(), name='month'),
    path('month/<int:year>/<int:month>/', views.MonthCalendar.as_view(), name='month'),
    path('week/', views.WeekCalendar.as_view(), name='week'),
    path('week/<int:year>/<int:month>/<int:day>/', views.WeekCalendar.as_view(), name='week'),
    path('week_with_schedule/', views.WeekWithScheduleCalendar.as_view(), name='week_with_schedule'),
    path('week_with_schedule/<int:year>/<int:month>/<int:day>/',views.WeekWithScheduleCalendar.as_view(),name='week_with_schedule'),
    path('month_with_schedule/',views.MonthWithScheduleCalendar.as_view(), name='month_with_schedule'),
    path('month_with_schedule/<int:year>/<int:month>/',views.MonthWithScheduleCalendar.as_view(), name='month_with_schedule'),
    #Info
    #---------------------------------------------------------------------------------------------------------------------------------
    path("info_top/",views.info_top,name='info_top'),
    path('info_new/',views.info_new,name = "info_new"),
    path('info_edit/<int:num>',views.info_edit,name = "info_edit"),
    path('info_edit_comp/',views.info_edit_comp,name = "info_edit_comp"),
    path('info_delete/<int:num>',views.info_delete,name = "info_delete"),
    path("info_detail/<int:num>",views.info_detail,name='info_detail'),


    #Todo
    #---------------------------------------------------------------------------------------------------------------------------------
    path('todo_new/',views.todo_new,name = "todo_new"),
    path('todo_edit/<int:num>',views.todo_edit,name = "todo_edit"),
    path('todo_delete/<int:num>',views.todo_delete,name = "todo_delete"),
    path('todo_status/<int:num>',views.todo_status,name = "todo_status"),
    path('todo_hist/',views.todo_hist,name="todo_hist"),
    path('todo_top/',views.todo_top,name="todo_top"),
    path('todo_detail/<int:num>',views.todo_detail,name="todo_detail"),
    path('create_itemgroup/',views.create_itemgroup,name="create_itemgroup"),
    path('todo_group/',views.todo_group,name="todo_group"),
    path('todo_groupdetail/<int:num>',views.todo_groupdetail,name="todo_groupdetail"),
    path('todo_comp/',views.todo_comp,name = "todo_comp"),

    
    #FileUpload
    #---------------------------------------------------------------------------------------------------------------------------------
    path('upload/',views.file_upload,name="file_upload"),
    path('category/',views.file_category,name="file_category"),
    path('category_comp/',views.category_comp,name="category_comp"),
    path('file_detail/<int:num>',views.file_detail,name="file_detail"),
    path('file_delete/<int:num>',views.file_delete,name="file_delete"),
    path('filedelete_comp/',views.filedelete_comp,name="filedelete_comp"),
    path('file_comp/',views.filedelete_comp,name="file_comp"),

    #Mail
    #---------------------------------------------------------------------------------------------------------------------------------
    path('mail_top/',views.mail_top,name="mail_top"),

    #Accounting
    #---------------------------------------------------------------------------------------------------------------------------------
    path('accounting_top/',views.accounting_top,name="accounting_top"),



]
