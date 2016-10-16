from django.shortcuts import render
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse, HttpResponseRedirect
from django.core.urlresolvers import reverse
from bailout.forms import MemberSearchForm, UserForm, UserProfileForm, RatingForm
from bailout.models import Bailout, UserProfile
from django.contrib.auth.models import User


def index(request):
    display = 'this is a test'
    context = {
        'display' : display
    }
    return render(request, 'base.html', context)

def data(request):
    members = []
    members_1 = []
    members_1 = Bailout.objects.all()
    dems = 0
    reps = 0

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
    for i in members_1:
        if i.party == 'Dem':
            dems += 1
        if i.party == 'Rep':
            reps += 1
    dum = 0
    for i in members_1:
        try:
            dum += i.PAC
        except:
            pass
    members_avg = dum/len(members_1)
    objs = Bailout.objects.all()
    obj = objs[0]
    # display = ''
    # display += '{} - {} - {} - {} - {}<br><br>'.format(obj.identifier, obj.name, obj.state, obj.PAC, obj.switch)
    context = {
        'objs' : objs,
        'form': form,
        'members': members,
        'dems' : dems,
        'reps' : reps,
        'members_avg' : members_avg,
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

    if request.method == 'POST':
        form = MemberSearchForm(request.POST)
        if form.is_valid():
            #return HttpResponseRedirect('/bailout/member_search')
            member_name = form.cleaned_data['name']
            members_to_rate = Bailout.objects.filter(name__icontains=member_name)


            # search_dict = {}
            # for field_name, field_value in form.cleaned_data.iteritems():
                # if field_value:
                    # search_dict[field_name] = field_value
            #print 'Search dict:\n\t{}'.format(str(search_dict))
            #members = Bailout.objects.filter(**search_dict)
    else:
        form = MemberSearchForm()
    context = {
        'form': form,
        'members_to_rate': members_to_rate,
        'members' : members,
        'da_user' : da_user,
        # 'user_state' : user_state,
        'user_profile' : user_profile,
    }
    return render(request, 'dashboard.html', context)












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
            rate_obj = form.save(commit=False)
            rate_obj.user = request.user
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
    return HttpResponseRedirect(reverse('index'))

def members_by_user_state(request, state=None):
    da_user = None
    if request.user.is_authenticated():
        da_user = request.user.username
    # user_state = UserProfile.User.objects.get()
    members_of_user_state = Bailout.objects.filter(state=state)

    context = {
        'da_user' : da_user,
        'members_of_user_state' : members_of_user_state,
        # 'user_state' : user_state,

    }
    return render(request, 'member_by_user_state.html', context)
# Create your views here.