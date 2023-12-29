from django import forms
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import ReadOnlyPasswordHashField

User = get_user_model()

class UserAdminCreationForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput)
    password_2 = forms.CharField(label="Confirm password",widget=forms.PasswordInput)
    username = forms.CharField(label='Username',widget=forms.TextInput)
    
    class Meta:
        model = User
        fields = ['username']
        
    def clean_username(self):
        username = self.cleaned_data['username']
        try:
            User.objects.get(username=username)
        except User.DoesNotExist:
            return username
        raise forms.ValidationError('This username is already in use.')
        
    def clean(self): #during validation
        cleaned_data = super().clean() #getting cleaned data from form
        
        password = cleaned_data.get('password')
        password_2 = cleaned_data.get('password_2')
        
        if password is not None and password != password_2:
            self.add_error(password_2,"Your passwords must match!")
            
        return cleaned_data
    
    def save(self,commit=True):  #during saving user
        user = super().save(commit=False) #getting data from user form 
        user.set_password(self.cleaned_data['password'])
        if commit:
            user.save()
        return user
    
    
class UserAdminChangeForm(forms.ModelForm):
    password = ReadOnlyPasswordHashField()
    
    class Meta:
        model = User
        fields ='__all__'
        
        
    def clean_password(self):
        return self.initial['password']
    
# class LoginForm(forms.ModelForm):
#     email = forms.CharField(label='Email')
#     password = forms.CharField(widget=forms.PasswordInput)


# class RegisterForm(forms.ModelForm):
#     password = forms.CharField(widget=forms.PasswordInput)
#     password_2 = forms.CharField(label="Confirm password",widget=forms.PasswordInput)
#     username = forms.CharField(label='Username',widget=forms.TextInput)
#     class Meta:
#         model = User
#         fields = ['username','email']
    
#     def clean(self): #during validation
#         clean_data = super().clean() #getting cleaned data from form
        
#         password = clean_data.get('password')
#         password_2 = clean_data.get('password_2')
        
#         if password is not None and password != password_2:
#             self.add_error(password_2,"Your passwords must match!")
            
#         return clean_data
    
#     def save(self,commit=True):  #during saving user
#         user = super().save(commit=False) #getting data from user form 
#         user.set_password(self.clean_data['password'])
#         if commit:
#             user.save()
#         return user
    