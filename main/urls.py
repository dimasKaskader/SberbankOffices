from django.conf.urls import url
from . import views


urlpatterns = [
    url(r'^$', views.main_view, name='main_view'),  # главная
    url(r'^branch$', views.branch, name='branch'),
    url(r'^candidates$', views.candidates, name='candidates'),
    url(r'^deleted_branch$', views.deleted_branch, name='deleted_branch'),
]