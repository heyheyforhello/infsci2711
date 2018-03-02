from django.conf.urls import url

from . import views

urlpatterns = [
    url(r'^search/$', views.search, name='search'),
    url(r'^category/$', views.CategoryView.as_view(), name='category'),
    url(r'^category/(?P<category_slug>[-\w\d]+)/$', views.CategoryDetailView, name='category_index'),
    # url(r'^category/(?P<category_slug>[-\w\d]+)/$', views.ProductsListView, name='category'),
    url(r'^(?P<slug>[-\w\d]+)/$', views.ProductDetailView.as_view(), name='detail'),
    url(r'^$', views.ProductsListView.as_view(), name='index'),
    url(r'^hot$', views.HotProductView.as_view(), name='hot_product'),
]
