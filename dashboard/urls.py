from django.urls import path
from django.contrib.auth import views as auth_views

from dashboard.views import (
    Dashboard,
    EditUserView,
    DeleteUserView,
    AddUserView,
    UserDasboard,
    ItemListView,
    AddItemView,
    EditItemView,
    DeleteItemView,
    inspect_item

)

urlpatterns = [
    path("", Dashboard.as_view(), name='dashboard'),  # Add the name here
    path('edit-user/<int:user_id>/', EditUserView.as_view(), name='edit_user'),
    path('delete-user/<int:user_id>/', DeleteUserView.as_view(), name='delete_user'),
    path('add-user/', AddUserView.as_view(), name='add_user'),
    path('userdasboard/', UserDasboard.as_view(), name='userdasboard'),
    path('logout/', auth_views.LogoutView.as_view(next_page='/login'), name='logout'),  # Update this line
    path('items/', ItemListView.as_view(), name='item_list'),
    path('items/add/', AddItemView.as_view(), name='add_item'),
    path('items/edit/<int:item_id>/', EditItemView.as_view(), name='edit_item'),
    path('items/delete/<int:item_id>/', DeleteItemView.as_view(), name='delete_item'),


]
