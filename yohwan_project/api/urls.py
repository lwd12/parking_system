from django.urls import include, path
from rest_framework import routers
from . import views  # views.py import
from django.contrib import admin

router = routers.DefaultRouter()  # DefaultRouter를 설정
#router.register('residents_information', views.residents_informationViewSet)
#router.register('residents_information', views.residents_informationViewSet)
#router.register('insidetheparkinglot', views.insidetheparkinglotViewSet)
#router.register('parkinglot', views.parkinglotViewSet)
#router.register('entrancetotheparkinglot', views.entrancetotheparkinglotViewSet)
router.register('unauthorized_parkinglot', views.unauthorized_parkinglotViewSet)
#router.register('visitor_information', views.visitor_informationViewSet)
router.register('safetyaccident', views.safetyaccidentViewSet)
#router.register('loginforAdministrator', views.loginforAdministratorViewSet)
#router.register('loginforClient', views.loginforClientViewSet)
router.register('question', views.questionViewSet)
router.register('answer', views.answerViewSet)

urlpatterns = [
    path('', include(router.urls)),
    path('', include(router.urls)),
    path('residents_information/', views.residents_informationAPIView.as_view(), name='residents_information'),
    path('residents_information/<int:residents_number>', views.residents_informationdetailAPIView.as_view(),
         name='residents_information'),
    path('insidetheparkinglot/', views.insidetheparkinglotAPIView.as_view(), name='insidetheparkinglot'),
    path('insidetheparkinglot/<int:parking_seatnumber>', views.insidetheparkinglotdetailAPIView.as_view(),
         name='insidetheparkinglot'),
    path('parkinglot/', views.parkinglotAPIView.as_view(), name='parkinglot'),
    # path('parkinglot/<int:residents_choice_seatnumber>', views.parkinglotdetailAPIView.as_view(), name='parkinglot'),
    path('entrancetotheparkinglot/', views.entrancetotheparkinglotAPIView.as_view(), name='entrancetotheparkinglot'),
    path('entrancetotheparkinglot/<int:parking_log_number>', views.entrancetotheparkinglotdetailAPIView.as_view(),
         name='entrancetotheparkinglot'),
    path('unauthorized_parking/', views.unauthorized_parkingAPIView.as_view(), name='unauthorized_parking'),
    path('unauthorized_parking/<int:parking_log_number>', views.unauthorized_parkingdetailAPIView.as_view(),
         name='unauthorized_parking'),
    path('visitor_information/', views.visitor_informationAPIView.as_view(), name='visitor_information'),
    path('visitor_information/<int:visitor_information_number>', views.visitor_informationdetailAPIView.as_view(),
         name='visitor_information'),
    path('safetyaccident/', views.safetyaccidentAPIView.as_view(), name='safetyaccident'),
    path('safetyaccident/<int:safetyaccident_number>', views.safetyaccidentdetailAPIView.as_view(),
         name='safetyaccident'),
    path('loginforAdministrator/', views.loginforAdministratorAPIView.as_view(), name='loginforAdministrator'),
    path('loginforAdministrator/<int:loginforAdministrator_number>', views.loginforAdministratordetailAPIView.as_view(),
         name='loginforAdministrator'),
    # path('loginforClient/', views.loginforClientAPIView.as_view(), name='loginforClient'),
    path('loginforClient/<int:loginforClient_number>', views.loginforClientdetailAPIView.as_view(),
         name='loginforClient'),
    path('question/', views.questionAPIView.as_view(), name='question'),
    path('question/<int:question_number>', views.questiondetailAPIView.as_view(), name='question'),
    path('answer/', views.answerAPIView.as_view(), name='answer'),
    path('answer/<int:answer_number>', views.answerdetailAPIView.as_view(), name='answer'),
    path('RegistUser/', views.RegistUser.as_view(), name='RegistUser'),
    path('loginforClient/', views.Clientlogin.as_view(), name='loginforClient'),
    path('ClientData/', views.ClientData.as_view(), name='ClientData'),
    path('SessionData/', views.loginAPIView.as_view(), name='SessionData'),
]
