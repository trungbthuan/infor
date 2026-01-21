from django import forms
from .models import Profiles

class ProfileForm(forms.ModelForm):
    # Lớp Meta để kết nối Form với Model
    class Meta:
        model = Profiles
        # Chọn các trường bạn muốn hiển thị và cho phép người dùng chỉnh sửa
        fields = ['full_name', 'birthday', 'sex', 'birth_place', 'nation', 'recruitment_day', 'job_title', 'department']
        # Tùy chọn: Thêm các widget để thay đổi kiểu hiển thị của trường
        widgets = {
            'full_name': forms.TextInput(attrs={'class': 'form__input', 'autocomplete': 'off', 'placeholder': ' '}),
            # Sử dụng Input type="date" cho trường birthday
            'birthday': forms.DateInput(attrs={'type': 'date', 'class': 'form__input', 'autocomplete': 'off', 'placeholder': ' '}),
            'sex': forms.TextInput(attrs={'class': 'form__input', 'autocomplete': 'off', 'placeholder': ' '}),
            'birth_place': forms.TextInput(attrs={'class': 'form__input', 'autocomplete': 'off', 'placeholder': ' '}),
            'nation': forms.TextInput(attrs={'class': 'form__input', 'autocomplete': 'off', 'placeholder': ' '}),
            # Sử dụng Input type="date" cho trường recruitment_day
            'recruitment_day': forms.DateInput(attrs={'type': 'date', 'class': 'form__input', 'autocomplete': 'off', 'placeholder': ' '}),
            'job_title': forms.TextInput(attrs={'class': 'form__input', 'autocomplete': 'off', 'placeholder': ' '}),
            'department': forms.TextInput(attrs={'class': 'form__input', 'autocomplete': 'off', 'placeholder': ' '}),

        }
        