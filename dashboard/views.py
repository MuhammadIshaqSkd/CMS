from django.shortcuts import render, get_object_or_404, redirect

from django.contrib.auth.mixins import LoginRequiredMixin
from django.views import View

from dashboard.helper import update_inspect_item
from users.models import User
# Create your views here.
from django import forms
from django.urls import reverse
from django.contrib import messages
from dashboard.models import Item




class Dashboard( LoginRequiredMixin,View):
    login_url = '/login'
    @staticmethod
    def get(request):
        update_inspect_item()
        if request.user.user_role == "Admin":
            all_user = User.objects.all()
            normal_user = all_user.count
            admin_user = all_user.filter(user_role="Admin").count
            all_item = Item.objects.all().count()
            context = {
                'user': request.user,
                'all_user': all_user,
                'normal_user': normal_user,
                'admin_user': admin_user,
                'all_item': all_item,
            }
            return render(request, 'dashboard.html', context)
        else:
            return redirect('/')


class UserDasboard(LoginRequiredMixin, View):
    login_url = "/login"
    @staticmethod
    def get(request):
        update_inspect_item()
        user = request.user
        items = Item.objects.all()
        return render(request, 'user_dashboard.html', {'items': items, 'user':user})

# Form to edit user role
class EditUserRoleForm(forms.ModelForm):
    class Meta:
        model = User
        update_inspect_item()
        fields = ['user_role']  # Assume user_role is a field in your User model

class EditUserView(View):
    def get(self, request, user_id):
        if request.user.user_role == "Admin":
            user = get_object_or_404(User, id=user_id)
            context = {
                'user': user,
            }
            return render(request, 'edit_user.html', context)
        else:
            return redirect('/')

    def post(self, request, user_id):
        if request.user.user_role == "Admin":
            user = get_object_or_404(User, id=user_id)
            new_role = request.POST.get('role')

            # Update user role
            if new_role:
                user.user_role = new_role  # Adjust this line if your user role field is different
                user.save()
                messages.success(request, 'User role updated successfully.')
            else:
                messages.error(request, 'Please select a valid role.')

            return redirect('dashboard')
        else:
            return redirect('/')

class DeleteUserView(LoginRequiredMixin, View):
    login_url = '/login'

    def get(self, request, user_id):
        update_inspect_item()
        if request.user.user_role == "Admin":
            user = get_object_or_404(User, id=user_id)
            user.delete()  # Delete the user from the database
            return redirect(reverse('dashboard'))
        else:
            return redirect('/')

class AddUserView(View):
    def get(self, request):
        update_inspect_item()
        if request.user.user_role == "Admin":
            return render(request, 'add_user.html')
        else:
            return redirect('/')

    def post(self, request):
        update_inspect_item()
        if request.user.user_role == "Admin":
            email = request.POST.get('email')
            password = request.POST.get('password')
            user_role = request.POST.get('role')

            # Create a new user
            try:
                # Check if any user's email contains the input email
                if User.objects.filter(email__iexact=email).exists():
                    messages.error(request, f'The email "{email}" already exists.')
                    return render(request, 'add_user.html', {'email': email, 'user_role': user_role})
                user = User.objects.create_user(username=email, email=email, password=password)

                user.user_role = user_role  # Adjust this if you're using a custom user model
                user.save()
                messages.success(request, 'User added successfully!')
                return redirect('dashboard')  # Redirect to the dashboard or another page
            except Exception as e:
                messages.error(request, f'Error adding user: {str(e)}')
                return render(request, 'add_user.html', {'email': email, 'user_role': user_role})
        else:
            return redirect('/')


class ItemListView(View):
    def get(self, request):
        update_inspect_item()
        if request.user.user_role == "Admin":
            items = Item.objects.all()
            return render(request, 'item_list.html', {'items': items})
        else:
            return redirect('/')


class AddItemView(View):
    def get(self, request):
        update_inspect_item()
        if request.user.user_role == "Admin":
            return render(request, 'add_item.html')
        else:
            return redirect('/')

    def post(self, request):
        # Get all fields from the form
        if request.user.user_role == "Admin":
            location = request.POST.get('location')
            description = request.POST.get('description')
            identification = request.POST.get('identification')
            tamper_seal = request.POST.get('tamper_seal')
            overhead_sign = request.POST.get('overhead_sign')
            checklist = request.POST.get('checklist')
            s_on_floor = request.POST.get('s_on_floor')
            comments = request.POST.get('comments')

            # Create the item
            Item.objects.create(
                location=location,
                description=description,
                identification=identification,
                tamper_seal=tamper_seal,
                overhead_sign=overhead_sign,
                checklist=checklist,
                s_on_floor=s_on_floor,
                comments=comments
            )
            messages.success(request, 'Item added successfully!')
            return redirect('item_list')
        else:
            return redirect('/')



class EditItemView(View):
    def get(self, request, item_id):
        update_inspect_item()
        item = get_object_or_404(Item, id=item_id)
        if request.user.user_role == 'Admin':
            return render(request, 'edit_item.html', {'item': item})
        else:
            return render(request, 'edit_item_user.html', {'item': item})

    def post(self, request, item_id):
        item = get_object_or_404(Item, id=item_id)
        if request.user.user_role == "Admin":

            item.location = request.POST.get('location')
            item.description = request.POST.get('description')
            item.identification = request.POST.get('identification')
            item.tamper_seal = request.POST.get('tamper_seal')
            item.overhead_sign = request.POST.get('overhead_sign')
            item.checklist = request.POST.get('checklist')
            item.s_on_floor = request.POST.get('s_on_floor')
            item.comments = request.POST.get('comments')
            item.inspected_by = request.user
            item.save()
            messages.success(request, 'Item updated successfully!')
            return redirect('item_list')
        else:
            item.s_on_floor = request.POST.get('s_on_floor')

            item.checklist = request.POST.get('checklist')
            item.inspected_by = request.user
            item.comments = request.POST.get('comments')
            item.save()
            messages.success(request, 'Item Inspect successfully!')
            return redirect('userdasboard')


class DeleteItemView(View):
    def post(self, request, item_id):
        if request.user.user_role == "Admin":
            item = get_object_or_404(Item, id=item_id)
            item.delete()
            messages.success(request, 'Item deleted successfully!')
            return redirect('item_list')
        else:
            return redirect('/')


def inspect_item(request):
    update_inspect_item()
    items = Item.objects.filter(checklist='Available')
    checklist = items.first()
    return render(request, 'item_detail.html', {'items': items, 'checklist':checklist})

def overdue_item(request):
    update_inspect_item()
    items = Item.objects.filter(checklist='Not Applicable')
    checklist = items.first()
    return render(request, 'item_detail.html', {'items': items, 'checklist':checklist})


def item_list_filter(request):
    items = Item.objects.all()
    location = request.GET.get('location')
    checklist = request.GET.get('checklist')
    description = request.GET.get('description')

    if location:
        items = items.filter(location__icontains=location)
    if checklist and checklist != "All":
        items = items.filter(checklist=checklist)
    if description:
        items = items.filter(description__icontains=description)

    context = {'items': items}
    print(request.user.user_role)
    if request.user.user_role == "Admin":
        return render(request, 'item_list.html', context)
    else:
        return render(request, 'user_dashboard.html', context)
