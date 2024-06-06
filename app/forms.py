from django import forms
from multiupload.fields import MultiFileField

class CustomClearableFileInput(forms.ClearableFileInput):
    allow_multiple_selected = True

    def __init__(self, attrs=None):
        super().__init__(attrs)
        self.attrs.update({'multiple': 'multiple'})

class UploadFileForm(forms.Form):
    files = MultiFileField(
        min_num=1,
        max_num=10,
        max_file_size=1024*1024*5,
        widget=CustomClearableFileInput(attrs={'class': 'form-control'}),
        required=True
    )
