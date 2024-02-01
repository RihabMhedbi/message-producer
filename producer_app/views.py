import requests
from rest_framework import viewsets, status
from rest_framework.authentication import BasicAuthentication
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_api_key.permissions import HasAPIKey

from message_producer.settings import CONSUMER_URL
from producer_app.models import Message
from producer_app.serializers import MessageSerializer


class MessageViewSet(viewsets.ModelViewSet):
    authentication_classes = [BasicAuthentication]
    permission_classes = [IsAuthenticated]
    queryset = Message.objects.all()
    serializer_class = MessageSerializer

    def create(self, request, *args, **kwargs):
        create_response = super().create(request, *args, **kwargs)
        response = requests.post(f"{CONSUMER_URL}/api/process_message/",
                                 json={"message": request.data.get('text'),
                                       "webhook_url": f"/webhook/{create_response.data.get('id')}/"})
        return Response(response.json(), status=create_response.status_code)


class WebhookReceiverView(APIView):
    permission_classes = [HasAPIKey]

    def post(self, request, message_id):
        result = request.data.get('result')
        if not result:
            return Response({'error': 'Result not provided'}, status=status.HTTP_400_BAD_REQUEST)
        try:
            message = Message.objects.get(pk=message_id)
            message.text = result
            message.save()
            return Response({'message': 'Message updated successfully'}, status=status.HTTP_200_OK)
        except Message.DoesNotExist:
            return Response({'message': 'Message not found'}, status=status.HTTP_404_NOT_FOUND)
