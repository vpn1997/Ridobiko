
from django.conf.urls import url,include
from django.contrib import admin
from log.views import get_login,logout_view,register_view
from cart.views import search_page,index_page,cart_page,fil_page,buy_page,add_page,rate_page,history_page,detail_page,dis_page

urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'^login/',get_login),
    url(r'^logout/',logout_view),
    url(r'^register/',register_view),
    url(r'history/',history_page),
    url(r'^index',index_page),
    url(r'^accounts/', include('allauth.urls')),
    url(r'^cart/',cart_page),
    url(r'^fil',fil_page),
    url(r'^buy/',buy_page),
    url(r'rate/',rate_page),
    url(r'^add/',add_page),
    url(r'^detail/',detail_page),
    url(r'^dis/',dis_page)
]
