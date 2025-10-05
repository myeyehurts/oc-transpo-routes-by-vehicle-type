from import_export import resources, fields

from .models import Route


class RouteResource(resources.ModelResource):
    number = fields.Field(column_name='route_id', attribute='number')
    destination = fields.Field(column_name='route_long_name', attribute='destination')
    bg_colour = fields.Field(column_name='route_color', attribute='bg_colour')
    text_colour = fields.Field(column_name='route_text_color', attribute='text_colour')

    class Meta:
        model = Route
        fields = ('number', 'destination', 'bg_colour', 'text_colour')
        import_id_fields = ('number',)

