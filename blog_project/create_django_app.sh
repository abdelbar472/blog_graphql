#!/bin/bash

# Ensure the script is executed with an app name argument
if [ $# -eq 0 ]; then
    echo "Usage: $0 <app_name>"
    exit 1
fi

APP_NAME=$1

# Create the Django app
python manage.py startapp $APP_NAME
if [ $? -ne 0 ]; then
    echo "Failed to create Django app"
    exit 1
fi

# Navigate to the app directory
cd $APP_NAME || exit

# Create urls.py with the specified content
cat <<EOL > urls.py
from django.urls import path
from .views import *

urlpatterns = [
    # Add your URL patterns here
]
EOL

# Create serializers.py with the specified content
cat <<EOL > serializers.py
from rest_framework import serializers
from .models import *

# Add your serializers here
EOL

# Create schema.py with the specified content
cat <<EOL > schema.py
import graphene
from graphene_django import DjangoObjectType
from .models import *

# Add your GraphQL schema here
class Query(graphene.ObjectType):
    pass
EOL

echo "Django app '$APP_NAME' created with urls.py, serializers.py, and schema.py"