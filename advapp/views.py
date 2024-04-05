from django.http import HttpResponse
from django.shortcuts import render, get_object_or_404, redirect

# Create your views here.
from django.urls import reverse_lazy, reverse
from django.views import View
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView, TemplateView
from django.contrib.auth.mixins import LoginRequiredMixin

from .forms import AdvertForm, RespondForm
from .models import Advert, Respond, Category


class AdvertList(ListView):
    model = Advert
    ordering = '-date_creation'
    template_name = 'home.html'
    context_object_name = 'advert_list'
    paginate_by = 5
    extra_context = {'adverts': Advert.objects.all()}

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        page = context['page_obj']
        context['all_categories'] = Category.objects.all()
        context['paginator_range'] = page.paginator.get_elided_page_range(
            page.number, on_each_side=1, on_ends=1)
        return context


class AdvertDetail(DetailView):
    model = Advert
    template_name = 'advert.html'
    context_object_name = 'advert'

    def get_context_data(self, **kwargs):
        """Get correct html-title"""
        context = super().get_context_data(**kwargs)
        adv_author = Advert.objects.get(id=self.request.path.split('/')[-1]).user_id
        context['is_author'] = self.request.user == adv_author
        return context


class AdvertCategoryList(ListView):
    model = Advert
    context_object_name = 'advert_cat_list'
    paginate_by = 5
    template_name = 'categories.html'

    def get_queryset(self):
        self.category = get_object_or_404(Category, id=self.kwargs['pk'])
        queryset = Advert.objects.filter(category=self.category).order_by('-date_creation')
        return queryset

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        page = context['page_obj']
        context['all_categories'] = Category.objects.all()
        context['category'] = self.category
        context['paginator_range'] = page.paginator.get_elided_page_range(
            page.number, on_each_side=1, on_ends=1)
        return context


class ProfileView(LoginRequiredMixin, TemplateView):
    template_name = 'profile.html'
    success_url = reverse_lazy('home')


class AdvertCreate(LoginRequiredMixin, CreateView):
    form_class = AdvertForm
    model = Advert
    template_name = 'create_or_edit.html'

    def get_context_data(self, **kwargs):
        """Get correct html-title"""
        context = super().get_context_data(**kwargs)
        context['get_title'] = "Create"
        return context

    def form_valid(self, form):
        """Get author = user"""
        advert = form.save(commit=False)
        advert.user_id = self.request.user
        return super().form_valid(form)


class AdvertEdit(LoginRequiredMixin, UpdateView):
    form_class = AdvertForm
    model = Advert
    template_name = 'create_or_edit.html'

    def get_context_data(self, **kwargs):
        """Get correct html-title"""
        context = super().get_context_data(**kwargs)
        context['get_title'] = "Edit"
        return context


class AdvertDelete(LoginRequiredMixin, DeleteView):
    model = Advert
    template_name = 'delete.html'
    success_url = '/home/'


class CreateRespond(LoginRequiredMixin, CreateView):
    form_class = RespondForm
    model = Respond
    template_name = 'advert.html'
