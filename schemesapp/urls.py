from django.urls import path
from . import views

urlpatterns = [
     path('home/', views.home, name = "home"),
      path('feedback/', views.feedback, name = "feedback"),
      path('feedbacks/', views.view_feedback, name = "view_feedbacks"),
      path('login/', views.login_view, name = "login"),
      path('register/', views.register, name = "register"),
      path('logout/', views.logout_view, name = "logout"),
      path('addemployee/', views.add_employee, name= "add_employee"),
      path('feedbacks/respond/<int:feedback_id>/', views.reply_feedback, name="reply_feedback"),
      path("translate/", views.translate_page, name="translate_text"),
      path('schemes/', views.scheme_list, name='scheme_list'),
      path('scheme/<int:pk>/', views.scheme_detail, name='scheme_detail'),
      path('schemeadd/', views.scheme_input, name='add_scheme'),
      path('userdetails/', views.user_detail_input, name='user_detail'),
      path('eligibility/<int:pk>/', views.scheme_eligibility, name='user_eligibility'),
      path('check-eligibility/', views.check_all_eligibility, name='check_all_eligibility'),
      path('userdetails/view/', views.view_user_details, name='view_user_details'),
      path('userdetails/edit/', views.edit_user_details, name='edit_user_details'),
]

