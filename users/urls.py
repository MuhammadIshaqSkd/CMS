from django.urls import path
from users.views import Home, Login
from dashboard.views import inspect_item, overdue_item
urlpatterns = [
    path('', Home.as_view()),
    path('login', Login.as_view()),
    path('inspect_item/', inspect_item, name='inspect_item'),  # For showing details of a specific item
    path('overdue_item/', overdue_item, name='overdue_item'),  # For showing details of a specific item

]