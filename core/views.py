import sys

from django.conf import settings
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from django.shortcuts import render, redirect, get_object_or_404

# Create your views here.
from django.urls import reverse
from multiprocessing import get_context
from rest_framework import status, permissions
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework.views import APIView

from core.forms import RetailerAccountForm, StoreAccountForm, TypeForm
from core.serializers import RetailerSerializer, StoreSerializer, TypeSerializer
from core.utils import context_data, get_real_id
from django.shortcuts import render

from core.models import RetailerAccount, StoreAccount, Type


def type_add(request, rid=None):
    if rid:
        retailer = get_object_or_404(Type, id=get_real_id(rid))
    else:
        retailer = None

    if request.method == "POST":
        form = TypeForm(request.POST, request.FILES, instance=retailer)
        if form.is_valid():
            form.save()
            return redirect(reverse("core:type-detail"))
    else:
        form = TypeForm(instance=retailer)
    return render(request, "core/type_create.html", context={'form': form})


def type_detail(request, rid=None):
    if rid:
        context = Type.objects.filter(id=get_real_id(rid))
    else:
        context = Type.objects.all()

    page = request.GET.get('page', 1)

    paginator = Paginator(context, 4)
    try:
        context = paginator.page(page)
    except PageNotAnInteger:
        context = paginator.page(1)
    except EmptyPage:
        context = paginator.page(paginator.num_pages)
    return render(request, 'core/type_detail.html', context={'context': context})



def retailer_add(request, rid=None):
    if rid:
        retailer = get_object_or_404(RetailerAccount, id=get_real_id(rid))
    else:
        retailer = None

    if request.method == "POST":
        form = RetailerAccountForm(request.POST, request.FILES, instance=retailer)
        if form.is_valid():
            form.save()
            return redirect(reverse("core:retailer-detail"))
    else:
        form = RetailerAccountForm(instance=retailer)
    return render(request, "core/retailer_account.html", context={'form': form})


def retailer_detail(request, rid=None):
    if rid:
        context = RetailerAccount.objects.filter(id=get_real_id(rid))
    else:
        context = RetailerAccount.objects.all()

    page = request.GET.get('page', 1)

    paginator = Paginator(context, 4)
    try:
        context = paginator.page(page)
    except PageNotAnInteger:
        context = paginator.page(1)
    except EmptyPage:
        context = paginator.page(paginator.num_pages)
    return render(request, 'core/retailer_detail.html', context={'context': context})


def home(request):
    return render(request, 'core/base.html', context={})


@api_view(['GET', 'POST'])
def api_retailer_list(request, format=None):
    """
    List all code Retailers, or create a new Retailer.
    """
    if request.method == 'GET':
        snippets = RetailerAccount.objects.all()
        serializer = RetailerSerializer(snippets, many=True)
        return Response(serializer.data)

    elif request.method == 'POST':
        serializer = RetailerSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET', 'PUT', 'DELETE'])
def api_retailer_detail(request, pk, format=None):
    """
    Retrieve, update or delete a code Retailer.
    """
    try:
        snippet = RetailerAccount.objects.get(pk=pk)
    except RetailerAccount.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

    if request.method == 'GET':
        serializer = RetailerSerializer(snippet)
        return Response(serializer.data)

    elif request.method == 'PUT':
        serializer = RetailerSerializer(snippet, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    elif request.method == 'DELETE':
        snippet.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


def store_add(request, sid=None):
    if sid:
        store = get_object_or_404(StoreAccount, id=get_real_id(sid))
    else:
        store = None

    if request.method == "POST":
        form = StoreAccountForm(request.POST, instance=store)
        if form.is_valid():
            form.save()
            return redirect(reverse("core:store-detail"))
    else:
        form = StoreAccountForm(instance=store)
    return render(request, "core/create_account.html", context={'form': form})


def store_detail(request, sid=None):
    if sid:
        context = [StoreAccount.objects.filter(id=get_real_id(sid))]
    else:
        context = StoreAccount.objects.all()

    page = request.GET.get('page', 1)

    paginator = Paginator(context, 4)
    try:
        context = paginator.page(page)
    except PageNotAnInteger:
        context = paginator.page(1)
    except EmptyPage:
        context = paginator.page(paginator.num_pages)
    return render(request, 'core/store_detail.html', context={'context': context})


def retailers_store(request, rid):
    return render(request, 'core/store_detail.html', context={'context': StoreAccount.objects.filter(sChain__id=get_real_id(rid))})


@api_view(['GET', 'POST'])
def api_store_list(request, format=None):
    """
    List all code stores, or create a new store.
    """
    if request.method == 'GET':
        stores = StoreAccount.objects.all()
        serializer = StoreSerializer(stores, many=True)
        return Response(serializer.data)

    elif request.method == 'POST':
        serializer = StoreSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET', 'PUT', 'DELETE'])
def api_store_detail(request, pk, format=None):
    """
    Retrieve, update or delete a code store.
    """
    try:
        store = StoreAccount.objects.get(pk=pk)
    except StoreAccount.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

    if request.method == 'GET':
        serializer = StoreSerializer(store)
        return Response(serializer.data)

    elif request.method == 'PUT':
        serializer = StoreSerializer(store, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    elif request.method == 'DELETE':
        store.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


@api_view(['GET', 'POST'])
def api_type_list(request, format=None):
    if request.method == 'GET':
        types = Type.objects.all()
        serializer = TypeSerializer(types, many=True)
        return Response(serializer.data)

    elif request.method == 'POST':
        serializer = TypeSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET', 'PUT', 'DELETE'])
def api_type_detail(request, pk, format=None):
    try:
        type_ = Type.objects.get(pk=pk)
    except Type.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

    if request.method == 'GET':
        serializer = TypeSerializer(type_)
        return Response(serializer.data)

    elif request.method == 'PUT':
        serializer = TypeSerializer(type_, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    elif request.method == 'DELETE':
        type_.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


class ContextView(APIView):
    def get(self, request, format=None):
        return Response(context_data(True))