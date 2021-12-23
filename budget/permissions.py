from django.db.models import Q
from rest_framework import permissions

from .models import SharePermission, BudgetsList


class AdmittedOrOwner(permissions.BasePermission):

    def has_permission(self, request, view):
        user = request.user
        return (BudgetsList.objects.filter(
            id=view.kwargs['list_id']
        ).filter(
            Q(owner=user.id) | Q(shared_permissions__user=user.id)
        ))


class OnlyOwnerDelete(permissions.BasePermission):

    def has_permission(self, request, view):
        if request.method != 'DELETE':
            return True
        return request.user.id == view.get_object().owner
