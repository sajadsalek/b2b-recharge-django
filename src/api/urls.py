from django.urls import path, include


urlpatterns = [
    # path("appname/", include(("src.app.url", "appname"))
    path('auth/', include(('src.authentication.urls', 'auth'))),
]