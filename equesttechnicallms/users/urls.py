from django.urls import path
from equesttechnicallms.users import views
from equesttechnicallms.users.views import (
    user_detail_view,
    user_redirect_view,
    user_update_view,

)

app_name = "users"
urlpatterns = [
    path('login/', views.loginPage, name="login"),
    path('logout/', views.logoutUser, name="logout"),
    path('register/', views.registerPage, name="register"),

    path("~redirect/", view=user_redirect_view, name="redirect"),
    path("~update/", view=user_update_view, name="update"),
    path("<str:username>/", view=user_detail_view, name="detail"),
]
