from django.views import View
from django.views.generic import (ListView,
                                  CreateView,
                                  DeleteView)
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.shortcuts import render
from django.urls import reverse_lazy
from django.http import Http404
from django.core.exceptions import BadRequest

from .models import Bullet, List

class IsListOwnerMixin(UserPassesTestMixin):
    """
    Custom Mixin to check if the user is the owner of the List
    """

    permission_denied_message = 'Sorry, you are not the owner of this list.'

    def test_func(self, **kwargs):
        return self.get_object().author == self.request.user

class IsBulletOwnerMixin(UserPassesTestMixin):
    """
    Custom Mixin to check if the user is the owner of the Bullet
    """

    permission_denied_message = 'Sorry, you are not the owner of this bullet.'

    def test_func(self, **kwargs):
        return self.get_object().list.author == self.request.user


class ListListView(LoginRequiredMixin, ListView):
    model = List
    template_name = 'list_list.html'

class ListCreateView(LoginRequiredMixin, CreateView):
    template_name = 'list_create.html'
    model = List
    fields = ['title']

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)

class ListDeleteView(LoginRequiredMixin, IsListOwnerMixin, DeleteView):
    model = List
    template_name = 'list_delete.html'
    success_url = reverse_lazy('list_list')


class ListUpdateView(LoginRequiredMixin, IsListOwnerMixin, View):
    template_name = 'list_edit.html'
    main_model = List
    foreign_model = Bullet

    def get_object(self):
        """
        Get the main object for the given primary key.
        """
        try:
            return self.main_model.objects.get(pk=self.kwargs['pk'])
        except self.main_model.DoesNotExist:
            raise Http404("Object does not exist")

    def get(self, request, **kwargs):
        return render(request, self.template_name, {'list': self.get_object()})

    def post(self, request, **kwargs):
        """
        Handles a POST request to the view to either modify existing elements (bullets) of a list
        or add a new one to it.
        """
        to_do_list = self.get_object()

        if 'Save' in request.POST:
            for bullet in to_do_list.bullets.all():
                if f'bullet-{bullet.id}' in request.POST:
                    bullet.is_completed = True
                else:
                    bullet.is_completed = False
                bullet.title = request.POST.get(f"title-{bullet.id}")
                bullet.save()

        elif 'Add' in request.POST:
            to_do_list.bullets.create(
            title=request.POST.get('new_bullet_title'),
            is_completed=False,
            )
            to_do_list.save()

        else:
            raise BadRequest

        return render(request, self.template_name, {'list': to_do_list})


class BulletDeleteView(LoginRequiredMixin, IsBulletOwnerMixin, DeleteView):
    template_name = 'bullet_delete.html'
    model = Bullet
    
    def dispatch(self, request, *args, **kwargs):
        self.success_url = self.model.objects.get(pk=kwargs['pk']).get_absolute_url()
        return super().dispatch(request, *args, **kwargs)
