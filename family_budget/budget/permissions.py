from django.db.models import Q
from rest_framework import permissions

from .models import SharePermission


class AdmittedOrOwner(permissions.BasePermission):

    def has_permission(self, request, view):
        user = request.user
        return (
            SharePermission.objects.filter(
                budgets_list__id=view.kwargs['list_id']
            ).filter(Q(owner=user) | Q(user=user))
        )


class OnlyOwnerDelete(permissions.BasePermission):

    def has_permission(self, request, view):
        if request.method != 'DELETE':
            return True
        return request.user == view.get_object().owner
