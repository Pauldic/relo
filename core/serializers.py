from rest_framework import serializers

from core.models import RetailerAccount, StoreAccount, Type


class TypeSerializer(serializers.ModelSerializer):
    tid = serializers.IntegerField(source='id')
    name = serializers.CharField(source='sType')

    class Meta:
        model = Type
        fields = ('tid', 'name')


class RetailerSerializer(serializers.ModelSerializer):
    rid = serializers.IntegerField(source='id')
    name = serializers.CharField(source='sChain')
    banner_name = serializers.CharField(source='sBanner_name')
    logo = serializers.CharField(source='sLogo')
    types = TypeSerializer(source='sTypes', many=True, read_only=True)

    class Meta:
        model = RetailerAccount
        fields = ('rid', 'name', 'banner_name', 'logo', 'types')


class StoreSerializer(serializers.ModelSerializer):
    sid = serializers.IntegerField(source='id')

    retailer = RetailerSerializer(source='sChain', many=False, read_only=True)
    # retailer = serializers.PrimaryKeyRelatedField(source='sChain', queryset=RetailerAccount.objects.all())
    add_one = serializers.CharField(source='sAddOne')
    city = serializers.CharField(source='sCity')
    state = serializers.CharField(source='sState')
    zip = serializers.IntegerField(source='sZip')
    phone = serializers.CharField(source='sPhoneOne')

    class Meta:
        model = StoreAccount
        fields = ('sid', 'retailer', 'add_one', 'city', 'state', 'zip', 'phone')

