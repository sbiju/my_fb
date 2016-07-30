try:
    from urllib import quote_plus #python 2
except:
    pass

try:
    from urllib.parse import quote_plus #python 3
except: 
    pass

from django.contrib.auth.models import User
from friendship.models import Friend, Follow, FriendshipRequest
from django.contrib import messages
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.db.models import Q
from django.http import HttpResponse, HttpResponseRedirect, Http404
from django.shortcuts import render, get_object_or_404, redirect
from django.utils import timezone
from django.contrib.auth.decorators import login_required
from django.views.generic import CreateView, TemplateView, UpdateView, DetailView, View
from django.contrib.auth.models import User
from django.contrib.sessions.models import Session
from django.utils import timezone
from django.core.mail import send_mail
from django.conf import settings


from .forms import BlogPostForm, BlogShareForm, ContactusForm
from .models import BlogPost
from blog_main.mixins import LoginRequiredMixin


def get_current_users():
    active_sessions = Session.objects.filter(expire_date__gte=timezone.now())
    user_id_list = []
    for session in active_sessions:
        data = session.get_decoded()
        user_id_list.append(data.get('_auth_user_id', None))
    # Query all logged in users based on id list
    return User.objects.filter(id__in=user_id_list)


def loggedusers(request):
    queryset = get_current_users().order_by('-last_login')
    count = get_current_users().count()
    context = {
        "queryset": queryset,
        "count" : count,
    }
    return render (request,'home.html',context)


class NewBlogPostView(LoginRequiredMixin, CreateView):
    form_class = BlogPostForm
    template_name = 'posts/post_form.html'

    def dispatch(self, request, *args, **kwargs):
        return super(NewBlogPostView, self).dispatch(request, *args, **kwargs)

    def form_valid(self, form):
        blog_post_obj = form.save(commit=False)
        blog_post_obj.owner = self.request.user
        blog_post_obj.save()
        return HttpResponseRedirect(blog_post_obj.get_absolute_url())


@login_required
def post_detail(request, slug=None):
    instance = get_object_or_404(BlogPost, slug=slug)
    if instance.publish > timezone.now() or instance.draft:
        if not request.user.is_staff or not request.user.is_superuser:
            raise Http404
    share_string = quote_plus(instance.content)
    context = {
        "title": instance.title,
        "instance": instance,
        "share_string": share_string,
    }
    return render(request, "posts/post_detail.html", context)


@login_required
def post_list(request):
    today = timezone.now().date()
    friends_list = Friend.objects.friends(request.user)
    # current_user = get_current_users()
    queryset_list = BlogPost.objects.filter(owner=request.user).filter(is_shared=False)
    query = request.GET.get("q")
    if query:
        queryset_list = queryset_list.filter(
                Q(title__icontains=query)|
                Q(content__icontains=query)|
                Q(owner__first_name__icontains=query) |
                Q(owner__last_name__icontains=query)
                ).distinct()
    paginator = Paginator(queryset_list, 4)
    page_request_var = "page"
    page = request.GET.get(page_request_var)
    try:
        queryset = paginator.page(page)
    except PageNotAnInteger:
        # If page is not an integer, deliver first page.
        queryset = paginator.page(1)
    except EmptyPage:
        # If page is out of range (e.g. 9999), deliver last page of results.
        queryset = paginator.page(paginator.num_pages)

    context = {
        "object_list": queryset,
        "title": "Posts",
        "page_request_var": page_request_var,
        "today": today,
        "user_list": friends_list,
    }
    return render(request, "posts/post_list.html", context)


@login_required
def post_list_all(request):
    today = timezone.now().date()
    queryset_list = BlogPost.objects.all()
    query = request.GET.get("q")
    if query:
        queryset_list = queryset_list.filter(
                Q(title__icontains=query)|
                Q(content__icontains=query)|
                Q(owner__first_name__icontains=query) |
                Q(owner__last_name__icontains=query)
                ).distinct()
    paginator = Paginator(queryset_list, 4)
    page_request_var = "page"
    page = request.GET.get(page_request_var)
    try:
        queryset = paginator.page(page)
    except PageNotAnInteger:
        # If page is not an integer, deliver first page.
        queryset = paginator.page(1)
    except EmptyPage:
        # If page is out of range (e.g. 9999), deliver last page of results.
        queryset = paginator.page(paginator.num_pages)

    context = {
        "object_list": queryset,
        "title": "Posts",
        "page_request_var": page_request_var,
        "today": today,
    }
    return render(request, "posts/post_list_all.html", context)


@login_required
def post_shared_list( request):
    today = timezone.now().date()
    queryset_list = BlogPost.objects.filter(is_shared=True)
    query = request.GET.get("q")
    if query:
        queryset_list = queryset_list.filter(
                Q(title__icontains=query)|
                Q(content__icontains=query)|
                Q(owner__first_name__icontains=query) |
                Q(owner__last_name__icontains=query)
                ).distinct()
    paginator = Paginator(queryset_list, 4)
    page_request_var = "page"
    page = request.GET.get(page_request_var)
    try:
        queryset = paginator.page(page)
    except PageNotAnInteger:
        # If page is not an integer, deliver first page.
        queryset = paginator.page(1)
    except EmptyPage:
        # If page is out of range (e.g. 9999), deliver last page of results.
        queryset = paginator.page(paginator.num_pages)

    context = {
        "shared_list": queryset,
        "title": "Shared Posts",
        "page_request_var": page_request_var,
        "today": today,
    }
    return render(request, "posts/post_shared.html", context)


@login_required
def post_share(request, slug=None):
    instance = get_object_or_404(BlogPost, slug=slug)
    form = BlogShareForm(request.POST or None, request.FILES or None, instance=instance)
    if form.is_valid():
        instance = form.save(commit=False)
        instance.save()
        messages.success(request, 'Post shared Successfully')
        return HttpResponseRedirect(instance.get_absolute_url())

    context = {
        "title": instance.title,
        "instance": instance,
        "form":form,
    }
    return render(request, "posts/post_share_form.html", context)


@login_required
def post_update(request, slug=None):
    instance = get_object_or_404(BlogPost, slug=slug)
    form = BlogPostForm(request.POST or None, request.FILES or None, instance=instance)
    if form.is_valid():
        instance = form.save(commit=False)
        instance.save()
        messages.success(request, 'Post updated Successfully')
        return HttpResponseRedirect(instance.get_absolute_url())

    context = {
        "title": instance.title,
        "instance": instance,
        "form":form,
    }
    return render(request, "posts/post_form.html", context)


@login_required
def post_delete(request, slug=None):
    instance = get_object_or_404(BlogPost, slug=slug, owner=request.user)
    instance.delete()
    messages.success(request, "Successfully deleted")
    return redirect("posts:list")


def contact_us(request):
    form = ContactusForm(request.POST or None)
    if form.is_valid():
        form_email = form.cleaned_data.get("email")
        form_message = form.cleaned_data.get("message")
        form_full_name = form.cleaned_data.get("full_name")
        subject = 'Blog contact form'
        from_email = settings.EMAIL_HOST_USER
        to_email = [from_email]
        contact_message = "%s/%s via %s"%(
                form_full_name,
                form_message,
                form_email)
        # some_html_message = """
        # <h1>hello</h1>
        # """
        send_mail(subject,
                contact_message,
                from_email,
                to_email,
                # html_message=some_html_message,
                fail_silently=False)
    context = {
        "form": form,
    }

    return render(request, 'contact_us.html', context)


