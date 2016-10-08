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
    dem_count_fs = 0
    rep_count_fs = 0
    for i in Bailout.objects.all():
        if i.financial_services_committee == 1:
            fin_serv.append(i)
    for i in fin_serv:
        if i.party == 'Dem':
            dem_count_fs += 1
        if i.party == 'Rep':
            rep_count_fs += 1
    dummy_fs = 0
    for i in fin_serv:
        try:
            dummy_fs += i.PAC
        except:
            pass
    fin_serv_avg = dummy_fs/len(fin_serv)
    context = {
        'fin_serv' : fin_serv,
        'dem_count_fs' : dem_count_fs,
        'rep_count_fs' : rep_count_fs,
        'fin_serv_avg' : fin_serv_avg,
    }


    return render(request, 'financial_services_committee.html', context)

def switchers(request):
    the_switchers = []
    dem_count_sw = 0
    rep_count_sw = 0
    for i in Bailout.objects.all():
        if i.switch == 'Yes':
            the_switchers.append(i)
    for i in the_switchers:
        if i.party == 'Dem':
            dem_count_sw += 1
        if i.party == 'Rep':
            rep_count_sw += 1
    dummy_sw = 0
    for i in the_switchers:
        try:
            dummy_sw += i.PAC
        except:
            pass
    the_switchers_avg = dummy_sw/len(the_switchers)

    context = {
        'the_switchers' : the_switchers,
        'dem_count_sw' : dem_count_sw,
        'rep_count_sw' : rep_count_sw,
        'the_switchers_avg' : the_switchers_avg

    }

    return render(request, 'switchers.html', context)

def no_no(request):
    nah_nah = []
    dem_count = 0
    rep_count = 0
    for i in Bailout.objects.all():
        if i.vote_1 == 'No' and i.vote_2 == 'No':
            nah_nah.append(i)
    for i in nah_nah:
        if i.party == 'Dem':
            dem_count += 1
        if i.party == 'Rep':
            rep_count += 1
    dummy = 0
    for i in nah_nah:
        try:
            dummy += i.PAC
        except:
            pass
    nah_nah_avg = dummy/len(nah_nah)

    context = {
        'nah_nah' : nah_nah,
        'dem_count' : dem_count,
        'rep_count' : rep_count,
        'nah_nah_avg' : nah_nah_avg,
    }
    return render(request, 'no_no.html', context)

def yes_yes(request):
    yah_yah = []
    dem_count_yy = 0
    rep_count_yy = 0
    for i in Bailout.objects.all():
        if i.vote_1 == 'Yes' and i.vote_2 == 'Yes':
            yah_yah.append(i)
    for i in yah_yah:
        if i.party == 'Dem':
            dem_count_yy += 1
        if i.party == 'Rep':
            rep_count_yy += 1
    dummy_yy = 0
    for i in yah_yah:
        try:
            dummy_yy += i.PAC
        except:
            pass
    yah_yah_avg = dummy_yy/len(yah_yah)

    context = {
        'yah_yah' : yah_yah,
        'dem_count_yy' : dem_count_yy,
        'rep_count_yy' : rep_count_yy,
        'yah_yah_avg' : yah_yah_avg,
    }
    return render(request, 'yes_yes.html', context)
# Create your views here.
