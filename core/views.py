from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from django.db.models import Q
from django.http import HttpResponse, JsonResponse
from django.shortcuts import redirect, get_object_or_404
from django.shortcuts import render
# Create your views here.
from django.urls import reverse

from core.forms import RetailerAccountForm, StoreAccountForm, TypeForm
from core.models import RetailerAccount, StoreAccount, Type
from core.utils import get_real_id, context_data


def get_context(request):
    return JsonResponse(context_data(True))


@login_required
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


@login_required
def type_detail(request, rid=None):
    if rid:
        context = Type.objects.filter(id=get_real_id(rid))
    else:
        context = Type.objects.all()

    q = request.GET.get('q', None)
    if q:
        context = context.filter(Q(sChain__icontains=q))

    page = request.GET.get('page', 1)

    paginator = Paginator(context, 4)
    try:
        context = paginator.page(page)
    except PageNotAnInteger:
        context = paginator.page(1)
    except EmptyPage:
        context = paginator.page(paginator.num_pages)
    return render(request, 'core/type_detail.html', context={'context': context, 'q': q})


@login_required
def retailer_add(request, rid=None):
    if rid:
        retailer = get_object_or_404(RetailerAccount, id=get_real_id(rid))
    else:
        retailer = None

    if request.method == "POST":
        form = RetailerAccountForm(request.POST, request.FILES, instance=retailer)
        if form.is_valid():
            form.save(commit=False)
            form.save()
            return redirect(reverse("core:retailer-detail"))
    else:
        form = RetailerAccountForm(instance=retailer)
    return render(request, "core/retailer_account.html", context={'form': form})


@login_required
def retailer_detail(request, rid=None):
    if rid:
        context = RetailerAccount.objects.filter(id=get_real_id(rid))
    else:
        context = RetailerAccount.objects.all()

    q = request.GET.get('q', None)
    if q:
        context = context.filter(Q(sChain__icontains=q))

    page = request.GET.get('page', 1)

    paginator = Paginator(context, 4)
    try:
        context = paginator.page(page)
    except PageNotAnInteger:
        context = paginator.page(1)
    except EmptyPage:
        context = paginator.page(paginator.num_pages)
    return render(request, 'core/retailer_detail.html', context={'context': context, 'q': q})


def home(request):

    return render(request, 'core/base.html', context={})


# @api_view(['GET', 'POST'])
# def api_retailer_list(request, format=None):
#     """
#     List all code Retailers, or create a new Retailer.
#     """
#     if request.method == 'GET':
#         snippets = RetailerAccount.objects.all()
#         serializer = RetailerSerializer(snippets, many=True)
#         return Response(serializer.data)
#
#     elif request.method == 'POST':
#         serializer = RetailerSerializer(data=request.data)
#         if serializer.is_valid():
#             serializer.save()
#             return Response(serializer.data, status=status.HTTP_201_CREATED)
#         return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


# @api_view(['GET', 'PUT', 'DELETE'])
# def api_retailer_detail(request, pk, format=None):
#     """
#     Retrieve, update or delete a code Retailer.
#     """
#     try:
#         snippet = RetailerAccount.objects.get(pk=pk)
#     except RetailerAccount.DoesNotExist:
#         return Response(status=status.HTTP_404_NOT_FOUND)
#
#     if request.method == 'GET':
#         serializer = RetailerSerializer(snippet)
#         return Response(serializer.data)
#
#     elif request.method == 'PUT':
#         serializer = RetailerSerializer(snippet, data=request.data)
#         if serializer.is_valid():
#             serializer.save()
#             return Response(serializer.data)
#         return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
#
#     elif request.method == 'DELETE':
#         snippet.delete()
#         return Response(status=status.HTTP_204_NO_CONTENT)


@login_required
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


