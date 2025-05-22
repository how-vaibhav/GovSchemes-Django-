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
      path('feedbacks/respond/<int:feedback_id>/', views.reply_feedback, name="reply_feedback")
]
