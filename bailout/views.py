from django.shortcuts import render, get_object_or_404
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse, HttpResponseRedirect
from django.core.urlresolvers import reverse
from bailout.forms import MemberSearchForm, UserForm, UserProfileForm, RatingForm
from bailout.models import Bailout, UserProfile, Rating
from django.contrib.auth.models import User
from django.core.cache import cache
from django.db.models import Sum, Avg
from rest_framework.views import APIView
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from django.views.decorators.csrf import csrf_exempt
from rest_framework.renderers import JSONRenderer
from rest_framework.parsers import JSONParser
from bailout.serializers import BailoutSerializer


def index(request):
    display = 'this is a test'
    context = {
        'display' : display
    }
    return render(request, 'base.html', context)

def data(request):
    all_members = Bailout.objects.all()
    all_members_count = Bailout.objects.count()
    total_dems_count, total_reps_count = count_all_members_by_party()

    members = []

    members_searched_for = []
    if request.method == 'POST': # !!! I THINK I ONLY NEED THIS IN MEMBER_SEARCH VIEW ???
        form = MemberSearchForm(request.POST)
        if form.is_valid():
            member_name = form.cleaned_data['name']
            members_searched_for = Bailout.objects.filter(name__icontains=member_name)
    else:
        form = MemberSearchForm()


    total_PAC_all_members = Bailout.objects.aggregate(Sum('PAC'))
    avg_PAC_all_members = Bailout.objects.aggregate(Avg('PAC'))

    context = {
        'all_members' : all_members,
        'all_members_count' : all_members_count,
        'total_dems_count' : total_dems_count,
        'total_reps_count' : total_reps_count,
        'form': form,
        'members_searched_for': members_searched_for,
        'total_PAC_all_members' : total_PAC_all_members,
        'avg_PAC_all_members' : avg_PAC_all_members,
    }

    return render(request, 'data_new.html', context)

def links(request):
    return render(request, 'links.html')

def member_search(request):
    members_searched_for = []
    if request.method == 'POST':
        form = MemberSearchForm(request.POST)
        if form.is_valid():
            # return HttpResponseRedirect('data/member_search')
            member_name = form.cleaned_data['name']
            members_searched_for = Bailout.objects.filter(name__icontains=member_name)
    #make context dictionary and pass it to render
    # in html file add link back to data

    return render(request, 'member_search.html', {'members_searched_for' : members_searched_for})

def count_all_members_by_party():
    total_dems_count = cache.get('democrats', None)
    total_reps_count = cache.get('republicans', None)

    if total_dems_count and total_reps_count:
        return total_dems, total_reps
    else:
        total_dems_count = Bailout.objects.filter(party='Dem').count()
        total_reps_count = Bailout.objects.filter(party='Rep').count()
        return total_dems_count, total_reps_count


