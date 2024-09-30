from django.urls import path
from .views import NotificationListView

urlpatterns = [
    path('notifications/', NotificationListView.as_view(), name='notification-list'), # Should be empty e.g '', View.as_view() to mount directly on tifications app
]