from django.contrib.auth.decorators import login_required
from django.shortcuts import render,HttpResponseRedirect,redirect

# Create your views here.
from blog_app.models import Post
from django.utils import timezone
from blog_app.forms import PostForm


def post_list(request):
    posts = Post.objects.filter(published_at__isnull=False).order_by("-published_at")
    return render(request, "post_list.html", {"posts": posts},)

def post_detail(request,pk):
    post= Post.objects.get(pk=pk)
    return render(
        request,"post_detail.html",{"post": post}
    )

@login_required
def draft_list(request):
    posts = Post.objects.filter(published_at__isnull=True).order_by("-published_at")
    return render(request, "draft_list.html", {"posts": posts},)
    # return render(request, "draft_list.html", {"draft": drafts},)

@login_required
def draft_detail(request,pk):
    post= Post.objects.get(pk=pk, published_at__isnull=True)
    return render(
        request,"draft_detail.html",{"post": post}
    )

@login_required
def draft_publish(request,pk):
    post=Post.objects.get(pk=pk,published_at__isnull=True)
    post.published_at=timezone.now()
    post.save()
    return HttpResponseRedirect("/")

@login_required
def post_delete(request,pk):
    post=Post.objects.get(pk=pk)
    post.delete()
    return HttpResponseRedirect("/")

@login_required
def post_create(request):
    form = PostForm()
    if request.method=="POST":
        form= PostForm(request.POST)
        if form.is_valid():
            post= form.save(commit=False)
            post.author = request.user
            post.save()
            return redirect("draft-list")
       
    #write logic here to add new post

    return render(request,"post_create.html", {"form": form})

@login_required
def post_update(request, pk):
    post = Post.objects.get(pk=pk)
    form = PostForm(instance=post)
    if request.method=="POST":
        form= PostForm(request.POST, instance=post)
        if form.is_valid():
            post.save()
            if post.published_at:
                return redirect("post-detail",post.pk)
            else:
                return redirect("draft-detail", post.pk)
           
       
    #write logic here to add new post

    return render(request,"post_create.html", {"form": form})