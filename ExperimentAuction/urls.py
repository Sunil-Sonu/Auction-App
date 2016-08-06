"""MyApp URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.9/topics/http/urls/
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
from django.contrib.staticfiles.urls import staticfiles_urlpatterns
from django.contrib.staticfiles.urls import static

from ssapp import views, classviews
from django.conf import settings

urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'register/', views.register, name='register'),  #REGISTRATION PAGE
    url(r'login/', views.user_login, name='login'),        #LOGIN PAGE
    url(r'logout/$', views.user_logout, name='logout'),     #LOG OUT PAGE
    url(r'^$', views.index, name='index'),              #HOME PAGE OR MAIN PAGE
    url(r'homepage/$',views.homepage,name='Homepage'),    # HOME PAGE
    url(r'homepage/sellerdetails/$',views.selleritems,name='sellerdetails'),   #
    url(r'homepage/mybid/$', views.MyBids, name='mybid'),  #
    url(r'homepage/update/(?P<pk>[0-9]+)/$',classviews.UpdateProductView.as_view(),name='product-update'),
    url(r'homepage/delete/(?P<pk>[0-9]+)/$', classviews.DeleteProductView.as_view(), name='product-delete'),
    url(r'homepage/create/$',classviews.CreateSellerView.as_view(),name='create'), #
    url(r'homepage/categories/$',classviews.CategoriesView.as_view(),name='categories'), #CATEGORY
    url(r'homepage/categories/products/(?P<pk>[0-9]+)/$',views.ProductsView,name='products'),     #PRODUCTS IN THAT CATEGORY
    url(r'homepage/categories/products/bid/(?P<pk>[0-9]+)/$', classviews.ProductsUpdateView.as_view(), name='bid'), #UPDATE THE BID
  #  url(r'homepage/categories/products/bid/(?P<pk>[0-9]+)/$',views.ProductsBuy,name='bid'),
    url(r'homepage/solddetails/(?P<pk>[0-9]+)/$',views.BuyerView,name='Buyer'),   # Display BUYER'S INFORMATION
    url(r'homepage/purchases/$',views.UserProducts,name='UserProducts') , # Displaying purchased ITEMS
    url(r'homepage/categories/products/biddetails/(?P<pk>[0-9]+)/$',views.ItemInfo,name='items'),
    url(r'homepage/createcategory/$',classviews.CategoriesDisplay.as_view(),name='create-cate'),
   #PROFILE
    url(r'homepage/profile/$',views.userprofile,name='Profile'),

    #THIS IS FOR RESET OF PASSWORD

    url(r'resetpassword/$','django.contrib.auth.views.password_reset',name='reset_password'),
    url(r'^resetpassword/passwordsent/$', 'django.contrib.auth.views.password_reset_done', name='password_reset_done'),
    url(r'^reset/(?P<uidb64>[0-9A-Za-z]+)-(?P<token>.+)/$', 'django.contrib.auth.views.password_reset_confirm',
        name='password_reset_confirm'),
    url(r'reset/done/$','django.contrib.auth.views.password_reset_complete',name='password_reset_complete'),
    #url(r'homepage/profile/$',classviews.UpdateUserProfile.as_view(),name='profile')
    url(r'homepage/search/$',views.searchitem,name='searchbox')
]

urlpatterns += staticfiles_urlpatterns()
urlpatterns+= static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)