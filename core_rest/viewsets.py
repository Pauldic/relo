from rest_framework import viewsets, status
from rest_framework.decorators import detail_route
from rest_framework.exceptions import ParseError
from rest_framework.permissions import DjangoModelPermissions
from rest_framework.response import Response
from rest_framework.views import APIView

from core.models import Type, RetailerAccount, StoreAccount
from core_rest.serializers import TypeSerializer, StoreSerializer, RetailerSerializer, LogoUploadSeriallizer


class TypeViewSet(viewsets.ModelViewSet):
    queryset = Type.objects.all()
    serializer_class = TypeSerializer


class LogoUploadViewSet(viewsets.ModelViewSet):
    # permission_classes = (DjangoModelPermissions,)

    queryset = RetailerAccount.objects.all()
    serializer_class = LogoUploadSeriallizer


class RetailerAccountViewSet(viewsets.ModelViewSet):
    # permission_classes = (DjangoModelPermissions,)

    queryset = RetailerAccount.objects.all()
    serializer_class = RetailerSerializer

    # def create(self, request, pk=None, format=None):
    #     serializer = RetailerSerializer(data=request.data)
    #     if serializer.is_valid():
    #         serializer.save()
    #         return Response(serializer.data, status=status.HTTP_201_CREATED)
    #     return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    #
    #     try:
    #         retailer = RetailerAccount.objects.create(sChain=request.data['name'], sBanner_name=request.data['banner_name'])
    #         try:
    #             for tid in request.data['types']:
    #                 retailer.sTypes.add(Type.objects.get(id=tid))
    #             retailer.save()
    #         except KeyError:
    #             pass
    #         return Response(self.get_serializer(retailer, many=False).data)
    #     except KeyError:
    #         raise ParseError('Review parameters passed')

    # def update(self, request, *args, **kwargs):
    #     serializer = RetailerSerializer(self.get_object(pk), data=request.data)
    #     if serializer.is_valid():
    #         serializer.save()
    #         return Response(serializer.data)
    #     return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class StoreAccountViewSet(viewsets.ModelViewSet):
    """
    retrieve:
    Return the given store.

    list:
    Return a list of all the existing stores.

    create:
    Create a new store instance.

    update:
    Update existing store instance.

    partial_update:
    Partial update existing store instance.

    destroy:
    Destroy existing store instance.
    """
    queryset = StoreAccount.objects.all()
    serializer_class = RetailerSerializer


class RetailerStoreViewSet(viewsets.ModelViewSet):
    serializer_class = StoreSerializer

    def get_queryset(self):
        """
        This view should return a list of all the purchases for
        the user as determined by the username portion of the URL.
        """
        return StoreAccount.objects.filter(sChain__id=self.kwargs['id'])

