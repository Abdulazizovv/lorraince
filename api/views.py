from botapp.models import BotUser
from botapp.serializers import BotUserSerializer
from product.models import SoftSlide
from product.serializers import SoftSlideSerializer
from rest_framework.generics import ListAPIView, RetrieveAPIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from core.pagination import GlobalPagination


class BotUserListView(ListAPIView):
    queryset = BotUser.objects.all()
    serializer_class = BotUserSerializer
    permission_classes = [IsAuthenticated]
    pagination_class = GlobalPagination
    

class BotUserDetailView(RetrieveAPIView):
    queryset = BotUser.objects.all()
    serializer_class = BotUserSerializer
    permission_classes = [IsAuthenticated]

    def get(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(instance)
        return Response(serializer.data)
    
class SoftSlideListView(ListAPIView):
    queryset = SoftSlide.objects.all()
    serializer_class = SoftSlideSerializer
    permission_classes = [IsAuthenticated]
    pagination_class = GlobalPagination

class SoftSlideDetailView(RetrieveAPIView):
    queryset = SoftSlide.objects.all()
    serializer_class = SoftSlideSerializer
    permission_classes = [IsAuthenticated]

    def get(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(instance)
        return Response(serializer.data)