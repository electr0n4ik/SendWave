from django.urls import path
from django.views.decorators.cache import cache_page

from .apps import MainConfig
from .views import (
    ClientListView,
    ClientCreateView,
    ClientUpdateView,
    ClientDeleteView
)

from email_manager.views import MailingListView

app_name = MainConfig.name

urlpatterns = [
    path('', cache_page(60)(MailingListView.as_view()), name='home'),  # 2. кеширование главной страницы
    path('list/', ClientListView.as_view(), name='list'),
    path('create/', ClientCreateView.as_view(), name='create'),
    path('update/<int:pk>', ClientUpdateView.as_view(), name='update'),
    path('delete/<int:pk>/', ClientDeleteView.as_view(), name='delete'),
]
