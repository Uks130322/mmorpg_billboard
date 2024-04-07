from django_filters import FilterSet, ModelChoiceFilter
from .models import Advert, Respond


class RespondFilter(FilterSet):
    advert = ModelChoiceFilter(
        queryset=Respond.objects.all(),
        lookup_expr='exact',
        label='Объявление',
        empty_label='Все объявления',
        field_name='advert_id'
    )

    class Meta:
        model = Respond
        fields = []

    def __init__(self, *args, **kwargs):
        super(RespondFilter, self).__init__(*args, **kwargs)
        self.filters['advert'].queryset = Advert.objects.filter(user_id=kwargs['request'])
