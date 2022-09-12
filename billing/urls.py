from django.urls import path, include
from billing.views import *
from rest_framework.authtoken.views import ObtainAuthToken

urlpatterns = [
    path('registeradmin/',AdminRegisterView.as_view(),name= 'Admin Will Register'),
    path('registeradmin/<int:pk>',AdminDetailView.as_view(),name= 'Admin Details'),
    
    path('main/',MainView.as_view(),name= 'main title'),
    path('main/<int:pk>',MainDetailView.as_view(),name= 'Admin Details'),
    
    path('sub_title_one/', Sub_Title_One_View.as_view(),name='sub_title_one'),
    path('sub_title_one/<int:pk>', Sub_Title_One_DetailView.as_view(),name='sub_title_one_detail'),
    
    path('sub_title_two/', Sub_Title_Two_View.as_view(),name='sub_title_two'),
    path('sub_title_two/<int:pk>', Sub_Title_Two_DetailView.as_view(),name='sub_title_two_detail'),
    
    # path('api/auth/login', SignInAPI.as_view()),
    # path('main/get',MainGetView.as_view(),name= 'main title'),
    # path('get_admin',AdminDetail.as_view(),name= 'get admin detail'),
    path('login/', CustomLoginView.as_view(),name= 'login'),
    # path('login/', customer_login),
    path('User_logout/', User_logout), # admin will logout  
    
    path('change_password/', ChangePasswordView.as_view(), name='change-password'),
    
]