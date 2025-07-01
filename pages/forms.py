from django import forms
from django.core.exceptions import ValidationError
from django.contrib.auth.models import User
from django.contrib.auth.hashers import check_password
from .models import Posts, Comments
from django.contrib.auth.password_validation import validate_password


class SignupForm(forms.ModelForm):
    password = password_confirmation = forms.CharField(
        strip=False,
        min_length=8,
        widget=forms.PasswordInput()
    )

    class Meta:
        model = User
        fields = {"username", "password"}

    def clean_username(self):
        username = self.cleaned_data["username"]
        if User.objects.filter(username=username).exists():
            raise ValidationError(
                f"Username '{username}' is already taken. Please choose another one."
            )
        return username

    def clean(self):
        cleaned_data = super().clean()
        password = cleaned_data.get("password")
        pw_conf = cleaned_data.get("password_confirmation")

        if password and pw_conf and password != pw_conf:
            self.add_error(
                "password_confirmation", ValidationError("The password fields didn't match.")
            )

    # def _post_clean(self):
    #     super()._post_clean()
    #     password = self.cleaned_data.get("password")
    #     if password:
    #         try:
    #             validate_password(password, self.instance)
    #         except ValidationError as error:
    #             self.add_error("password", error)


class PostForm(forms.ModelForm):
    class Meta:
        model = Posts
        fields = ["title", "text"]
        labels = {
            "title": "Post title",
            "text": "Post text"
        }


class CommentForm(forms.ModelForm):
    class Meta:
        model = Comments
        fields = ["text"]
        labels = {
            "text": "What would you like to say?"
        }


class ChangeUsernameForm(forms.Form):
# class ChangeUsernameForm(forms.ModelForm):

    username = forms.CharField(max_length=150, label="New username:")
    # class Meta:
    #     model = User
    #     fields = {"username"}
    #     labels = {"username": "New username:"}

    def clean_username(self):
        username = self.cleaned_data["username"]
        if User.objects.filter(username=username).exists():
            raise ValidationError(
                f"Username '{username}' is already taken. Please choose another one."
            )

        return username


class LoginForm(forms.Form):
    username = forms.CharField(max_length=150)
    password = forms.CharField(
        strip=False,
        widget=forms.PasswordInput(),
        min_length=8
    )

    def clean(self):
        cleaned_data = super().clean()
        username = cleaned_data.get("username")
        password = cleaned_data.get("password")

        if username and password:
            user = User.objects.filter(username=username)

            if not user.exists() or password != user[0].password:
            # if not user.exists() or not check_password(password, user[0].password):
                raise ValidationError("Incorrect username or password.")


class ChangePasswordForm(forms.Form):
    # old_password = forms.CharField(
    #     strip=False,
    #     widget=forms.PasswordInput(),
    #     min_length=8,
    # )
    new_password1 = forms.CharField(
        strip=False,
        widget=forms.PasswordInput(),
        min_length=8,
        label="New password:"
    )
    new_password2 = forms.CharField(
        strip=False,
        widget=forms.PasswordInput(),
        min_length=8,
        label="New password confirmation:"
    )

    def __init__(self, user, *args, **kwargs):
        self.user = user
        super().__init__(*args, **kwargs)
    
    # def clean_old_password(self):
    #     old_password = self.cleaned_data["old_password"]
    #
    #     if self.user.password != old_password:
    #     # if not check_password(old_password, self.user.password):
    #         raise ValidationError(
    #             "The old password was entered incorrectly."
    #         )
    #     return old_password

    # def clean_new_password1(self):
    #     password = self.cleaned_data["new_password1"]
    #     validate_password(password, self.user)
    #     return password

    def clean(self):
        cleaned_data = super().clean()
        new_pw1 = cleaned_data.get("new_password1")
        new_pw2 = cleaned_data.get("new_password2")

        if new_pw1 and new_pw2 and new_pw1 != new_pw2:
            self.add_error(
                "new_password2", ValidationError("The password fields didn't match.")
            )

    def save(self):
        self.user.password = self.cleaned_data["new_password1"]
        # self.user.set_password(self.cleaned_data["new_password1"])
        self.user.save()
        return self.user
