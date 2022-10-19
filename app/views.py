from csv import excel
from gc import garbage
from urllib import response
from django.shortcuts import HttpResponse, HttpResponseRedirect, render
from django.views import View
from django.forms import formset_factory, modelformset_factory
from .forms import BinsForm
from django.contrib import messages
from .models import Bin, Garbage
from django.urls import reverse
from django.contrib.auth.decorators import login_required
import pandas as pd

# Create your views here.


def index_view(request):
    if request.user.is_authenticated:
        return HttpResponseRedirect(reverse('dashboard'))
    return render(request, 'index.html')


@login_required()
def dashboard_view(request):
    bins = Bin.objects.all()
    # breakpoint()
    return render(request, 'dashboard.html', {'bins': bins})



class AddBinsFormView(View):
    form = BinsForm
    template_name="add_bins.html"

    # Overiding the get method
    def get(self,request,*args,**kwargs):
        context={'form':self.form(),}
        return render(request, self.template_name, context)

    #Overiding the post method
    def post(self, request, *args, **kwargs):
        form = self.form(self.request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Bin Created Successfully...✅')
            form = self.form()
        return render(request, self.template_name, context={'form': form})



@login_required()
def details_view(request):
    bin_id = request.GET.get('bin_id', None)
    if bin_id:
        try: 
            bin = Bin.objects.get(id=bin_id)
            garbages = bin.garbage_set.all().order_by('-date')[:5]
            chart_value = [g.garbage_level for g in garbages[::-1]]
            chart_level = [g.date.strftime("%I:%M %p") for g in garbages[::-1]]
        except:
            bin = garbages = chart_value = chart_level = None
        return render(request, 'details.html', {"bin": bin, "garbages": garbages, "chart_level": chart_level, "chart_value":chart_value})
    else:
        return HttpResponseRedirect(reverse('dashboard'))


@login_required()
def delete_view(request):
    bin_id = request.GET.get('bin_id', None)
    if bin_id:
        Bin.objects.filter(id=bin_id).delete()
    return HttpResponseRedirect(reverse('dashboard'))


@login_required()
def download_view(request):
    bin_id = request.GET.get('bin_id', None)
    if bin_id:
        bin = Bin.objects.get(id=bin_id)
        garbages = bin.garbage_set.all().order_by('-date')
        df = pd.DataFrame.from_records([g.to_dict() for g in garbages])
        response = HttpResponse(content_type='text/csv')
        response['Content-Disposition'] = 'attachment; filename={}.csv'.format(bin.name)
        df.to_csv(path_or_buf=response, index=False)
        return response
    return HttpResponseRedirect(reverse('dashboard'))


class UpdateBinsFormView(View):
    form = BinsForm
    template_name="add_bins.html"

    # Overiding the get method
    def get(self, request, *args,**kwargs):
        bin_id = request.GET.get('bin_id', None)
        if bin_id:
            bin = Bin.objects.get(id=bin_id)
            request.session["bin_id"] = bin_id
            form = self.form(instance=bin)
            return render(request, self.template_name, {"form": form})
        else:
            return HttpResponseRedirect(reverse('dashboard'))

    #Overiding the post method
    def post(self, request, *args, **kwargs):
        form = self.form(self.request.POST)
        if form.is_valid():
            bin_id = request.session["bin_id"]
            bin = Bin.objects.get(id=bin_id)
            bin_form = self.form(form.cleaned_data, instance=bin)
            bin_form.save()
            request.session.pop('bin_id', None)
            messages.success(request, 'Bin Updated Successfully...✅')
        return render(request, self.template_name, context={'form': form})
