from django import forms
from django.contrib.auth import password_validation
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm, PasswordResetForm, SetPasswordForm
from MediaSite.models import Reviews


class ReviewForm(forms.ModelForm):

    class Meta:
        model = Reviews
        fields = ['name', 'text', 'rating']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form__input', 'placeholder': 'Ваше Имя'}),
            'text': forms.Textarea(
                attrs={'class': 'form__textarea', 'id': "contactcomment", 'placeholder': 'Ваш отзыв'}),
        }


class UserRegisterForm(UserCreationForm):
    username = forms.CharField(
        widget=forms.TextInput(attrs={'class': "sign__input", 'placeholder': 'Логин'}))
    password1 = forms.CharField(widget=forms.PasswordInput(attrs={'class': "sign__input", 'placeholder': 'Пароль'}))
    password2 = forms.CharField(
        widget=forms.PasswordInput(attrs={'class': "sign__input", 'placeholder': 'Подтвердите пароль'}))
    is_staff = forms.BooleanField(required=False)
    is_superuser = forms.BooleanField(required=False)


class UserLoginForm(AuthenticationForm):
    username = forms.CharField(
        widget=forms.TextInput(attrs={'class': 'sign__input', 'placeholder': 'Логин'}))
    password = forms.CharField(widget=forms.PasswordInput(attrs={'class': 'sign__input', 'placeholder': 'Пароль'}))


class ResetPasswordForm(PasswordResetForm):
    email = forms.EmailField(
        label=("Email"),
        max_length=254,
        widget=forms.EmailInput(
            attrs={'autocomplete': 'email', 'class': 'sign__input', 'placeholder': ('Enter your Email')})
    )


class SetNewPasswordForm(SetPasswordForm):
    new_password1 = forms.CharField(
        label=("New password"),
        widget=forms.PasswordInput(
            attrs={'autocomplete': 'new-password', 'class': 'sign__input', 'placeholder': ('New password')}),
        strip=False,
        help_text=password_validation.password_validators_help_text_html(),
    )
    new_password2 = forms.CharField(
        label=("New password confirmation"),
        strip=False,
        widget=forms.PasswordInput(
            attrs={'autocomplete': 'new-password', 'class': 'sign__input', 'placeholder': ('Repeat password')}),
    )
