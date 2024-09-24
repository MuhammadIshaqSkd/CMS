from django.utils import timezone

from dashboard.models import Item


def update_inspect_item():
    all_items = Item.objects.filter(checklist="Available")
    for items in all_items:
        if items.created >= timezone.now():

            items.checklist = "Not Applicable"
            items.save()
