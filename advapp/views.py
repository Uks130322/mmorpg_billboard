from django.shortcuts import render, get_object_or_404

# Create your views here.
from django.views import View
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from django.contrib.auth.mixins import LoginRequiredMixin

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