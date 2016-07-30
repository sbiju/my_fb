from django.contrib.auth import get_user_model
from django.contrib.auth.decorators import login_required
from django.forms.models import modelformset_factory
from django.http import Http404
from django.shortcuts import render, get_object_or_404, redirect
from django.views.generic import ListView, DetailView, UpdateView, DeleteView, CreateView, TemplateView
from django.core.urlresolvers import reverse_lazy

User = get_user_model()

from .forms import  UserProfileForm
from .models import UserProfile
from blog_main.mixins import StaffRequiredMixin, LoginRequiredMixin

from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect


@login_required
def account_redirect(request):
    return redirect('profiles:user_detail', pk=request.user.pk)


class HomePageView(TemplateView):
    template_name = "home.html"


class UserListView(ListView):
    model = UserProfile


class UserDetailView(LoginRequiredMixin, DetailView):
    model = UserProfile

    def get_context_data(self, **kwargs):
        context = super(UserDetailView, self).get_context_data(**kwargs)

        return context


class UserCreateView(LoginRequiredMixin, CreateView):
    model = UserProfile
    form_class = UserProfileForm

    def form_valid(self, form):
        new_user = form.save(commit=False)
        new_user.user = self.request.user
        new_user.save()
        return super(UserCreateView, self).form_valid(form)


class UserUpdateView(StaffRequiredMixin, UpdateView):
    model = UserProfile
    form_class = UserProfileForm


class UserDeleteView(LoginRequiredMixin, DeleteView):
    model = UserProfile
    success_url = reverse_lazy('member_list')
    template_name = 'profiles/confirm_delete.html'










