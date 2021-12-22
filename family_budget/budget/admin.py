from django.contrib import admin
from .models import (BudgetsList, Budget, BudgetOperation,
                     Category, SharePermission)

admin.site.register(BudgetsList)
admin.site.register(SharePermission)
admin.site.register(Budget)
admin.site.register(BudgetOperation)
admin.site.register(Category)
