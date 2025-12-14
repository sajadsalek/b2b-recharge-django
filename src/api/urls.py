from django.urls import path, include


urlpatterns = [
    path("appname/", include(("src.app.url", "appname")))
]