def financial_services_committee(request):
    members_financial_services_committee = Bailout.objects.filter(financial_services_committee = 1)
    members_financial_services_committee_count = Bailout.objects.filter(financial_services_committee = 1).count()

    dems_financial_services_committee_count = Bailout.objects.filter(financial_services_committee = 1).filter(party = 'Dem').count()
    reps_financial_services_committee_count = Bailout.objects.filter(financial_services_committee = 1).filter(party = 'Rep').count()

    total_PAC_financial_services = Bailout.objects.filter(financial_services_committee = 1).aggregate(Sum('PAC'))
    avg_PAC_financial_services = Bailout.objects.filter(financial_services_committee = 1).aggregate(Avg('PAC'))

    context = {
        'members_financial_services_committee' : members_financial_services_committee,
        'members_financial_services_committee_count' : members_financial_services_committee_count,
        'dems_financial_services_committee_count' : dems_financial_services_committee_count,
        'reps_financial_services_committee_count' : reps_financial_services_committee_count,
        'total_PAC_financial_services' : total_PAC_financial_services,
        'avg_PAC_financial_services' : avg_PAC_financial_services,
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
    total_members = dem_count_sw + rep_count_sw

    context = {
        'the_switchers' : the_switchers,
        'dem_count_sw' : dem_count_sw,
        'rep_count_sw' : rep_count_sw,
        'the_switchers_avg' : the_switchers_avg,
        'total_members' : total_members,
				'dummy_sw' : dummy_sw,
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
    dummy_nn = 0
    for i in nah_nah:
        try:
            dummy_nn += i.PAC
        except:
            pass
    nah_nah_avg = dummy_nn/len(nah_nah)
    total_members = dem_count + rep_count


    context = {
        'nah_nah' : nah_nah,
        'dem_count' : dem_count,
        'rep_count' : rep_count,
        'nah_nah_avg' : nah_nah_avg,
        'total_members' : total_members,
			  'dummy_nn' : dummy_nn,
    }
    return render(request, 'no_no.html', context)

def order_by_pac(request):
    membs_order_by_pac = Bailout.objects.order_by('-PAC')

    context = {
        'membs_order_by_pac' : membs_order_by_pac,
    }

    return render(request, 'order_by_pac.html', context)

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
    total_members = dem_count_yy + rep_count_yy

    context = {
        'yah_yah' : yah_yah,
        'dem_count_yy' : dem_count_yy,
        'rep_count_yy' : rep_count_yy,
        'yah_yah_avg' : yah_yah_avg,
        'total_members' : total_members,
	    'dummy_yy' : dummy_yy,
    }
    return render(request, 'yes_yes.html', context)


def analyze(request):
#____________ALL-MEMBERS_________________________________________
    all_members = Bailout.objects.all()
    dems = 0
    reps = 0


    for i in all_members:
        if i.party == 'Dem':
            dems += 1
        if i.party == 'Rep':
            reps += 1
    dummy_all = 0
    bailout_supp_all = 0
    bailout_opp_all = 0
    ada_all = 0
    for i in all_members:
        try:
            dummy_all += i.PAC
            bailout_supp_all += i.bailout_support
            bailout_opp_all += i.bailout_opposition
            ada_all += i.ada_score

        except:
            pass
    all_members_avg = dummy_all / len(all_members)
    bailout_supp_all_avg = bailout_supp_all/len(all_members)
    bailout_opp_all_avg = bailout_opp_all/len(all_members)
    ada_all_avg = ada_all / len(all_members)
#____________YES-YES_____________________________________________
    yah_yah = []
    dems_yes_yes = []
    reps_yes_yes = []
    for i in Bailout.objects.all():
        if i.vote_1 == 'Yes' and i.vote_2 == 'Yes':
            yah_yah.append(i)
    for i in yah_yah:
        if i.party == 'Dem':
            dems_yes_yes.append(i)
        if i.party == 'Rep':
            reps_yes_yes.append(i)
    dem_count_yy = len(dems_yes_yes)
    rep_count_yy = len(reps_yes_yes)
    dummy_yy = 0
    bailout_supp_yah_yah = 0
    bailout_opp_yah_yah = 0
    ada_yah_yah = 0
    for i in yah_yah:
        try:
            dummy_yy += i.PAC
            bailout_supp_yah_yah += i.bailout_support
            bailout_opp_yah_yah += i.bailout_opposition
            ada_yah_yah += i.ada_score
        except:
            pass
    yah_yah_avg = dummy_yy / len(yah_yah)
    bailout_supp_yah_yah_avg = bailout_supp_yah_yah / len(yah_yah)
    bailout_opp_yah_yah_avg = bailout_opp_yah_yah / len(yah_yah)
    ada_yah_yah_avg = ada_yah_yah / len(yah_yah)
# __________ NO-NO ___________________________________________________
    nah_nah = []
    dems_no_no = []
    reps_no_no = []
    for i in Bailout.objects.all():
        if i.vote_1 == 'No' and i.vote_2 == 'No':
            nah_nah.append(i)
    for i in nah_nah:
        if i.party == 'Dem':
            dems_no_no.append(i)
        if i.party == 'Rep':
            reps_no_no.append(i)
    dem_count_nn = len(dems_no_no)
    rep_count_nn = len(reps_no_no)
    dummy_nn = 0
    bailout_supp_nah_nah = 0
    bailout_opp_nah_nah = 0
    ada_nah_nah = 0
    for i in nah_nah:
        try:
            dummy_nn += i.PAC
            bailout_supp_nah_nah += i.bailout_support
            bailout_opp_nah_nah += i.bailout_opposition
            ada_nah_nah += i.ada_score
        except:
            pass
    nah_nah_avg = dummy_nn / len(nah_nah)
    bailout_supp_nah_nah_avg = bailout_supp_nah_nah / len(nah_nah)
    bailout_opp_nah_nah_avg = bailout_supp_nah_nah / len(nah_nah)
    ada_nah_nah_avg = ada_nah_nah / len(yah_yah)
#____________FINANCIAL SERVICES COMMITTEE____________________________________________________
    fin_serv = []
    dems_fs = []
    reps_fs = []
    for i in Bailout.objects.all():
        if i.financial_services_committee == 1:
            fin_serv.append(i)
    for i in fin_serv:
        if i.party == 'Dem':
            dems_fs.append(i)
        if i.party == 'Rep':
            reps_fs.append(i)
    dem_count_fs = len(dems_fs)
    rep_count_fs = len(reps_fs)
    dummy_fs = 0
    bailout_supp_fs = 0
    bailout_opp_fs = 0
    ada_fs = 0
    for i in fin_serv:
        try:
            dummy_fs += i.PAC
            bailout_supp_fs += i.bailout_support
            bailout_opp_fs += i.bailout_opposition
            ada_fs += i.ada_score
        except:
            pass
    fin_serv_avg = dummy_fs / len(fin_serv)
    bailout_supp_fs_avg = bailout_supp_fs / len(fin_serv)
    bailout_opp_fs_avg = bailout_opp_fs / len(fin_serv)
    ada_fs_avg = ada_fs / len(fin_serv)

#____________SWITCH______________________________________________
    the_switchers = []
    dems_sw = []
    reps_sw = []
    for i in Bailout.objects.all():
        if i.switch == 'Yes':
            the_switchers.append(i)
    for i in the_switchers:
        if i.party == 'Dem':
            dems_sw.append(i)
        if i.party == 'Rep':
            reps_sw.append(i)
    dem_count_sw = len(dems_sw)
    rep_count_sw = len(reps_sw)
    dummy_sw = 0
    bailout_supp_sw = 0
    bailout_opp_sw = 0
    ada_sw = 0
    for i in the_switchers:
        try:
            dummy_sw += i.PAC
            bailout_supp_sw += i.bailout_support
            bailout_opp_sw += i.bailout_opposition
            ada_sw += i.ada_score
        except:
            pass
    the_switchers_avg = dummy_sw / len(the_switchers)
    bailout_supp_sw_avg = bailout_supp_sw / len(the_switchers)
    bailout_opp_sw_avg = bailout_opp_sw / len(the_switchers)
    ada_sw_avg = ada_sw / len(the_switchers)

#_____________DEMS & REPS / VOTING GROUPS___________________________________________

    all_democrats = Bailout.objects.filter(party='Dem')
    all_republicans = Bailout.objects.filter(party='Rep')
    # LIST OF VARIABLES FROM SAME VIEW DECLARED EARLIER
    # dems_yes_yes, reps_yes_yes, dems_no_no, reps_no_no
    # dems_sw, reps_sw, dems_fs, reps_fs

    pac_total_all_dems = 0
    bailout_supp_all_dems_total = 0
    bailout_opp_all_dems_total = 0
    ada_all_dems = 0
    for i in all_democrats:
        try:
            pac_total_all_dems += i.PAC
            bailout_supp_all_dems_total += i.bailout_support
            bailout_opp_all_dems_total += i.bailout_opposition
            ada_all_dems += i.ada_score
        except:
            pass
    all_dems_pac_avg = pac_total_all_dems/len(all_democrats)
    all_dems_bailout_supp_avg = bailout_supp_all_dems_total/len(all_democrats)
    all_dems_bailout_opp_avg = bailout_opp_all_dems_total/len(all_democrats)
    ada_all_dems_avg = ada_all_dems/len(all_democrats)

    pac_total_all_reps = 0
    bailout_supp_all_reps_total = 0
    bailout_opp_all_reps_total = 0
    ada_all_reps = 0
    for i in all_republicans:
        try:
            pac_total_all_reps += i.PAC
            bailout_supp_all_reps_total += i.bailout_support
            bailout_opp_all_reps_total += i.bailout_opposition
            ada_all_reps += i.ada_score
        except:
            pass
    all_reps_pac_avg = pac_total_all_reps / len(all_republicans)
    all_reps_bailout_supp_avg = bailout_supp_all_reps_total / len(all_republicans)
    all_reps_bailout_opp_avg = bailout_opp_all_reps_total / len(all_republicans)
    ada_all_reps_avg = ada_all_reps / len(all_republicans)

    length_dems_yy = len(dems_yes_yes)
    pac_total_dems_yy = 0
    bailout_supp_dems_yy_total = 0
    bailout_opp_dems_yy_total = 0
    ada_dems_yy = 0

    for i in dems_yes_yes:
        try:
            pac_total_dems_yy += i.PAC
            bailout_supp_dems_yy_total += i.bailout_support
            bailout_opp_dems_yy_total += i.bailout_opposition
            ada_dems_yy += i.ada_score
        except:
            pass
    dems_yy_pac_avg = pac_total_dems_yy/len(dems_yes_yes)
    dems_yy_bailout_supp_avg = bailout_supp_dems_yy_total/len(dems_yes_yes)
    dems_yy_bailout_opp_avg = bailout_opp_dems_yy_total/len(dems_yes_yes)
    dems_yy_ada_avg = ada_dems_yy/len(dems_yes_yes)


    length_reps_yy = len(reps_yes_yes)
    pac_total_reps_yy = 0
    bailout_supp_reps_yy_total = 0
    bailout_opp_reps_yy_total = 0
    ada_reps_yy = 0
    for i in reps_yes_yes:
        try:
            pac_total_reps_yy += i.PAC
            bailout_supp_reps_yy_total += i.bailout_support
            bailout_opp_reps_yy_total += i.bailout_opposition
            ada_reps_yy += i.ada_score
        except:
            pass
    reps_yy_pac_avg = pac_total_reps_yy / len(reps_yes_yes)
    reps_yy_bailout_supp_avg = bailout_supp_reps_yy_total / len(reps_yes_yes)
    reps_yy_bailout_opp_avg = bailout_opp_reps_yy_total / len(reps_yes_yes)
    reps_yy_ada_avg = ada_reps_yy / len(reps_yes_yes)


    length_dems_nn = len(dems_no_no)
    pac_total_dems_nn = 0
    bailout_supp_dems_nn_total = 0
    bailout_opp_dems_nn_total = 0
    ada_dems_nn = 0
    for i in dems_no_no:
        try:
            pac_total_dems_nn += i.PAC
            bailout_supp_dems_nn_total += i.bailout_support
            bailout_opp_dems_nn_total += i.bailout_opposition
            ada_dems_nn += i.ada_score
        except:
            pass
    dems_nn_pac_avg = pac_total_dems_nn / len(dems_no_no)
    dems_nn_bailout_supp_avg = bailout_supp_dems_nn_total / len(dems_no_no)
    dems_nn_bailout_opp_avg = bailout_opp_dems_nn_total / len(dems_no_no)
    dems_nn_ada_avg = ada_dems_nn / len(dems_no_no)


    length_reps_nn = len(reps_no_no)
    pac_total_reps_nn = 0
    bailout_supp_reps_nn_total = 0
    bailout_opp_reps_nn_total = 0
    ada_reps_nn = 0
    for i in reps_no_no:
        try:
            pac_total_reps_nn += i.PAC
            bailout_supp_reps_nn_total += i.bailout_support
            bailout_opp_reps_nn_total += i.bailout_opposition
            ada_reps_nn += i.ada_score
        except:
            pass
    reps_nn_pac_avg = pac_total_reps_nn / len(reps_no_no)
    reps_nn_bailout_supp_avg = bailout_supp_reps_nn_total / len(reps_no_no)
    reps_nn_bailout_opp_avg = bailout_opp_reps_nn_total / len(reps_no_no)
    reps_nn_ada_avg = ada_reps_nn / len(reps_no_no)

    length_dems_sw = len(dems_sw)
    pac_total_dems_sw = 0
    bailout_supp_dems_sw_total = 0
    bailout_opp_dems_sw_total = 0
    ada_dems_sw = 0
    for i in dems_sw:
        try:
            pac_total_dems_sw += i.PAC
            bailout_supp_dems_sw_total += i.bailout_support
            bailout_opp_dems_sw_total += i.bailout_opposition
            ada_dems_sw += i.ada_score
        except:
            pass
    dems_sw_pac_avg = pac_total_dems_sw/len(dems_sw)
    dems_sw_bailout_supp_avg = bailout_supp_dems_sw_total / len(dems_sw)
    dems_sw_bailout_opp_avg = bailout_supp_dems_sw_total / len(dems_sw)
    dems_sw_ada_avg = ada_dems_sw / len(dems_sw)


    length_reps_sw = len(reps_sw)
    pac_total_reps_sw = 0
    bailout_supp_reps_sw_total = 0
    bailout_opp_reps_sw_total = 0
    ada_reps_sw = 0
    for i in reps_sw:
        try:
            pac_total_reps_sw += i.PAC
            bailout_supp_reps_sw_total += i.bailout_support
            bailout_opp_reps_sw_total += i.bailout_opposition
            ada_reps_sw += i.ada_score
        except:
            pass
    reps_sw_pac_avg = pac_total_reps_sw / len(reps_sw)
    reps_sw_bailout_supp_avg = bailout_supp_reps_sw_total / len(reps_sw)
    reps_sw_bailout_opp_avg = bailout_supp_reps_sw_total / len(reps_sw)
    reps_sw_ada_avg = ada_reps_sw / len(reps_sw)






#_____________CONTEXT_______________________________________________
    context = {
        'all_members': all_members,
        'dems': dems,
        'reps': reps,
        'all_members_avg': all_members_avg,
        'dummy_all': dummy_all,
        'bailout_supp_all_avg': bailout_supp_all_avg,
        'bailout_opp_all_avg': bailout_opp_all_avg,
        'ada_all_avg' : ada_all_avg,

        'yah_yah': yah_yah,
        'dem_count_yy': dem_count_yy,
        'rep_count_yy': rep_count_yy,
        'yah_yah_avg': yah_yah_avg,
        'dummy_yy' : dummy_yy,
        'bailout_supp_yah_yah_avg' : bailout_supp_yah_yah_avg,
        'bailout_opp_yah_yah_avg' : bailout_opp_yah_yah_avg,
        'ada_yah_yah_avg' : ada_yah_yah_avg,
        'dems_yes_yes' : dems_yes_yes,
        'reps_yes_yes' : reps_yes_yes,

        'nah_nah': nah_nah,
        'dem_count_nn': dem_count_nn,
        'rep_count_nn': rep_count_nn,
        'nah_nah_avg': nah_nah_avg,
        'dummy_nn' : dummy_nn,
        'bailout_supp_nah_nah_avg' : bailout_supp_nah_nah_avg,
        'bailout_opp_nah_nah_avg' : bailout_opp_nah_nah_avg,
        'ada_nah_nah_avg' : ada_nah_nah_avg,

        'fin_serv': fin_serv,
        'dem_count_fs': dem_count_fs,
        'rep_count_fs': rep_count_fs,
        'fin_serv_avg': fin_serv_avg,
        'dummy_fs' : dummy_fs,
        'bailout_supp_fs_avg' : bailout_supp_fs_avg,
        'bailout_opp_fs_avg' : bailout_opp_fs_avg,
        'ada_fs_avg' : ada_fs_avg,


        'the_switchers': the_switchers,
        'dem_count_sw': dem_count_sw,
        'rep_count_sw': rep_count_sw,
        'the_switchers_avg': the_switchers_avg,
        'dummy_sw' : dummy_sw,
        'bailout_supp_sw_avg' : bailout_supp_sw_avg,
        'bailout_opp_sw_avg' : bailout_opp_sw_avg,
        'ada_sw_avg' : ada_sw_avg,

        'all_democrats' : all_democrats,
        'all_republicans' : all_republicans,
        'all_dems_pac_avg' : all_dems_pac_avg,
        'all_dems_bailout_supp_avg' : all_dems_bailout_supp_avg,
        'all_dems_bailout_opp_avg' : all_dems_bailout_opp_avg,
        'ada_all_dems_avg' : ada_all_dems_avg,

        'all_reps_pac_avg' : all_reps_pac_avg,
        'all_reps_bailout_supp_avg' : all_reps_bailout_supp_avg,
        'all_reps_bailout_opp_avg' : all_reps_bailout_opp_avg,
        'ada_all_reps_avg' : ada_all_reps_avg,

        'dems_yy_pac_avg' : dems_yy_pac_avg,
        'dems_yy_bailout_supp_avg' : dems_yy_bailout_supp_avg,
        'dems_yy_bailout_opp_avg' : dems_yy_bailout_opp_avg,
        'dems_yy_ada_avg' : dems_yy_ada_avg,
        'length_dems_yy' : length_dems_yy,

        'reps_yy_pac_avg' : reps_yy_pac_avg,
        'reps_yy_bailout_supp_avg' : reps_yy_bailout_supp_avg,
        'reps_yy_bailout_opp_avg' : reps_yy_bailout_opp_avg,
        'reps_yy_ada_avg' : reps_yy_ada_avg,
        'length_reps_yy' : length_reps_yy,

        'dems_nn_pac_avg' : dems_nn_pac_avg,
        'dems_nn_bailout_supp_avg' : dems_nn_bailout_supp_avg,
        'dems_nn_bailout_opp_avg' : dems_nn_bailout_opp_avg,
        'dems_nn_ada_avg' : dems_nn_ada_avg,
        'length_dems_nn' : length_dems_nn,

        'reps_nn_pac_avg' : reps_nn_pac_avg,
        'reps_nn_bailout_supp_avg' : reps_nn_bailout_supp_avg,
        'reps_nn_bailout_opp_avg' : reps_nn_bailout_opp_avg,
        'reps_nn_ada_avg' : reps_nn_ada_avg,
        'length_reps_nn' : length_reps_nn,

        'dems_sw_pac_avg' : dems_sw_pac_avg,
        'dems_sw_bailout_supp_avg' : dems_sw_bailout_supp_avg,
        'dems_sw_bailout_opp_avg' : dems_sw_bailout_opp_avg,
        'dems_sw_ada_avg' : dems_sw_ada_avg,
        'length_dems_sw' : length_dems_sw,

        'reps_sw_pac_avg' : reps_sw_pac_avg,
        'reps_sw_bailout_supp_avg' : reps_sw_bailout_supp_avg,
        'reps_sw_bailout_opp_avg' : reps_sw_bailout_opp_avg,
        'reps_sw_ada_avg' : reps_sw_ada_avg,
        'length_reps_sw' : length_reps_sw,

        'pac_total_all_dems' : pac_total_all_dems,
        'pac_total_all_reps' : pac_total_all_reps,
        'pac_total_dems_yy' : pac_total_dems_yy,
        'pac_total_reps_yy' : pac_total_reps_yy,
        'pac_total_dems_nn' : pac_total_dems_nn,
        'pac_total_reps_nn' : pac_total_reps_nn,
        'pac_total_dems_sw' : pac_total_dems_sw,
        'pac_total_reps_sw' : pac_total_reps_sw,






    }

    return render(request, 'analyze.html', context)



def register(request):
    registered = False
    if request.method =='POST':
        user_form = UserForm(data=request.POST)
        profile_form = UserProfileForm(data=request.POST)
        if user_form.is_valid() and profile_form.is_valid():
            user = user_form.save()
            user.set_password(user.password)
            user.save()
            profile = profile_form.save(commit=False)
            profile.user = user
            if 'picture' in request.FILES:
                profile.picture = request.FILES['picture']
            profile.save()
            registered = True
        else:
            print user_form.errors, profile_form.errors
    else:
        user_form = UserForm()
        profile_form = UserProfileForm()

    context = {
        'user_form' : user_form,
        'profile_form' : profile_form,
        'registered' : registered
    }

    return render(request, 'user_registration.html', context)

def user_login(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(username=username, password=password)
        if user:
            if user.is_active:
                login(request, user)
                return HttpResponseRedirect('/bailout/dashboard')
            else:
                return HttpResponse("Your account is disabled :'(")
        else:
            print 'Invalid login details: {0}, {1}'.format(username, password)
            return HttpResponse("Invalid login details supplied.")
    else:
        return render(request, 'login.html', {})

@login_required(login_url='/')
def user_dashboard(request):
    da_user = None
    if request.user.is_authenticated():
        da_user = request.user.username
    user_profile = UserProfile.objects.get(user__username=da_user)
    members_to_rate = []
    members = []
    members = Bailout.objects.all()






    search_form = MemberSearchForm()
    if request.method == 'POST':
        if request.POST.get('moc', False):
            form = RatingForm(request.POST)
            if form.is_valid():
                rate_obj = form.save(commit=False)  # Must link rating and logged in user prior to saving
                rate_obj.user = request.user  # This line links the rating object with the user that is logged in
                rate_obj.save()
                print 'i made it this far'



        else:
            search_form = MemberSearchForm(request.POST)
            if search_form.is_valid():
                #return HttpResponseRedirect('/bailout/member_search')
                member_name = search_form.cleaned_data['name']
                members_to_rate = Bailout.objects.filter(name__icontains=member_name)


            # search_dict = {}
            # for field_name, field_value in form.cleaned_data.iteritems():
                # if field_value:
                    # search_dict[field_name] = field_value
            #print 'Search dict:\n\t{}'.format(str(search_dict))
            #members = Bailout.objects.filter(**search_dict)
    else:
        search_form = MemberSearchForm()
    context = {
        'form': search_form,
        'members_to_rate': members_to_rate,
        'members' : members,
        'da_user' : da_user,
        # 'user_state' : user_state,
        'user_profile' : user_profile,
    }
    return render(request, 'dashboard.html', context)


# @login_required(login_url='/')
# def rating_page_search(request):











    # members_to_rate = []
    # members_to_rate = Bailout.objects.all()
    #
    #
    #
    #
    #
    #
    #
    #
    #
    # # if request.method == 'POST':
    # #     form = RatingForm(request.POST)
    # #     if form.is_valid():
    # #         rate_objs = form.save(commit=False)
    # #         rate_objs.user = request.user # person who is rating the objects is the user who is requesting the information
    # #         rate_objs.save()
    # # else:
    # #     form = RatingForm()
    # # mocs = Bailout.objects.all()
    # context = {
    #     'members_to_rate' : members_to_rate,
    # }
    #
    # return render(request, 'dashboard.html', context)

@login_required(login_url='/')
def rating_page(request, identifier=None):
    member_to_rate = Bailout.objects.get(identifier=identifier)
    da_user = None
    if request.user.is_authenticated():
        da_user = request.user.username
    if request.method == 'POST':
        form = RatingForm(request.POST)
        if form.is_valid():
            rate_obj = form.save(commit=False)  # Must link rating and logged in user prior to saving
            rate_obj.user = request.user      # This line links the rating object with the user that is logged in
            rate_obj.save()
    else:
        form = RatingForm()

    context = {
        'form' : form,
        'da_user' : da_user,
        'member_to_rate' : member_to_rate,
    }

    return render(request, 'rating_page.html', context)



@login_required(login_url='/')
def user_logout(request):
    logout(request)
    return HttpResponseRedirect('/bailout/')

@login_required(login_url='/')
def members_by_user_state(request, state=None):
    da_user = request.user.username #CHANGE FOR OTHERS!!!!!!!
    # user_state = UserProfile.User.objects.get()
    # if not state:
        # make default state for user if they dont add when they sign up
    members_of_user_state = Bailout.objects.filter(state_ab=state)
    user_state = state

    context = {
        'da_user' : da_user,
        'members_of_user_state' : members_of_user_state,
        'user_state' : user_state,

    }
    return render(request, 'member_by_user_state.html', context)


@login_required(login_url='/')
def user_ratings(request):
    da_user = None
    if request.user.is_authenticated():
        da_user = request.user.username
    members_rated = Rating.objects.filter(user__username=da_user)
    total_ratings = len(members_rated)
    user_profile = UserProfile.objects.get(user__username=da_user)

    context = {
        'members_rated' : members_rated,
        'total_ratings' : total_ratings,
        'da_user' : da_user,
        'user_profile' : user_profile,
    }

    return render(request, 'user_ratings.html', context)

def explain_variables(request):
    return render(request, 'explain_variables.html')

# ==================== REST API VIEWS =======================

@api_view(['GET'])
def members_of_congress_list(request):
    if request.method == 'GET':
        members_of_congress = Bailout.objects.all()
        serializer = BailoutSerializer(members_of_congress, many=True)
        return Response(serializer.data)

@api_view(['GET'])
def member_of_congress_detail(request, name):
    try:
        member_of_congress = Bailout.objects.filter(name__icontains=name)
    except Bailout.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)

    if request.method == 'GET':
        serializer = BailoutSerializer(member_of_congress)
        return Response(serializer.data)
