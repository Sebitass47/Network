from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse
from django.contrib import messages
from .models import *
import json
from django.http import JsonResponse
from django.core.paginator import Paginator
from django.views.decorators.csrf import csrf_exempt



def index(request):
    posts = Posts.objects.all().order_by("timestamp").reverse()
    paginator = Paginator(posts, 10)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    return render(request, "network/index.html",{
        'page_obj': page_obj
    })


def login_view(request):
    if request.method == "POST":

        # Attempt to sign user in
        username = request.POST["username"]
        password = request.POST["password"]
        user = authenticate(request, username=username, password=password)

        # Check if authentication successful
        if user is not None:
            login(request, user)
            messages.add_message(request, messages.SUCCESS, 'Login Successful')
            return HttpResponseRedirect(reverse("index"))
        else:
            messages.add_message(request, messages.WARNING, 'Invalid username and/or password')
            return render(request, "network/login.html")
    else:
        return render(request, "network/login.html")


def logout_view(request):
    logout(request)
    messages.add_message(request, messages.SUCCESS, 'Logout Successful')
    return HttpResponseRedirect(reverse("index"))


def register(request):
    if request.method == "POST":
        username = request.POST["username"]
        email = request.POST["email"]

        # Ensure password matches confirmation
        password = request.POST["password"]
        confirmation = request.POST["confirmation"]
        if password != confirmation:
            messages.add_message(request, messages.WARNING, 'Passwords must match.')
            return render(request, "network/register.html")

        if len(username) <= 0 or len(email) <= 0 or len(password) <= 0:
            messages.add_message(request, messages.WARNING, 'Information is missing.')
            return render(request, "network/register.html")
        # Attempt to create new user
        try:
            user = User.objects.create_user(username, email, password)
            user.save()
        except IntegrityError:
            messages.add_message(request, messages.WARNING, 'Username already taken.')
            return render(request, "network/register.html")

        login(request, user)
        messages.add_message(request, messages.SUCCESS, 'Register Successful')
        return HttpResponseRedirect(reverse("index"))
    else:
        return render(request, "network/register.html")

@login_required
def new_post(request):
    if request.method == "POST":
        content = request.POST["content"]
        if content is not None:
            user_id = request.user.id
            user_id = User.objects.get(id=user_id)
            post = Posts(content=content, created_by=user_id)
            post.save()
            messages.add_message(request, messages.SUCCESS, 'Post shared successfully')
            return HttpResponseRedirect(reverse("index"))


def user(request, id):
    user = User.objects.get(id=id)
    posts = Posts.objects.filter(created_by=id).order_by("timestamp").reverse()
    follow = Following.objects.filter(user_id=user).count()
    following = Following.objects.filter(following=user).count()
    paginator = Paginator(posts, 10)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    return render(request, "network/index.html",{
        "profile": user,
        'page_obj': page_obj,
        "follow": follow,
        "following": following,
    })


#JS
@login_required
def follow(request, user_id):
    #Seguir o dejar de seguir al usuario.
    if request.method == "POST":
        
        try:
            user = User.objects.get(id=user_id)
            
        except User.DoesNotExist:
            return JsonResponse({"message": "Not found"}, status=404)
        #Checar si los usarios ya se siguen 
        try: 
            test = Following.objects.get(user_id=request.user, following=user)
        #Si no se siguen, haremos que se sigan 
        except Following.DoesNotExist:
            follow = Following(user_id=request.user, following=user)
            follow.save()
            return JsonResponse({"message": "Following"}, status=200)
        
        #Si ya se siguen, tenemos que hacer que se dejen de seguir.
        test.delete()
        return JsonResponse({"message": "Unfollow"}, status=200)
    
    #Checar si se siguen o no
    else:
        #Ver si se siguen
        try: 
            test = Following.objects.get(user_id=request.user, following=user_id)
        #Si no se siguen, mandar un false.
        except Following.DoesNotExist:
            return JsonResponse({"message": "Follow"})
        
        #Si si se siguen, mandar un True
        return JsonResponse({"message": "Following"})


@login_required
def following(request):
    posts = Posts.objects.filter(created_by__in=Following.objects.values_list("following").filter(user_id=request.user)).order_by("timestamp").reverse()
    paginator = Paginator(posts, 10)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    return render(request, "network/index.html",{
        'page_obj': page_obj
    })


@login_required
def profile(request):
    posts = Posts.objects.filter(created_by=request.user.id).order_by("timestamp").reverse()
    paginator = Paginator(posts, 10)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    return render(request, "network/index.html",{
        'page_obj': page_obj
    })

#JS
@login_required
def edit(request, post_id):
    try:
        post = Posts.objects.get(created_by=request.user, pk=post_id)
    except Posts.DoesNotExist:
        return JsonResponse({"error": "Sometime is wrong."}, status=404)

    content = json.loads(request.body)
    if content.get("content") is not None:
        post.content = content["content"]
        post.save()
    return JsonResponse({"success": "Edit save"}, status=200)


@csrf_exempt
@login_required
def new_heart(request, post_id):
    try:
        post = Posts.objects.get(pk=post_id)
    except Posts.DoesNotExist:
        return JsonResponse({"error": "Sometime is wrong."}, status=404)


    if request.method == "POST":
        delete = Heart.objects.get(post_id=post_id, user_id=request.user)
        delete.delete()
        post.hearts = int(post.hearts) - 1
        post.save()
        return JsonResponse({"success": "Edit save"}, status=200)
        
    else:
        post = Posts.objects.get(pk=post_id)
        new = Heart(post_id=post, user_id=request.user)
        new.save()
        post.hearts = int(post.hearts) + 1
        post.save()
        return JsonResponse({"success": "Edit save"}, status=200)

@csrf_exempt
@login_required
def heart(request):
    if request.method == "POST":
        content = json.loads(request.body)
        publications = content["content"]
        result = {}
        for publication in publications:
            try:
                like = Heart.objects.get(post_id=publication, user_id=request.user)
                result[publication] = True
            except Heart.DoesNotExist:
                result[publication] = False
        return JsonResponse({"result": result}, status=200)


@login_required
def delete(request, post_id):
    try:
        post = Posts.objects.get(id=post_id, created_by=request.user)
    except Posts.DoesNotExist:
        return JsonResponse({"error": "Sometime is wrong."}, status=404)

    post.delete()
    return JsonResponse({"success": "Post delete"}, status=200)

   