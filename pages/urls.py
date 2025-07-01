from django.urls import path
from . import views
from django.contrib.auth.views import LoginView, LogoutView


urlpatterns = [
    path('', views.indexView, name="index"),

    path('login', views.loginView, name="login"),
    # path('login', LoginView.as_view(template_name='pages/login.html')),

	path('logout', LogoutView.as_view(next_page='/')),
    path('signup', views.signUpView, name="signup"),
    path('user_settings', views.userSettingView, name="uset_settings"),
    path('change_username', views.changeUsernameView, name="change_username"),
    path('change_password', views.changePasswordView, name="change_password"),
    path('confirm_account_deletion', views.confirmDeleteAccountView, name="confirm_account_deletion"),
    path('delete_account', views.deleteAccountView, name="delete_account"),
    path('write_post', views.writePostView, name="write_post"),
    path('delete_post', views.deletePostView, name="delete_post"),
    path('post/<int:post_pk>', views.postView, name="post"),
    path('delete_comment/<int:post_pk>', views.deleteCommentView, name="delete_comment"),
]
