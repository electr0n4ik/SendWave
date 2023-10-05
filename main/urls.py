from django.urls import path

from .apps import MainConfig
from .views import (
    ClientListView,
    ClientCrateView,
    ClientUpdateView,
    ClientDeleteView
)

from email_manager.views import MailingListView

app_name = MainConfig.name

urlpatterns = [
    path('', MailingListView.as_view(), name='home'),
    path('list/', ClientListView.as_view(), name='list'),
    path('create/', ClientCrateView.as_view(), name='create'),
    path('update/<int:pk>', ClientUpdateView.as_view(), name='update'),
    path('delete/<int:pk>/', ClientDeleteView.as_view(), name='delete'),
]
