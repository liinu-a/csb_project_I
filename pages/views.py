from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth import login, logout, update_session_auth_hash
from django.contrib.auth.models import User
from django.contrib.auth.forms import PasswordChangeForm
from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_POST
from django.core.exceptions import PermissionDenied
from django.db import connection
from django.db.models import Count
from .models import Posts, Comments
from .forms import SignupForm, PostForm, CommentForm, ChangeUsernameForm, LoginForm, ChangePasswordForm


def indexView(request):
    posts = Posts.objects.annotate(num_comments=Count("comments"))
    return render(request, "pages/index.html", {"user": request.user, "posts": posts})


def loginView(request):
    if request.user.is_authenticated:
        messages.info(request, f"You are already logged in as {request.user.username}.")
        return redirect("/")

    if request.method == "POST":
        form = LoginForm(request.POST)
        if form.is_valid():
            user = User.objects.get(username=form.cleaned_data["username"])
            login(request, user)
            return redirect("/")
    else:
        form = LoginForm()

    return render(request, "pages/login.html", {"form": form})


def signUpView(request):
    if request.method == "POST":
        form = SignupForm(request.POST)
        if form.is_valid():

            user = form.save() # Does not hash the password.
            # user = form.save(commit=False)
            # user.set_password(form.cleaned_data["password"])
            # user = form.save(commit=True)

            login(request, user)
            messages.success(
                request, f"Hello {user.username}! Your account was created successfully."
            )
            return redirect("/")
    else:
        form = SignupForm()

    return render(request, "pages/signup.html", {"form": form})


@login_required
def userSettingView(request):
    return render(request, "pages/user_settings.html", {"user": request.user})


@login_required
def changePasswordView(request):
    if request.method == "POST":
        form = ChangePasswordForm(request.user, request.POST)
        # form = PasswordChangeForm(request.user, request.POST)

        if form.is_valid():
            user = form.save()
            update_session_auth_hash(request, user)
            messages.success(request, "Your password was updated successfully.")
            return redirect("/user_settings")
    else:
        form = ChangePasswordForm(request.user)
        # form = PasswordChangeForm(request.user)

    return render(request, "pages/change_password.html", {"form": form})


@login_required
def changeUsernameView(request):
    user = request.user
    if request.method == "POST":
        form = ChangeUsernameForm(request.POST)
        if form.is_valid():
            new_username = form.cleaned_data["username"]

            with connection.cursor() as cursor:
                cursor.execute(
                    "UPDATE auth_user SET username = '%s' WHERE id = '%s'" % (new_username, request.user.pk)
                )
            # user.username = new_username
            # user.save()

            messages.success(
                request, f"Your username was changed succesfully to {new_username}!"
            )
            return redirect("/user_settings")
    else:
        form = ChangeUsernameForm()

    return render(request, "pages/change_username.html", {"user": user, "form": form})


@login_required
@require_POST
def deleteAccountView(request):
    request.user.delete()
    logout(request)
    messages.success(request, "Account deleted.")
    return redirect("/")


@login_required
def confirmDeleteAccountView(request):
    return render(request, "pages/confirm_account_deletion.html")


@login_required
def writePostView(request):
    if request.method == "POST":
        form = PostForm(request.POST)
        if form.is_valid():
            post = form.save(commit=False)
            post.writer = request.user
            post = form.save(commit=True)
            messages.success(request, "Your post was created successfully!")
            return redirect(f"/post/{post.pk}")
    else:
        form = PostForm()

    return render(request, "pages/write_post.html", {"form": form})


@login_required
@require_POST
def deletePostView(request):
    try:
        post = Posts.objects.get(pk=request.POST.get("post-id"))

        # if post.writer == request.user:
        #     post.delete()
        #     messages.success(request, "Post deleted successfully.")
        # else:
        #     raise PermissionDenied("Permission to delete the post denied.")

        post.delete()
        messages.success(request, "Post deleted successfully.")
    except Posts.DoesNotExist:
        messages.error(request, "The post you tried to delete does not exist.")

    return redirect("/")


def postView(request, post_pk):
    try:
        post = Posts.objects.get(pk=post_pk)
    except Posts.DoesNotExist:
        messages.error(request, "Post could not be found.")
        return redirect("/")
    
    reply_to_id = None
    form = CommentForm()

    if request.method == "POST":
        if not request.user.is_authenticated:
            messages.error(request, "Commenting requires logging in.")
            return redirect("/login")

        try:
            reply_to_id = int(request.POST.get("modal-reply-to-id"))
            reply_to = None if reply_to_id == -1 else Comments.objects.get(pk=reply_to_id)

            if reply_to and reply_to.under_post.pk != post_pk:
                messages.error(request, "The comment you tried to reply to is under a different post.")
                return redirect("/")

            form = CommentForm(request.POST)
            if form.is_valid():
                comment = form.save(commit=False)
                comment.writer = request.user
                comment.under_post = post
                comment.reply_to = reply_to
                comment = form.save(commit=True)
                messages.success(request, "Your comment was posted successfully.")
                reply_to_id = None
                form = CommentForm()

        except (TypeError, ValueError, Comments.DoesNotExist, ValueError):
            reply_to_id = None
            messages.error(request, "The comment you tried to reply to is invalid.")

    return render(
        request, "pages/post.html", {
            "user": request.user,
            "post": post,
            "comments": Comments.objects.filter(under_post=post_pk),
            "modal_reply_to": reply_to_id,
            "form": form
        }
    )


@login_required
@require_POST
def deleteCommentView(request, post_pk):
    try:
        comment = Comments.objects.get(pk=request.POST.get("comment-id"))
        if comment.writer == request.user:
            comment.delete()
            messages.success(request, "Comment deleted successfully.")
        else:
            raise PermissionDenied("Permission to delete the comment denied.")
    except Comments.DoesNotExist:
        messages.error(request, "The comment you tried to delete does not exist.")

    return redirect(f"/post/{post_pk}")
