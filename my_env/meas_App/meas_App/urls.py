"""meas_App URL Configuration

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
from django.conf.urls import url
from meas import views
from rest_framework import routers
from rest_framework.urlpatterns import format_suffix_patterns
from rest_framework.authtoken.views import obtain_auth_token
from django.contrib.auth import views as auth_views
from django.urls import reverse_lazy
from django.conf.urls.static import static
from django.conf import settings

# Routers provide an easy way of automatically determining the URL conf.
router = routers.DefaultRouter()

urlpatterns = [
    path('', views.index, name='index'),
    path('test/', views.test, name='test'),
    path('auftraege/neu/', views.neworderview, name='neworder'),
    path('login/', views.loginview, name="login"),
    path('logout/',views.logoutview, name='logout'),
    path('terminplaner/',views.scheduler, name='scheduler'),
    path('mitarbeiter/', views.employeesview, name= 'employees'),
    path('mitarbeiter/edit/', views.employeeeditview, name="employeeedit"),
    path('material/', views.productsview, name= 'products'),
    path('kunden/', views.customersview, name='customers'),
    path('admin/', admin.site.urls),
    path('api/auth/', include('rest_framework.urls')),
    path('api-token-auth/', obtain_auth_token, name='api_token_auth'),
    path('api/', include(router.urls)),
    path('api/v1/employeelist/', views.EmployeeList.as_view()),
    path('api/v1/employee/<pk>', views.Employee.as_view()),
    path('api/v1/employee/', views.Employee.as_view()),
    path('api/v1/customerlist/', views.CustomerList.as_view()),
    path('api/v1/productlist/', views.ProductList.as_view()),
    path('api/v1/product/<pk>', views.Product.as_view()),
    path('api/v1/product/', views.Product.as_view()),

    #Password Reset
    path(
        'password-reset/',
        auth_views.PasswordResetView.as_view(
            template_name='meas/registration/password_reset_form.html',
            subject_template_name='meas/registration/password_reset_subject.txt',
            email_template_name='meas/registration/password_reset_email.html',
            success_url='done/'
        ),
        name='password_reset'
    ),
    path(
        'password-reset/done/',
        auth_views.PasswordResetDoneView.as_view(
            template_name='meas/registration/password_reset_done.html',
        ),
        name='password_reset_done'
    ),
    path(
        'password-reset-confirm/<uidb64>/<token>/',
        auth_views.PasswordResetConfirmView.as_view(
            template_name='meas/registration/password_reset_confirm.html',
            success_url=reverse_lazy('password_reset_complete')
        ),
        name='password_reset_confirm'
    ),
    path(
        'reset-done/',
        auth_views.PasswordResetCompleteView.as_view(
            template_name="meas/registration/password_reset_complete.html"
        ),
        name='password_reset_complete'
    )

]+ static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
