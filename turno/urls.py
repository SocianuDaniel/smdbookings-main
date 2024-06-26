from django.urls import path, include
from . import views
app_name='turno'
urlpatterns = [
    # path('update/<int:pk>/', views.UpdateOrari.as_view(), name='update'),
    # path('delete/<int:pk>/', views.DeleteOrario.as_view(), name='delete'),
    # path('<slug:slug>/', views.CreateOrarioView.as_view(), name="add_orario"),
    # path('<slug:slug>/dash/', views.ListOrariForEdit.as_view(), name="dash_orario"),
    path('<slug:slug>/', views.CreateTurnoView.as_view(), name="add_turno"),
    path('dash/<slug:slug>/', views.ListTurni.as_view(), name="dash_turno"),
    path('dash/<slug:slug>/<str:data>/', views.ListTurni.as_view(), name="list-by-date"),


]
