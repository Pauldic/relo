from django.db import transaction
from rest_framework import serializers

from core.models import RetailerAccount, StoreAccount, Type


class TypeSerializer(serializers.ModelSerializer):
    name = serializers.CharField(source='sType')

    class Meta:
        model = Type
        fields = ('id', 'name')


class LogoUploadSeriallizer(serializers.ModelSerializer):
    logo = serializers.ImageField(source='sLogo', default=None, allow_null=False)

    class Meta:
        model = RetailerAccount
        fields = ('id', 'logo')


class RetailerSerializer(serializers.ModelSerializer):
    name = serializers.CharField(source='sChain')
    banner_name = serializers.CharField(source='sBanner_name')
    logo = serializers.ImageField(source='sLogo', default=None, allow_null=True)
    # types = TypeSerializer(source='sTypes', many=True, allow_null=True, default=None, read_only=False)
    # types = serializers.PrimaryKeyRelatedField(source='sTypes', queryset=Type.objects.all(), many=True, allow_null=True, default=None, read_only=False)
    # types = serializers.StringRelatedField(source='sTypes', many=True) # if you want it to be Readonly
    types = serializers.HyperlinkedRelatedField(source='sTypes', queryset=Type.objects.all(), many=True, view_name='core-api:type-detail', allow_null=True, read_only=False)  # if you want it to be Readonly
    # types = serializers.HyperlinkedIdentityField(source='sTypes', many=True, view_name='type-detail') # if you want it to be Readonly
    # types = serializers.SlugRelatedField(source='sTypes', queryset=Type.objects.all(), many=True, slug_field='sType')

    class Meta:
        model = RetailerAccount
        fields = ('id', 'name', 'banner_name', 'logo', 'types')

    # @transaction.atomic
    # def create(self, validated_data):
    #     types = []
    #     try:
    #         # types = Type.objects.filter(pk__in=validated_data.pop('sTypes'))
    #         types = validated_data.pop('sTypes')
    #     except KeyError:
    #         pass
    #     instance = RetailerAccount.objects.create(**validated_data)
    #     if len(types) > 0:
    #         for type in types:
    #             instance.sTypes.add(type)
    #         instance.save()
    #     return instance


class StoreSerializer(serializers.ModelSerializer):
    retailer = RetailerSerializer(source='sChain', many=False)
    # retailer = serializers.PrimaryKeyRelatedField(source='sChain', queryset=RetailerAccount.objects.all())
    add_one = serializers.CharField(source='sAddOne')
    city = serializers.CharField(source='sCity')
    state = serializers.CharField(source='sState')
    zip = serializers.IntegerField(source='sZip')
    phone = serializers.CharField(source='sPhoneOne')

    class Meta:
        model = StoreAccount
        fields = ('id', 'retailer', 'add_one', 'city', 'state', 'zip', 'phone')

