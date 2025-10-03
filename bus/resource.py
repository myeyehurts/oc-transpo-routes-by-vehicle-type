from import_export import resources

from .models import Route


class RouteResource(resources.ModelResource):
    class Meta:
        model = Route

