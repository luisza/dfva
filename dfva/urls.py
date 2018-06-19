"""dfva URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.11/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf.urls import url, include
from django.contrib import admin
from rest_framework import routers
from django.conf import settings
from institution.urls import get_routes_view as instition_get_routes_view
from person.urls import get_routes_view as person_get_routes_view
from institution.urls import urlpatterns as institution_urls
from django.contrib.auth.views import LoginView, LogoutView
from django.urls.base import reverse_lazy
from corebase.views import home

router = routers.DefaultRouter()
instition_get_routes_view(router)
person_get_routes_view(router)


urlpatterns = [
    url(r'^$', home, name="home"),
    url(r'^accounts/login/$', LoginView.as_view(),
        {'redirect_to': reverse_lazy("institution_list")}, name='login'),
    url(r'^logout/$', LogoutView.as_view(next_page=reverse_lazy('home')),
        name='logout'),
    url(r'^admin/', admin.site.urls),
    #     url(r'^api-auth/', include('rest_framework.urls',
    #                                namespace='rest_framework')),
    url(r'^', include('corebase.urls')),
    url(r'^', include(router.urls)),
] + institution_urls

if settings.DOCKER:
    from django.conf.urls.static import static
    urlpatterns += static(settings.STATIC_URL,
                          document_root=settings.STATIC_ROOT)
    urlpatterns += static(settings.MEDIA_URL,
                          document_root=settings.MEDIA_ROOT)
