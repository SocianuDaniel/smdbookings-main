from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import HttpResponse
from django.urls import reverse_lazy
from django.utils.text import slugify
from django.views.generic import CreateView, UpdateView, DeleteView

import core.models
from core.views import PassRequestToFormViewMixin


# Create your views here.
class AddLocationView(LoginRequiredMixin, PassRequestToFormViewMixin, CreateView):
    template_name = 'location/add_location.html'
    model = core.models.Location
    success_url = reverse_lazy('base:list')
    form_class = core.forms.LocationForm

    def form_valid(self, form):
        my_user = self.request.user
        if not core.models.Location.objects.filter(user=my_user).count() >= my_user.locations:
            form.instance.user = my_user
            form.instance.slug = slugify(form.instance.name)
            return super().form_valid(form)
        else:
            return HttpResponse('nu se poate')
            # raise ValueError('%s has already a  locations' % my_user)


class UpdateLocation(LoginRequiredMixin, UpdateView):
    model = core.models.Location
    fields = (
        'description', 'image', 'country', 'region', 'province',
        'city', 'zip_code', 'street_name', 'street_number')
    template_name = 'location/edit_location.html'
    success_url = reverse_lazy('base:list')


class DeleteLocation(LoginRequiredMixin, DeleteView):
    template_name = 'location/delete_location.html'
    success_url = reverse_lazy('base:list')
    model = core.models.Location
