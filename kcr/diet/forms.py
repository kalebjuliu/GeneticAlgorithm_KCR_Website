from django import forms
from diet.models import UserBMI


class UserBMIForm(forms.ModelForm):
    class Meta:
        model = UserBMI
        fields = ('user', 'umur', 'tinggi_badan', 'berat_badan',
                  'jenis_kelamin', 'tingkat_aktivitas')

    def __init__(self, *args, **kwargs):
        super(UserBMIForm, self).__init__(*args, **kwargs)
        self.fields['user'].disabled = True
