import json
from http.client import HTTPResponse

from django.core import serializers
from django.http import JsonResponse
from django.utils.decorators import method_decorator
from django.views import View
from django.views.decorators.csrf import csrf_exempt
from django.views.generic import TemplateView
from rest_framework import viewsets, status
from rest_framework.decorators import api_view
from rest_framework.response import Response

from core.models import URL
from core.serializers import URLSerializer


class HomeView(TemplateView):
    template_name = "home.html"


class ActiveEndpointsView(TemplateView):
    template_name = "active_endpoints.html"


class EndpointView(TemplateView):
    template_name = "view_endpoint.html"


@api_view(['GET', 'POST'])
def url_endpoint(request, *args, **kwargs):
    """
    Get or Create a URL endpoint and it's details.
    """
    if request.method == 'GET':
        endpoint = kwargs.get('endpoint')
        # If there is no endpoint, this block will get all the endpoints
        if not endpoint:
            url_query_set = URL.objects.all()
            serializer = URLSerializer(url_query_set, many=True)
            return Response(serializer.data)

        # If there is endpoint, this block will get details for that particular endpoint
        try:
            url_obj = URL.objects.get(endpoint=endpoint)
            url_obj.hit_count += 1
            url_obj.save()
        except URL.DoesNotExist:
            return Response(data={'error': True, 'message': f'Could not found endpoint: {endpoint}'},
                            status=status.HTTP_404_NOT_FOUND)
        serializer = URLSerializer(url_obj)
        return Response(serializer.data)

    else:
        # POST Method: To create the endpoint
        # First check if the endpoint exists, if exists then throws error else creates the endpoint
        endpoint = request.data.get("endpoint")
        try:
            url_obj = URL.objects.get(endpoint=endpoint)
        except URL.DoesNotExist:
            url_obj = None
        if url_obj:
            return Response(data={'error': True, 'message': f'Same endpoint: {endpoint} already exist'},
                            status=status.HTTP_400_BAD_REQUEST)
        serialized_data = {
            'endpoint': endpoint,
            'url_data': [],
            'headers': str(request.headers)
        }
        query_param_data = {'query_params': [], 'raw_body': []}
        for key, value in request.data.items():
            if 'query_param' in key:
                query_param_data.get('query_params').append(value)
            if 'raw_body' in key:
                query_param_data.get('raw_body').append(value)
        serialized_data.update({'url_data': str(query_param_data)})
        serializer = URLSerializer(data=serialized_data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
