from __future__ import unicode_literals

# import os
from bs4 import BeautifulSoup
import urllib2
import re

from django.shortcuts import render
from django.contrib.auth.models import User
from django.contrib.auth import login as auth_login, logout as auth_logout, authenticate
from django.http.response import HttpResponseRedirect
from django_countries import countries as django_countries

import settings
from trip_constructor.models import UserProfile, Requirements, Trip
from trip_constructor.forms import ProfileForm


# login
def login(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(username=username, password=password)
        if user is None:
            return render(request, 'login.html', {'notification': 'Incorrect login or password'})
        else:
            auth_login(request, user)
            return HttpResponseRedirect('/constructor/')

    return render(request, 'login.html')


# register
def register(request):
    if request.user.is_authenticated():
        auth_logout(request)
    if request.method == 'POST':
        username = request.POST.get('username', '')
        user = User.objects.filter(username=username)
        if user:
            return render(request, 'register.html', {'notification': 'User already exists'})
        email = request.POST.get('email', '')
        password = request.POST.get('password', '')
        confirm_password = request.POST.get('confirm_password', '')
        if password and password == confirm_password:
            user = User.objects.create_user(username, email, password)
            user.save()
            # TODO: confirm email
            return HttpResponseRedirect('/')
    return render(request, 'register.html')


# visa constructor
def get_visa_constructor(request):
    if not request.user.is_authenticated():
        return HttpResponseRedirect('/')
    list_of_countries = {}
    # solve problems with key-value
    for code in settings.LIST_OF_COUNTRIES.keys():
        list_of_countries[code] = dict(django_countries).get(code)

    if request.method == 'POST': # retrieve data from wiki
        your_country = request.POST.get('your_country') # code of the country
        partner_country = request.POST.get('partner_country') # for example, DE

        arguments = {
            'your_country': your_country,
            'partner_country': partner_country,
            'list_of_countries': list_of_countries,
        }
        if 'add_countries' in request.POST: # if we add countries to user profile
            print request.POST
            countries = request.POST.getlist('countries')#.get('countries', [])
            print type(countries)
            for country in countries:
                print 'country:'
                print country
                your_requirements = Requirements.objects.filter(destination=country, nationality=your_country).first()

                partner_requirements = Requirements.objects.filter(destination=country, nationality=partner_country).first()
                trip = Trip.objects.get_or_create(user=request.user,
                                           your_requirements=your_requirements,
                                           partner_requirements=partner_requirements)[0]
                trip.save()

            arguments['notification'] = 'User profile successfully updated. To see saved countries, visit profile page'
            arguments['requirements'] = __get_requirements_from_db(your_country, partner_country) # get from db
        else:
            arguments['requirements'] = __get_requirements(your_country, partner_country) # get from wiki
        return render(request, 'visa_constructor.html', arguments)
    return render(request, 'visa_constructor.html', {'list_of_countries': list_of_countries})


def __get_requirements_from_db(your_country, partner_country):
    # custom query - to join table with requirements for both people
    query =  """
            SELECT r1.id, r1.flag as flag, r1.nationality as nationality,
            r1.notes as your_requirements, r2.notes as partner_requirements,
            r1.visa_required as your_visa, r2.visa_required as partner_visa
            FROM visa8_requirements r1
            JOIN visa8_requirements r2 ON r1.destination = r2.destination
            WHERE r1.nationality = "{your_country}"
            AND r2.nationality = "{partner_country}"
        """.format(your_country=your_country, partner_country=partner_country)

    requirements = Requirements.objects.raw(query)

    print 'requirements', requirements
    result = []  # concatenate results
    for row in requirements:
        new_row = {
            'country': row.destination,
            'flag': row.flag,
            'your_requirements': row.your_requirements,
            'partner_requirements': row.partner_requirements,
        }
        if new_row not in result:
            result.append(new_row)

    return result


# private method, parses data from the method __retrive_wiki_data and saves in DB
def __get_requirements(your_country, partner_country):
    your_url = settings.LIST_OF_COUNTRIES.get(your_country) # get url by country name
    partner_url = settings.LIST_OF_COUNTRIES.get(partner_country) # get url by country name

    your_requirements = __retrieve_wiki_data(your_url)  # get data from wiki
    partner_requirements = __retrieve_wiki_data(partner_url)

    # save requirements for user
    for row in your_requirements:
        destination = row.get('country')
        print destination
        requirements = Requirements.objects.get_or_create( # update or insert
            nationality=your_country,
            destination=row.get('country'))[0]

        if 'not required' in row.get('visa'):
            requirements.visa_required = 'not required'
        elif 'Visa required' in row.get('visa'):
            requirements.visa_required = 'required'
        else:
            requirements.visa_required = 'other'
        requirements.flag = row['flag']

        requirements.notes = row.get('visa') + ' ' + row.get('notes')
        requirements.save()

    # save requirements for partner
    if your_country != partner_country:
        for row in partner_requirements:
            requirements = Requirements()
            requirements.nationality = partner_country
            requirements.destination = row.get('country')

            if 'not required' in row.get('visa'):
                requirements.visa_required = 'not required'
            elif 'Visa required' in row.get('visa'):
                requirements.visa_required = 'required'
            else:
                requirements.visa_required = 'other'

            requirements.notes = row.get('visa') + ' ' + row.get('notes')
            requirements.save()

    result = [] # concatenate both dictionaries
    for your in your_requirements:
        index = your_requirements.index(your)
        partner = partner_requirements[index]
        new_row = {
            'country': your['country'],
            'flag': your['flag'],
            'your_requirements': your['visa'] + '\n ' + your['notes'],
            'partner_requirements': partner['visa'] + '\n ' + partner['notes'],
        }
        result.append(new_row)

    return result


# private method which retrieves and parses info from wiki
def __retrieve_wiki_data(url):
    result = []

    response = urllib2.urlopen(url) # open url
    html = response.read() # get html
    soup = BeautifulSoup(html, 'html5lib') # feed html to bs
    table = soup.find('table', attrs={'class':'sortable wikitable'}) # select necessary table
    body = table.find('tbody') # select table body

    for row in body.find_all('tr')[1:]: # select all the rows from the table, except header
        columns = row.find_all('td')
        flag = columns[0].find('img').get('src') # get icon url
        country = columns[0].find('a').get('title') # get country name
        visa = re.sub(r'\[[^)]*\]', '', columns[1].get_text()) # visa required / not required / on arrival / etc
        notes = re.sub(r'\[[^)]*\]', '', columns[2].get_text()) # notes: 30 days, etc

        # to skip this stupid country
        if 'ncipe' in country: # yeah, shitty code I know
            continue

        result.append({ # create dictionary from table row and add it to the list of results
            'country': country,
            'flag': flag,
            'visa': visa,
            'notes': notes,
        })

    return result


# show user's profile
def profile(request):
    user = request.user
    if not user.is_authenticated():
        return HttpResponseRedirect('/')

    # get saved trips
    trips = Trip.objects.filter(user=user)
    if request.method == 'POST':
        user_profile = UserProfile.objects.get(user=user)
        # to remove trips from profile
        if 'delete_countries' in request.POST:
            countries = request.POST.getlist('countries')
            for country in countries:
                trip = Trip.objects.filter(pk=country).first()
                if trip:
                    trip.delete()
            form = ProfileForm(user_profile)
        else:
            form = ProfileForm(user_profile, request.POST, request.FILES)

            # validate form and save
            if form.is_valid():
                user_profile = form.save()
                password = request.POST.get('password')
                if password:
                    user.set_password(password)
                    user.save()
            else:
                # TODO: display error message
                print form, 'not valid'
        return render(request, 'profile.html', {'form': form, 'picture': user_profile.picture, 'trips': trips, 'notification': 'User profile successfully updated'})
    user_profile = UserProfile.objects.get_or_create(user=user)[0]

    form = ProfileForm(instance=user_profile)
    return render(request, 'profile.html', {'form': form, 'picture': user_profile.picture, 'trips': trips })


def logout(request):
    auth_logout(request)
    return HttpResponseRedirect('/')