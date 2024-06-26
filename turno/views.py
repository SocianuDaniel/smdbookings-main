from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import  get_object_or_404, Http404, redirect
from django.urls import reverse_lazy

from django.views.generic import CreateView,ListView
import core.models
from core.views import PassRequestToFormViewMixin
import datetime
from core import models
from django.db.models import Q
from django.utils.translation import gettext_lazy as _

class CreateTurnoView(LoginRequiredMixin, PassRequestToFormViewMixin,CreateView):
    template_name = 'turno/add.html'
    success_url = reverse_lazy('orari:dash_orario')
    model = core.models.Turno
    form_class = core.forms.TurnoForm

    def get_initial(self):
        location = get_object_or_404(core.models.Location, slug=self.kwargs.get('slug'))
        return {'location': location}

    def get_success_url(self):
        return reverse_lazy('turno:dash_turno',args=[self.kwargs.get('slug')])

    def dispatch(self, request, *args, **kwargs):
        loc = get_object_or_404(core.models.Location, slug=self.kwargs.get('slug'))
        if loc.user == self.request.user:
            return super().dispatch(request, *args, **kwargs)
        return redirect(reverse_lazy('users:profile'))
        raise Http404


days = [
    (0, _("Monday")), (1, _("Tuesday")), (2, _("Wednesday")),
    (3, _("Thursday")), (4, _("Friday")), (5, _("Saturday")),
    (6, _("Sunday"))
]
class ListTurni(LoginRequiredMixin, PassRequestToFormViewMixin,ListView):
    model = models.Turno
    template_name = 'turno/dash.html'
    ordering = '-giorno'
    context_object_name = 'turni'
    date_field = 'giorno'
    def get_initial(self):
        location = get_object_or_404(core.models.Location, slug=self.kwargs.get('slug'))
        return {'location': location}
    def get_queryset(self):
        data = datetime.date.today()
        if 'data' in self.kwargs:
            try:
                data = datetime.datetime.strptime(self.kwargs['data'], "%Y-%m-%d")
            except (ValueError, TypeError):
                pass


        lunedi = data - datetime.timedelta(days=data.weekday() % 7)

        domenica = lunedi + datetime.timedelta(days=6)
        querry =models.Turno.objects.all().filter(Q(giorno__range=[lunedi,domenica])).order_by('giorno','inizio')
        orari = {}
        for numar, zi in days:
            orari[zi] = [i for i in querry if i.giorno.weekday() == numar]
        return orari

    def get_context_data(self, **kwargs):
        context = super(ListTurni, self).get_context_data(**kwargs)
        location = get_object_or_404(core.models.Location, slug=self.kwargs.get('slug'))

        context['location'] = location

        data = datetime.date.today()
        if 'data' in self.kwargs:
            try:
                data = datetime.datetime.strptime(self.kwargs['data'], "%Y-%m-%d")
            except (ValueError, TypeError):
                pass

        lunedi = data - datetime.timedelta(days=data.weekday() % 7)
        prossimo = lunedi + datetime.timedelta(days=7)
        anteriore = lunedi - datetime.timedelta(days=7)
        print(type(prossimo))
        print(anteriore)
        context['anteriore'] = anteriore.strftime("%Y-%m-%d")
        context['prossimo'] = prossimo.strftime("%Y-%m-%d")
        return context

