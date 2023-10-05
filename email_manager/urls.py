from django.urls import path

from .apps import EmailManagerConfig
from .views import (MailingListView,
                    MailingCreateView,
                    MailingUpdateView,
                    MailingDeleteView)

app_name = EmailManagerConfig.name

urlpatterns = [
    path('list/', MailingListView.as_view(), name='list'),
    path('create/', MailingCreateView.as_view(), name='create'),
    path('update/<int:pk>/', MailingUpdateView.as_view(), name='update'),
    path('delete/<int:pk>/', MailingDeleteView.as_view(), name='delete'),
]