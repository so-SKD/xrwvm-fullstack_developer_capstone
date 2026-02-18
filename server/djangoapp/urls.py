# Uncomment the imports before you add the code
from django.conf.urls.static import static
from django.conf import settings
from django.urls import path
from . import views

app_name = 'djangoapp'
urlpatterns = [
    # # path for registration
    path('register', views.register_user, name='register'),

    # path for login / logout
    path('login', views.login_user, name='login'),
    path('logout', views.logout_request, name='logout'),  

    # path for dealer reviews view

    # path for add a review view

] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
