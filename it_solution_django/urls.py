from django.urls import include, path

urlpatterns = [
    path('', include('runtext_app.urls')),
    ]
