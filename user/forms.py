from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from phonenumber_field.formfields import PhoneNumberField
from user.models import User, Profile


class UserLoginForm(AuthenticationForm):
    username = forms.CharField(widget=forms.TextInput(attrs={
        'class': 'form-group', 'placeholder': 'Введите вашу почту'}))
    password = forms.CharField(widget=forms.PasswordInput(attrs={
        'class': 'form-group', 'placeholder': 'Введите пароль'}))

    class Meta:
        model = User
        fields = ('username', 'password')


class UserRegisterForm(UserCreationForm):
    ROLE_CHOICES = [
        (User.RoleStatus.VENDOR, 'Vendor'),
        (User.RoleStatus.CUSTOMER, 'Customer'),
    ]

    username = forms.CharField(widget=forms.TextInput(attrs={
        'class': 'form-group', 'placeholder': 'Введите имя пользователя'}))
    email = forms.CharField(widget=forms.EmailInput(attrs={
        'class': 'form-group', 'placeholder': 'Введите адрес эл. почты'}))
    password1 = forms.CharField(widget=forms.PasswordInput(attrs={
        'class': 'form-group', 'placeholder': 'Введите пароль'}))
    password2 = forms.CharField(widget=forms.PasswordInput(attrs={
        'class': 'form-group', 'placeholder': 'Подтвердите пароль'}))
    role = forms.ChoiceField(choices=ROLE_CHOICES, widget=forms.Select(attrs={
        'class': 'form-group', 'placeholder': 'Выберите роль'}))

    class Meta:
        model = User
        fields = ('username', 'email', 'password1', 'password2', 'role')

    def clean_password2(self):
        cd = self.cleaned_data
        if cd['password1'] != cd['password2']:
            raise forms.ValidationError("Passwords don't match")
        return cd['password2']

    def clean_email(self):
        data = self.cleaned_data['email']
        if User.objects.filter(email=data).exists():
            raise forms.ValidationError("Email already registered")
        return data


class UserEditForm(forms.ModelForm):
    first_name = forms.CharField(widget=forms.TextInput(attrs={
        'class': 'form-group col-md-6', 'placeholder': 'Имя'}))
    last_name = forms.CharField(widget=forms.TextInput(attrs={
        'class': 'form-group col-md-6', 'placeholder': 'Фамилия'}))
    email = forms.EmailField(widget=forms.EmailInput(attrs={
        'class': 'form-group col-md-12', 'placeholder': 'Адрес эл. почты'}))
    phone_number = PhoneNumberField(
        widget=forms.TextInput(attrs={
            'class': 'form-group col-md-12',
            'placeholder': 'Мобильный телефон'
        })
    )

    class Meta:
        model = User
        fields = ('first_name', 'last_name', 'phone_number', 'email',)

    def clean_email(self):
        data = self.cleaned_data['email']
        qs = User.objects.exclude(id=self.instance.id).filter(email=data)
        if qs.exists():
            raise forms.ValidationError('Email already registered')
        return data


class ProfileForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ['date_of_birth']
