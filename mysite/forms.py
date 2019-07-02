from django import forms
from .models import User,Info,Todo,Schedule,ItemGroup,File
import bootstrap_datepicker_plus as datetimepicker
import calendar
from collections import deque




#Infoのフォーム
class InfoForm(forms.ModelForm):
    class Meta:
        model = Info
        fields = ['title','content','sub_content']

#Todoのフォーム
class TodoForm(forms.ModelForm):
    class Meta:
        model = Todo
        fields = ['title','content','deadline','group']
        widgets = {
            'deadline': datetimepicker.DatePickerInput(
                format='%Y-%m-%d',
                options={
                    'locale': 'ja',
                    'dayViewHeaderFormat': 'YYYY- MMMM',
                }
            )}

#関連案件のグループ作成フォーム
class GroupForm(forms.ModelForm):
    class Meta:
        model = ItemGroup
        fields = ['title',"content"]


#関連案件のグループ選択フォーム
class GroupSelectForm(forms.Form):
    def __init__(self,*args,**kwargs):
        super(GroupSelectForm,self).__init__(*args,**kwargs)
        self.fields['group'] = forms.ChoiceField(choices=[('-','-')] + [(item.title,item.title)\
        for item in ItemGroup.objects.all()],)






#ファイルアップロードフォーム
class FileUploadForm(forms.Form):
    file_data = forms.FileField()





#スケジュール管理
class BS4ScheduleForm(forms.ModelForm):
    """Bootstrapに対応するためのModelForm"""

    class Meta:
        model = Schedule
        fields = ('summary', 'description', 'start_time', 'end_time')
        widgets = {
            'summary': forms.TextInput(attrs={
                'class': 'form-control',
            }),
            'description': forms.Textarea(attrs={
                'class': 'form-control',
            }),
            'start_time': forms.TextInput(attrs={
                'class': 'form-control',
            }),
            'end_time': forms.TextInput(attrs={
                'class': 'form-control',
            }),
        }

    def clean_end_time(self):
        start_time = self.cleaned_data['start_time']
        end_time = self.cleaned_data['end_time']
        if end_time <= start_time:
            raise forms.ValidationError(
                '終了時間は、開始時間よりも後にしてください'
            )
        return end_time
