from django.urls import path, include

from src.financial.apis.refill import RefillApi

urlpatterns = [
    # path("appname/", include(("src.app.url", "appname"))
    path('auth/', include(('src.authentication.urls', 'auth'))),
    path('users/', include(('src.users.urls', 'users'))),
    path('financial/', include(('src.financial.urls', 'financial'))),

]