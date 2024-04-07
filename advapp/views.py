from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from django.shortcuts import render, get_object_or_404, redirect

# Create your views here.
from django.urls import reverse_lazy, reverse
from django.views import View
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView, TemplateView
from django.contrib.auth.mixins import LoginRequiredMixin

from .filters import RespondFilter
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
        """In the template will be different buttons depending on whether the user is the author.
        If user responded to this adv, he'll see the corresponding message"""
        context = super().get_context_data(**kwargs)
        adv_author = Advert.objects.get(id=self.request.path.split('/')[-1]).user_id
        context['is_author'] = self.request.user == adv_author
        responds_authors = Respond.objects.filter(advert_id=self.request.path.split('/')[-1]).values('user_id')
        context['responded'] = {'user_id': self.request.user.id} in responds_authors
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


class RespondCreate(LoginRequiredMixin, CreateView):
    form_class = RespondForm
    model = Respond
    template_name = 'respond.html'

    def get_context_data(self, **kwargs):
        """Get correct advert from url-path"""
        context = super().get_context_data(**kwargs)
        context['advert'] = Advert.objects.get(id=self.request.path.split('/')[-3])
        return context

    def form_valid(self, form):
        """Get author = user, get advert_id"""
        respond = form.save(commit=False)
        respond.user_id = self.request.user
        respond.advert_id = Advert.objects.get(id=self.request.path.split('/')[-3])
        return super().form_valid(form)


class RespondList(LoginRequiredMixin, ListView):
    model = Respond
    template_name = 'my_responds.html'
    context_object_name = 'responds'
    paginate_by = 10

    def get_queryset(self):
        queryset = Respond.objects.filter(advert_id__user_id=self.request.user).order_by('-date_creation')
        self.filterset = RespondFilter(self.request.GET, queryset, request=self.request.user)
        return self.filterset.qs

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        context['filterset'] = self.filterset
        page = context['page_obj']
        context['paginator_range'] = page.paginator.get_elided_page_range(
            page.number, on_each_side=1, on_ends=1)
        return context


class RespondDelete(LoginRequiredMixin, DeleteView):
    model = Respond
    template_name = 'respond_delete.html'
    success_url = reverse_lazy('my_responds')


@login_required
def accept_respond(request, pk):
    respond = Respond.objects.get(id=pk)
    respond.accepted = True
    respond.save()
    return redirect('my_responds')
