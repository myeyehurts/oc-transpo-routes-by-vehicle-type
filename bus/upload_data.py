import os

import django
from tablib import Dataset
from .models import Route
from bus.resource import RouteResource

def upload_from_spreadsheet(model, file_path):
    resource = model()
    dataset = Dataset()

    try:
        with open(file_path, 'r') as file:
            dataset.load(file.read(), format="csv") # read the spreadsheet file
            resource.import_data(dataset, dry_run=False) # upload and save to database
    except Exception as e:
        print(e)


def populate_tables():
    # need to upload to specific column
    upload_from_spreadsheet(RouteResource, "bus/spreadsheets/routes.csv")
    is_empty = False # keeps track of whether any spreadsheets uploads failed
    models = [Route]
    for model in models:
        if not model.objects.exists(): # check if data was uploaded to each table
            print(f"Error uploading items to the following table: {model.__name__}.") # error message if failure
            is_empty = True
    if not is_empty:
        print("Successfully populated tables.") # confirmation message
