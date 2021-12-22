from rest_framework import serializers

from .models import BudgetsList, Budget, Category, BudgetOperation


class BudgetsListSerializer(serializers.ModelSerializer):
    user = serializers.CharField(source='user.username', read_only=True)

    class Meta:
        model = BudgetsList
        fields = ('id', 'title', 'user')


class BudgetSerializer(serializers.ModelSerializer):

    class Meta:
        model = Budget
        fields = (
            'id',
            'title',
            'balance',
            'currency',
            'user',
            'create_date',
        )
