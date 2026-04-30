from django.urls import path
from django.conf import settings
from django.conf.urls.static import static

from . import views 

from .views import PetListView, PetDetailView

app_name = 'pets'

urlpatterns = [

    path('', PetListView.as_view(), name='pet_list'),
    path('<int:pk>/', PetDetailView.as_view(), name='pet_detail'),
    path('login/', views.login_view, name='login'),

    path('add/', views.add_pet, name='add_pet'),
]


if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)