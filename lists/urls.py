from django.urls import path

from .views import (ListListView,
                    ListCreateView,
                    ListDeleteView,
                    ListUpdateView,
                    BulletDeleteView)

urlpatterns = [
    path('', ListListView.as_view(), name='list_list'),
    path('create', ListCreateView.as_view(), name='list_create'),
    path('<int:pk>', ListUpdateView.as_view(), name='list_edit'),
    path('<int:pk>/delete', ListDeleteView.as_view(), name='list_delete'),
    path('bullet/<int:pk>/delete', BulletDeleteView.as_view(), name='bullet_delete'),
]