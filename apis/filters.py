import django_filters
from django_filters import ModelChoiceFilter
from apis.models import GroupImage,Images,Group




class ImagesFilter(django_filters.FilterSet):

    group = django_filters.NumberFilter(method='filter_by_group_id')
    class Meta:
        model = Images
        fields = ['title',"group"]

    def filter_by_group_id(self, queryset, name, value):
        return queryset.filter(group_images__group=value)