@login_required
def store_detail(request, sid=None):
    if sid:
        context = [StoreAccount.objects.filter(id=get_real_id(sid))]
    else:
        context = StoreAccount.objects.all()

    q = request.GET.get('q', None)
    if q:
        context = context.filter(Q(sChain__sChain__icontains=q) | Q(sState__icontains=q) | Q(sCity__icontains=q))

    page = request.GET.get('page', 1)

    paginator = Paginator(context, 4)
    try:
        context = paginator.page(page)
    except PageNotAnInteger:
        context = paginator.page(1)
    except EmptyPage:
        context = paginator.page(paginator.num_pages)

    return render(request, 'core/store_detail.html', context={'context': context, 'q': q})


@login_required
def retailers_store(request, rid):
    context = StoreAccount.objects.filter(sChain__id=get_real_id(rid))

    q = request.GET.get('q', None)
    if q:
        context = context.filter(Q(sChain__sChain__icontains=q) | Q(sState__icontains=q) | Q(sCity__icontains=q))

    page = request.GET.get('page', 1)

    paginator = Paginator(context, 4)
    try:
        context = paginator.page(page)
    except PageNotAnInteger:
        context = paginator.page(1)
    except EmptyPage:
        context = paginator.page(paginator.num_pages)

    return render(request, 'core/store_detail.html', context={'context': context, 'q': q})


# @api_view(['GET', 'POST'])
# def api_store_list(request, format=None):
#     """
#     List all code stores, or create a new store.
#     """
#     if request.method == 'GET':
#         stores = StoreAccount.objects.all()
#         serializer = StoreSerializer(stores, many=True)
#         return Response(serializer.data)
#
#     elif request.method == 'POST':
#         serializer = StoreSerializer(data=request.data)
#         if serializer.is_valid():
#             serializer.save()
#             return Response(serializer.data, status=status.HTTP_201_CREATED)
#         return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


# @api_view(['GET', 'PUT', 'DELETE'])
# def api_store_detail(request, pk, format=None):
#     """
#     Retrieve, update or delete a code store.
#     """
#     try:
#         store = StoreAccount.objects.get(pk=pk)
#     except StoreAccount.DoesNotExist:
#         return Response(status=status.HTTP_404_NOT_FOUND)
#
#     if request.method == 'GET':
#         serializer = StoreSerializer(store)
#         return Response(serializer.data)
#
#     elif request.method == 'PUT':
#         serializer = StoreSerializer(store, data=request.data)
#         if serializer.is_valid():
#             serializer.save()
#             return Response(serializer.data)
#         return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
#
#     elif request.method == 'DELETE':
#         store.delete()
#         return Response(status=status.HTTP_204_NO_CONTENT)


# @api_view(['GET', 'POST'])
# def api_type_list(request, format=None):
#     if request.method == 'GET':
#         types = Type.objects.all()
#         serializer = TypeSerializer(types, many=True)
#         return Response(serializer.data)
#
#     elif request.method == 'POST':
#         serializer = TypeSerializer(data=request.data)
#         if serializer.is_valid():
#             serializer.save()
#             return Response(serializer.data, status=status.HTTP_201_CREATED)
#         return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
#
#
# @api_view(['GET', 'PUT', 'DELETE'])
# def api_type_detail(request, pk, format=None):
#     try:
#         type_ = Type.objects.get(pk=pk)
#     except Type.DoesNotExist:
#         return Response(status=status.HTTP_404_NOT_FOUND)
#
#     if request.method == 'GET':
#         serializer = TypeSerializer(type_)
#         return Response(serializer.data)
#
#     elif request.method == 'PUT':
#         serializer = TypeSerializer(type_, data=request.data)
#         if serializer.is_valid():
#             serializer.save()
#             return Response(serializer.data)
#         return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
#
#     elif request.method == 'DELETE':
#         type_.delete()
#         return Response(status=status.HTTP_204_NO_CONTENT)
#

def ping(request):
    return HttpResponse(status=200)


# def handler404(request):
#     response = render_to_response('404.html', {}, context_instance=RequestContext(request))
#     response.status_code = 404
#     return response
#
#
# def handler500(request):
#     response = render_to_response('500.html', {}, context_instance=RequestContext(request))
#     response.status_code = 500
#     return response