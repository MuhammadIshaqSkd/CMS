from django.shortcuts import redirect, render
from django.contrib.auth import authenticate
from django.contrib import messages

from django.views import View
from django.contrib.auth import login

from dashboard.helper import update_inspect_item
from dashboard.models import Item
from datetime import datetime

# Create your views here.

class Home(View):
    @staticmethod
    def get(request):
        update_inspect_item()
        # Query for inspected and overdue items (you may have a field to define inspected/overdue)
        inspected_items = Item.objects.filter(checklist='Available')  # assuming 'status' field
        overdue_items = Item.objects.filter(checklist='Not Applicable')  # assuming 'status' field

        # Recent Activity Log (you may have an inspection log model)
        recent_activity = Item.objects.filter(modified__gte=datetime.now().replace(day=1))  # Inspected this month

        # Inspection Status Overview
        total_items = Item.objects.count()
        checked_items = inspected_items.count()
        pending_items = overdue_items.count()

        context = {
            'inspected_items': inspected_items,
            'overdue_items': overdue_items,
            'recent_activity': recent_activity,
            'total_items': total_items,
            'checked_items': checked_items,
            'pending_items': pending_items,
        }
        return render(request, "home.html", context)

class Login(View):
    @staticmethod
    def get(request):
        update_inspect_item()
        return render(request, "login.html")

    def post(self,request):
        Data = request.POST
        email = Data.get("email")
        Password = Data.get("password")
        user = authenticate(email=email, password=Password)

        if user:
            login(request, user)
            if user.user_role == 'Admin':
                return redirect("/dashboard")
            else:
                return redirect("dashboard/userdasboard")
        else:
            messages.error(request, "Invalid username or password.")
            return redirect("/login")
