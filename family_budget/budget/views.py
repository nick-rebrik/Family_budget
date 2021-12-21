from rest_framework import viewsets

from .models import BudgetsList
from .serializers import BudgetsListSerializer


class BudgetsListViewSet(viewsets.ModelViewSet):
    queryset = BudgetsList.objects.all()
    serializer_class = BudgetsListSerializer

    def perform_create(self, serializer):
        user = self.request.user
        serializer.save(user=user)
