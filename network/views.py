import json
from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseBadRequest, HttpResponseRedirect, JsonResponse
from django.shortcuts import render
from django.urls import reverse
from django.core.paginator import Paginator
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_exempt

from .models import *

@login_required
def index(request):
    posts_all = Post.objects.order_by('-date')
    posts_paginated = Paginator(posts_all, 10)
    page_num = 1
    if request.GET.get("page"):
        page_num = request.GET["page"]

    posts_page = posts_paginated.page(page_num)
    
    return render(request, "network/index.html", {
        "posts": posts_page
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
def post_submit(request):
    if body := request.POST.get("body"):
        post = Post(poster=request.user, body=body)
        post.save()
        return HttpResponseRedirect(reverse("index"))
    return HttpResponseBadRequest("You couldn't submit post.")

@csrf_exempt
@login_required
def post(request, post_id):

    # Query for requested post
    user = request.user
    post = Post.objects.get(pk=post_id)

    if request.method == "POST":
        data = json.loads(request.body)
        if data.get("like") is not None:
            print(data["like"])
            if data["like"] is True:
                user.likes.add(post)
            else:
                user.likes.remove(post)
        if  comment := data.get("comment"):
            Comment.objects.create(post=post, commenter=user, body=comment)
        return HttpResponse(status=204)

    # Post change must be via GET or PUT
    else:
        return JsonResponse({
            "error": "PUT request required."
        }, status=400)
        