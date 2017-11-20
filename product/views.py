import json

from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.contenttypes.models import ContentType
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage

from product.response import response_mimetype, JSONResponse, serialize
from django.db.models import Q
from django.http import HttpResponse
from django.shortcuts import render, get_object_or_404, redirect

# Create your views here.
from django.template import context
from django.urls import reverse
from django.views.generic import CreateView

from core.utils import get_real_id
from product.forms import BrandAccountForm, BrandForm
from product.models import BrandAccount, Brand


def index(request):

    return render(request, 'product/create_brand.html', context={})


@login_required
def brand_create(request, bid=None):
    if bid:
        brand = get_object_or_404(BrandAccount, id=get_real_id(bid))
    else:
        brand = None

    if request.method == "POST":
        form = BrandForm(request.POST, instance=brand)
        if form.is_valid():
            form.save()
            return redirect(reverse("product:brand-detail"))
    else:
        form = BrandForm(instance=brand)
    return render(request, 'product/brand_create.html', context={'form': form})


@login_required
def brand_detail(request, bid=None):
    if bid:
        context = [Brand.objects.filter(id=get_real_id(bid))]
    else:
        context = Brand.objects.all()

    q = request.GET.get('q', None)
    if q:
        context = context.filter(name__icontains=q)

    page = request.GET.get('page', 1)

    paginator = Paginator(context, 4)
    try:
        context = paginator.page(page)
    except PageNotAnInteger:
        context = paginator.page(1)
    except EmptyPage:
        context = paginator.page(paginator.num_pages)

    return render(request, 'product/brand_detail.html', context={'context': context, 'q': q})


@login_required
def brand_account_create(request, bid=None):
    if bid:
        brand = get_object_or_404(BrandAccount, id=get_real_id(bid))
    else:
        brand = None
    if request.method == 'POST':
        form = BrandAccountForm(request.POST, request.FILES, instance=brand)
        if form.is_valid():
            form.save()
            return redirect(reverse("product:brand-account-detail"))
    else:
        form = BrandAccountForm(instance=brand)
    return render(request, 'product/brand_account_create.html', context={'form': form})


@login_required
def brand_account_detail(request, bid=None):
    if bid:
        context = [BrandAccount.objects.filter(id=get_real_id(bid))]
    else:
        context = BrandAccount.objects.all()

    q = request.GET.get('q', None)
    if q:
        context = context.filter(Q(bran__name__icontains=q) | Q(name__icontains=q) | Q(website__icontains=q) | Q(email__icontains=q) | Q(title__icontains=q))

    page = request.GET.get('page', 1)

    paginator = Paginator(context, 4)
    try:
        context = paginator.page(page)
    except PageNotAnInteger:
        context = paginator.page(1)
    except EmptyPage:
        context = paginator.page(paginator.num_pages)

    return render(request, 'product/brand_account_detail.html', context={'context': context, 'q': q})


class BrandAccountCreateView(LoginRequiredMixin, CreateView):
    model = BrandAccount
    fields = ('brand', 'website', 'name', 'email', 'title', 'file')
    template_name = 'product/brand_account_create.html'

    def get_context_data(self, **kwargs):
        context = super(BrandAccountCreateView, self).get_context_data(**kwargs)
        context['maxImageSize'] = 50*1024*1024
        return context

    def form_valid(self, form):
        # TODO: Find away to report this error on the template, it is not reported
        def invalidate(msg):
            errors = form.errors.copy()
            errors.update({'file_size': msg})
            if self.request.is_ajax():
                return HttpResponse(content=json.dumps(errors), status=400, content_type='application/json')
            else:
                return super(JSONResponse, self).form_invalid(form)

        if int(form.files['file'].size) > (50*1024*1024):
            return invalidate("File size too large");

        self.object = form.save()
        data = {'files': [serialize(self.object)]}
        response = JSONResponse(data, mimetype=response_mimetype(self.request))
        response['Content-Disposition'] = 'inline; filename=files.json'
        return response
        # return super(POPCreateView, self).form_valid(form)

    def form_invalid(self, form):
        data = json.dumps(form.errors)
        if self.request.is_ajax():
            return HttpResponse(content=data, status=400, content_type='application/json')
        else:
            return super(JSONResponse, self).form_invalid(form)

