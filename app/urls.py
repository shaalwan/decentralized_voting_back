from django.urls import path
from .views import * 

urlpatterns = [
  #voter 
  path('voter/register',voterRegister.as_view()),
  path('voter/authenticate', voterAuthenticate.as_view()),
  path('voters/', voterList.as_view({'get':'list'})),
  path('voter/<int:pk>', voter.as_view()),

#company
  path('company/register',companyRegister.as_view()),
  path('company/authenticate', companyAuthenticate.as_view()),

#candidate
#  path('candidate/register',candidateRegister.as_view()),
]