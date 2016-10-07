from django.shortcuts import render

from django.http import HttpResponse, HttpResponseRedirect
from bailout.forms import MemberSearchForm
from bailout.models import Bailout

def index(request):
    display = 'this is a test'
    context = {
        'display' : display
    }
    return render(request, 'base_bailout.html', context)

def data(request):
    members = []
    if request.method == 'POST':
        form = MemberSearchForm(request.POST)
        if form.is_valid():
            #return HttpResponseRedirect('/bailout/member_search')
            member_name = form.cleaned_data['name']
            members = Bailout.objects.filter(name__icontains=member_name)


            # search_dict = {}
            # for field_name, field_value in form.cleaned_data.iteritems():
                # if field_value:
                    # search_dict[field_name] = field_value
            #print 'Search dict:\n\t{}'.format(str(search_dict))
            #members = Bailout.objects.filter(**search_dict)
    else:
        form = MemberSearchForm()

    objs = Bailout.objects.all()
    obj = objs[0]
    display = ''
    display += '{} - {} - {} - {} - {}<br><br>'.format(obj.identifier, obj.name, obj.state, obj.PAC, obj.switch)
    context = {
        'objs' : objs,
        'form': form,
        'members': members
    }
    return render(request, 'data.html', context)

def links(request):
    return render(request, 'links.html')

def member_search(request):
    members = []
    if request.method == 'POST':
        form = MemberSearchForm(request.POST)
        if form.is_valid():
            # return HttpResponseRedirect('data/member_search')
            member_name = form.cleaned_data['name']
            members = Bailout.objects.filter(name__icontains=member_name)
    #make context dictionary and pass it to render
    # in html file add link back to data

    return render(request, 'member_search.html', {'members':members})

def financial_services_committee(request):
    fin_serv = []
    for i in Bailout.objects.all():
        if i.financial_services_committee == 1:
            fin_serv.append(i)

    return render(request, 'financial_services_committee.html', {'fin_serv':fin_serv})
# Create your views here.
