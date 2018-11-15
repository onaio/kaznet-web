"""
Views Module for Ona App
"""
from rest_framework import status
from rest_framework.decorators import api_view, parser_classes
from rest_framework.parsers import JSONParser
from rest_framework.response import Response
from rest_framework_json_api.parsers import JSONParser as JSONAPIParser

from kaznet.apps.ona.api import process_ona_webhook


@api_view(['GET', 'POST'])
@parser_classes([JSONParser, JSONAPIParser])
def create_or_update_instance(request):
    """
    Creates or Updates an Instance
    """
    if request.method == 'POST':
        data = request.data
        if process_ona_webhook(data):
            return Response({"success": True}, status=status.HTTP_200_OK)
    return Response({"success": False}, status=status.HTTP_400_BAD_REQUEST)
