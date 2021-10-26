#don't go for it forms
from django import forms
from .models import Status

class StatusForm(forms.ModelForm):
    class Meta:
        model = Status
        fields = [
                'user',
                'content',
                'image'
                ]
    def clean_content(self,*args,**kwargs):
        content = self.cleaned_data.get('content')
        if len(content) > 10:
            raise forms.ValidationError('Content is too short')
        return content

    def clean(self,*args,**kwargs):
        data = self.cleaned_data
        # import pdb;pdb.set_trace()
        content = data.get('content',None)
        if content == '':
            content = None
        image = data.get('image',None)
        if content is None and image is None:
            raise forms.ValidationError("content or image is required.")
        return super().clean(*args,**kwargs)
