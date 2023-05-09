from django.shortcuts import render
from datetime import timedelta
from django.utils import timezone
from newspaper.models import Post, Category, Tag
from django.views.generic import ListView, TemplateView,View

class NavigationBar:
    def get_context_data(self,**kwargs):
        context=super().get_context_data(**kwargs)
        context["categories"]= Category.objects.all()[:5]
        context["tags"]=Tag.objects.all()[:10]
        return context
    
class HomeView(NavigationBar,ListView):
    model =Post
    queryset=Post.objects.filter(status="active",published_at__isnull=False).order_by("-published_at")
    template_name="aznews/main/home/home.html"
    context_object_name="posts"

    def get_context_data(self, **kwargs):
        context=super().get_context_data(**kwargs)
        context["trending_posts"]= Post.objects.filter(status="active",published_at__isnull=False).order_by("-published_at", "-views_count")
        context["featured_post"]=( Post.objects.filter(status="active",published_at__isnull=False).order_by ("-views_count").first())
        context["featured_posts"]=( Post.objects.filter(status="active",published_at__isnull=False).order_by ("-views_count")[2:5])
        one_week_ago= timezone.now()-timedelta(days=7)
        context['weekly_top_posts']=Post.objects.filter(status="active", published_at__isnull=False,published_at__gte=one_week_ago,).order_by("-published_at")[:7]        
        context['recent_articles']=Post.objects.filter(status="active", published_at__isnull=False,published_at__gte=one_week_ago,).order_by("-published_at")[:7]        

        context['categories']= Category.objects.all()[:6]     
        context["tags"]= Tag.objects.all()[:10]
        return context

class AboutView(NavigationBar, TemplateView):
    template_name="aznews/about.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["trending_posts"]= Post.objects.filter(status="active",published_at__isnull=False).order_by("-published_at", "-views_count")
        return context
    
class ContactView(View):
    template_name="aznews/main/contact.html"

    def get(self, request,*args,**kwargs):
        categories=Category.objects.all()[:5]
        tags=Tag.objects.all()[:10]
        return render (request, self.template_name,{"tags":tags, "categories": categories},)
