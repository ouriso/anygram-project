def filter_by_tags(request, queryset):
    filter_tags = request.GET.getlist('tags')
    if filter_tags != []:
        queryset = queryset.filter(tags__in=filter_tags).distinct()
    return (queryset, filter_tags)
