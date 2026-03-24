# Uncomment the imports before you add the code
from django.conf.urls.static import static
from django.conf import settings
from django.urls import path
from . import views
# from .models import CarMake, CarModel

app_name = 'djangoapp'

urlpatterns = [
    # # path for registration
    path('register', views.register_user, name='register'),

    # path for login / logout
    path('login', views.login_user, name='login'),
    path('logout', views.logout_request, name='logout'),

    # path for dealer reviews view
    path(
        route='reviews/dealer/<int:dealer_id>',
        view=views.get_dealer_reviews,
        name='dealer_details'
        ),
        
    # path to get cars
    path('get_cars/', views.get_cars, name='getcars'),

    # path to get dealers
    path(
        route='get_dealers',
        view=views.get_dealerships,
        name='get_dealers'
    ),
    path(
        route='get_dealers/<str:state>',
        view=views.get_dealerships,
        name='get_dealers_by_state'
    ),

    # path to get dealer details
    path(
        route='dealer/<int:dealer_id>',
        view=views.get_dealer_details,
        name='dealer_details'
    ),

    path(route='add_review', view=views.add_review, name='add_review'),

] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
