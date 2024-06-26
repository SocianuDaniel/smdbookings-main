from django.urls import path, include

from . import views

app_name = 'location'
urlpatterns = [

    path('add/', views.AddLocationView.as_view(), name='add'),
    path('edit/<slug:slug>/', views.UpdateLocation.as_view(), name='edit'),
    path('delete/<slug:slug>/', views.DeleteLocation.as_view(), name='delete'),

]