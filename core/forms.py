from django import forms
from django.contrib.auth.forms import UserChangeForm as BaseUserChangeForm
from django.contrib.auth.forms import UserCreationForm as BaseCreationForm
from django.core.validators import ValidationError
from localflavor.it import forms as it_forms
from django.utils.translation import gettext_lazy as _
import core.models
from .utils import send__activation_mail
from datetime import timedelta
from django.db.models import Q
from . import models
class UserCreationForm(BaseCreationForm):
    class Meta:
        model = models.User
        fields = (
            'name', 'email',
            'password1', 'password2',
        )

    def save(self, commit=True):
        user = super().save(commit=False)
        if commit:
            user.save()
        if not user.is_active:
            send__activation_mail(user)
        return user


class UserChangeForm(BaseUserChangeForm):
    class Meta:
        model = models.User
        fields = ('name',)


class LocationForm(forms.ModelForm):
    zip_code = it_forms.ITZipCodeField()

    class Meta:
        model = core.models.Location
        exclude = ('created', 'updated', 'user', 'slug')
        widgets = {
            'region': it_forms.ITRegionSelect,
            'province': it_forms.ITProvinceSelect,
        }

    def __init__(self, *args, **kwargs):
        self.request = kwargs.pop("request")
        super().__init__(*args, **kwargs)


    def clean(self):
        cleaned_data = super().clean()
        if core.models.Location.objects.filter(user=self.request.user).count() >= self.request.user.locations:
            raise ValidationError('%s has already a location' % self.request.user)
        return cleaned_data


class OrariForm(forms.ModelForm):
    class Meta:
        model = core.models.Orari
        fields = ('location', 'weekday', 'start', 'fine')
        widgets = {
            'weekday': forms.Select(attrs={'class': 'form-select'}),
            'user': forms.HiddenInput(),
            'start': forms.TimeInput(attrs={'type': 'time', 'class': 'form-select'}),
            'fine': forms.TimeInput(attrs={'type': 'time', 'class': 'form-select'})
        }
    def __init__(self, *args, **kwargs):
        self.request = kwargs.pop("request")
        super().__init__(*args, **kwargs)
        self.fields['location'].queryset = core.models.Location.objects.all().filter(user=self.request.user)
    def  clean(self):
        clean_data = super().clean()

        orar = core.models.Orari(
            location=clean_data.get('location'),
            weekday=clean_data.get('weekday'),
            start=clean_data.get('start'),
            fine=clean_data.get('fine')
        )
        allByDay = core.models.Orari.objects.all().filter(weekday=orar.weekday, location=orar.location)
        if allByDay:
            for hour in allByDay:
                start = hour.get_start_to_timedelta()
                fine = hour.get_fine_to_timedelta()
                if start < orar.get_start_to_timedelta() < fine:
                    raise ValidationError(
                        _('esiste gia un orario %s con che contiene questa ora %s' % (hour, start))
                    )
                if start > orar.get_start_to_timedelta() > fine:
                    raise ValidationError(
                        _('esiste gia un orario %s con che contiene questo  orario provi a mofificarlo ' % hour)
                    )
                if start < orar.get_fine_to_timedelta() <= fine:
                    raise ValidationError(
                        _('esiste gia un orario %s con che contiene questo  orario provi a mofificarlo ' % hour)
                    )
                if orar.get_start_to_timedelta() <= start and orar.get_fine_to_timedelta() >= fine:
                    raise ValidationError(
                        _('esiste gia un orario %s con che contiene questo  orario provi a mofificarlo ' % hour)
                    )
        return clean_data

class TurnoForm(forms.ModelForm):
    class Meta:
        model = models.Turno
        fields = ('location','dip', 'giorno', 'inizio', 'fine')

    def __init__(self, *args, **kwargs):
        self.request = kwargs.pop("request")
        super().__init__(*args, **kwargs)
        self.fields['location'].queryset = core.models.Location.objects.all().filter(user=self.request.user)
    def clean_fine(self):
        giorno = self.cleaned_data.get('giorno')
        fine = self.cleaned_data.get('fine')
        inizio = self.cleaned_data.get('inizio')
        if fine.date() < giorno:
            raise forms.ValidationError('la fine deve essere piu grande di %s' % giorno)
        if fine <= inizio:
            raise forms.ValidationError('la fine deve essere pi grande di %s ' % inizio)
        return fine

    def clean_inizio(self):

        inizio = self.cleaned_data.get('inizio')
        giorno = self.cleaned_data.get('giorno')

        if inizio.date() < giorno:
            raise forms.ValidationError('%s deve essere piu grande di %s' % (inizio, giorno))

        return inizio


    def clean(self):
        clean_data = self.cleaned_data
        giorno=clean_data.get('giorno')
        inizio=clean_data.get('inizio')
        fine=clean_data.get('fine')
        dip = clean_data.get('dip')
        """ controlla se esiste gia un turno con le stese ore """
        turni  = models.Turno.objects.all().filter(dip=dip, giorno=giorno
        ).exclude(id=self.instance.pk)
        if turni:
            for turno in turni:
                if inizio >= turno.inizio and inizio < turno.fine:
                    raise forms.ValidationError('esiste gia un turno [%s %s] che contiene %s' % (turno.inizio.strftime("%H:%M"),turno.fine.strftime("%H:%M"),inizio.strftime("%H:%M")))
                if fine > turno.inizio and fine <= turno.fine:
                    raise forms.ValidationError('esiste gia un turno [%s %s] che contiene %s' % (turno.inizio.strftime("%H:%M"),turno.fine.strftime("%H:%M"),fine.strftime("%H:%M")))

        """---------fine-----------"""

        """ check se tra l'ultimo turno passano 11 o 35 ore """
        ieri = giorno - timedelta(days=1)
        laltroieri = ieri - timedelta(days=1)
        turno_ieri_q = models.Turno.objects.filter(giorno=ieri, dip=dip).order_by('-fine')
        if turno_ieri_q:
            turno_ieri = turno_ieri_q[0]
            minimo =timedelta(hours=11)
            if inizio - turno_ieri.fine < minimo:
                raise forms.ValidationError('non passano le 11 ore con il turno %s' % turno_ieri)
        else:
            turno_ieri_q = models.Turno.objects.filter(giorno=laltroieri, dip=dip).order_by('-fine')
            if turno_ieri_q:
                turno_ieri = turno_ieri_q[0]
                minimo = timedelta(hours=35)
                if inizio - turno_ieri.fine < minimo:
                    raise forms.ValidationError('non passano le 35 ore con il turno %s' % turno_ieri)
        """---------fine-----------"""

        """check se tra la fine del turno e l'inizio del prossimo passano 11 o 35 ore """
        domani = giorno + timedelta(days=1)
        turno_domani_q = models.Turno.objects.filter(giorno=domani, dip=dip).order_by('inizio')
        if turno_domani_q:
            turno_domani = turno_domani_q[0]
            minimo = timedelta(hours=11)
            if turno_domani.inizio - fine < minimo:
                raise forms.ValidationError('non passano le 11 ore con il turno %s' % turno_domani)
        else:
            dopodomani = domani + timedelta(days=1)
            turno_dopodomani_q = models.Turno.objects.filter(giorno=dopodomani, dip=dip).order_by('inizio')
            if turno_dopodomani_q:
                turno_dopodomani = turno_dopodomani_q[0]
                minimo = timedelta(hours=35)
                if turno_dopodomani.inizio - fine < minimo:
                    raise forms.ValidationError('non passano le 35 ore con il turno %s' % turno_dopodomani)

        return clean_data