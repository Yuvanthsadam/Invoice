from django.urls import path
from .views import *
from . import views

urlpatterns = [
    path('productlist/',ProductView.as_view(),name= 'User List'),
    
    path('registeradmin/',AdminRegisterView.as_view(),name= 'Admin Will Register'),
    path('registeradmin/<int:pk>',AdminDetailView.as_view(),name= 'Admin Details'),
    
    path('login/', CustomLoginView.as_view(),name= 'login'),
    
    path('main/',MainView.as_view(),name= 'main title'),
    path('main/<int:pk>',MainDetailView.as_view(),name= 'Admin Details'),
    
    path('sub_title_one/', Sub_Title_One_View.as_view(),name='sub_title_one'),
    path('sub_title_one/<int:pk>', Sub_Title_One_DetailView.as_view(),name='sub_title_one_detail'),
    
    path('sub_title_two/', Sub_Title_Two_View.as_view(),name='sub_title_two'),
    path('sub_title_two/<int:pk>', Sub_Title_Two_DetailView.as_view(),name='sub_title_two_detail'),
    
    path('change_password/', ChangePasswordView.as_view(), name='change-password'),
    
    path('generatePDF/<int:id>/', views.generatePDF, name='generatePDF'),
    path('storePDF/', StoringPDFView.as_view(), name='storePDF'), 
     
    # path('generate_invoice/', InvoiceGenerator, name='generate_invoice'),       
    
    path('drafted/',DraftedView.as_view(),name= 'Draft List'),
    path('pending/',PendingView.as_view(),name= 'pending List'),
    path('completed/',CompletedView.as_view(),name= 'completed List'),
    
    
    path('User_logout/', User_logout), 
]