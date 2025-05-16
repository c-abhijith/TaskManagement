from django.urls import path

from taskmanager.views.usermanage_view import login_page,admin_panel,user_panel,create_user_view,custom_logout

urlpatterns = [
    path('login/', login_page, name='login_page'),
    path('adminpanel/', admin_panel, name='admin_panel'),
    path('userpanel/', user_panel, name='user_panel'),
    path("create/", create_user_view, name="create_user"),
    path('logout/', custom_logout, name='logout'),

]
