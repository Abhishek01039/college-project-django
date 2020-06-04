"""bookSharingBackend URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from django.conf.urls.static import static
from django.conf import settings
from .views import Index
from rest_framework.authtoken import views
from graphene_django.views import GraphQLView

# from rest_framework_simplejwt.views import (
#     TokenObtainPairView,
#     TokenRefreshView,
# )
urlpatterns = [
    path('admin/', admin.site.urls),
    path('', Index, name="index"),
    path('graphql/', GraphQLView.as_view(graphiql=True)),

    # path('api/token/', TokenObtainPairView.as_view(),
    #      name='token_obtain_pair'),  # post
    # path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('booksharing/', include('booksharingapi.urls')),
    path('api_token_auth/', views.obtain_auth_token)

] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT) + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
