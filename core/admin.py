from django.contrib import admin
from django.contrib.auth import get_user_model
from django.contrib.auth.models import Group
from django.shortcuts import get_object_or_404

import core.models
from . import forms
from . import utils
# Register your models here.
from .models import User


@admin.action(description="send user activation link")
def sent_user_activation_link(modeladmin, request, queryset):
    for obj in queryset:
        user = get_object_or_404(get_user_model(), pk=obj.pk)
        if not user.is_active:
            utils.send__activation_mail(user)


@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = ('email', 'name', 'locations', 'is_active', 'is_staff')
    actions = [sent_user_activation_link]
    form = forms.UserCreationForm




@admin.register(core.models.Orari)
class OrariAdmin(admin.ModelAdmin):
    list_display = ('weekday','start','fine','durata_apertura')
    sortable_by = ('weekday','start')
    ordering = ('weekday','start')
    list_filter = ('weekday',)

@admin.register(core.models.Location)
class AdminLocation(admin.ModelAdmin):
    prepopulated_fields = {
        'slug': ('name',)
    }
    readonly_fields = ('user',)
from . import models, forms

@admin.register(models.SMDManager)
class AdminSMDManager(admin.ModelAdmin):
    list_display = ( 'cognome', 'nome', 'ore')

@admin.register(models.Turno)
class AdminTurno(admin.ModelAdmin):
    list_display = ('dip','giorno', 'inizio', 'fine', 'durata')
    ordering = ('-giorno',)
    form = forms.TurnoForm


admin.site.unregister(Group)