import json
from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse
from .models import User,Post,Follow
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.core.paginator import Paginator
from django.contrib.auth.decorators import login_required




def index(request):
    posts=Post.objects.all().order_by('-date')
    paginator = Paginator(posts, 10)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    return render(request, "network/index.html",{"page_obj": page_obj})

@csrf_exempt
def newpost(request):
    if request.method=="POST":
        data = json.loads(request.body)
        post=data.get("post")
        if len(post)>0:
            getpost = Post.objects.create(content=post, user=request.user)
            return JsonResponse(getpost)
        else:
            return JsonResponse({
                "error": "there needs to be some content"}, status=400)



def login_view(request):
    if request.method == "POST":

        # Attempt to sign user in
        username = request.POST["username"]
        password = request.POST["password"]
        user = authenticate(request, username=username, password=password)

        # Check if authentication successful
        if user is not None:
            login(request, user)
            return HttpResponseRedirect(reverse("index"))
        else:
            return render(request, "network/login.html", {
                "message": "Invalid username and/or password."
            })
    else:
        return render(request, "network/login.html")


def logout_view(request):
    logout(request)
    return HttpResponseRedirect(reverse("index"))


def register(request):
    if request.method == "POST":
        username = request.POST["username"]
        email = request.POST["email"]

        # Ensure password matches confirmation
        password = request.POST["password"]
        confirmation = request.POST["confirmation"]
        if password != confirmation:
            return render(request, "network/register.html", {
                "message": "Passwords must match."
            })

        # Attempt to create new user
        try:
            user = User.objects.create_user(username, email, password)
            user.save()
        except IntegrityError:
            return render(request, "network/register.html", {
                "message": "Username already taken."
            })
        login(request, user)
        return HttpResponseRedirect(reverse("index"))
    else:
        return render(request, "network/register.html")

@login_required
def profile(request,user):
    user1=User.objects.get(username=user)
    check_user=Follow.objects.get(user=user1)
    followers=check_user.followers.all()
    following = check_user.following.all()

    posts = Post.objects.filter(user=user1).order_by('-date')
    paginator = Paginator(posts, 10)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    return render(request,"network/profile.html",{"user":user,"followers":followers,"following":following,"page_obj":page_obj})

def follow_unfollow(request,user):
    user1=User.objects.get(username=request.user)
    user2=User.objects.get(username=user)
    if user1==user2:
        return HttpResponseRedirect(reverse("index"))


    logged_user=Follow.objects.get(user=user1)
    check_user = Follow.objects.get(user=user2)
    followers=check_user.followers.all()

    if request.user in followers:
        check_user.followers.remove(user1)
        logged_user.following.remove(user2)
    else:
        check_user.followers.add(user1)
        logged_user.following.add(user2)
    return HttpResponseRedirect(reverse("profile",args=(user,)))

@login_required
def following(request):
    user1 = User.objects.get(username=request.user)
    logged_user = Follow.objects.get(user=user1)
    following = logged_user.following.all()
    posts=Post.objects.filter(user__in=following).order_by('-date')
    paginator = Paginator(posts, 10)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    return render(request,"network/following.html",{"page_obj":page_obj})

@csrf_exempt
def edit(request):
    if request.method=="PUT":
        data = json.loads(request.body)
        content = data.get("content")
        if content is not None:
            id=data.get("id")
            post=Post.objects.get(id=id)
            post.content=content
            post.save()
            return JsonResponse(post.serialize())

        else:
            return JsonResponse({
                "error": "there needs to be some content"}, status=400)
    else:
        return JsonResponse({
            "error": "only PUT request"}, status=400)

@csrf_exempt
def like(request):
    if request.method=="PUT":
        user=User.objects.get(username=request.user)
        data=json.loads(request.body)
        id=data.get("id")
        post=Post.objects.get(id=id)

        likedby=post.likes.all()
        if user in likedby:
            post.likes.remove(user)
        else:
            post.likes.add(user)
        post=Post.objects.get(id=id)

        return JsonResponse({"likes":post.likes.count()})
        #return JsonResponse({"message":"success","post":post},status=201)
    else:
        return JsonResponse({
            "error": "only PUT request"}, status=400)



















