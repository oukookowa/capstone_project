from django.urls import path
from .views import NotificationListView

urlpatterns = [
    path('', NotificationListView.as_view(), name='notification-list'), # Empty ('') because 'api/notifications/' is defined in main app
]