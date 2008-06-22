# -*- coding: utf-8 -*-
#--------------------------------
#$Date$
#$Author$
#$Revision$
#--------------------------------
#Copyright (C) 2007-2008 Alexander Koshelev (daevaorn@gmail.com)
from django import http
from django.contrib.syndication import views
from django.contrib.auth.decorators import login_required
from django.contrib.admin.views.decorators import staff_member_required
from django.shortcuts import *

from turbion.feedburner.models import Feed, Account
import re

FEEDBURNER_REG = re.compile( '(feedburner|feedvalidator)', re.I )

def _create_feed( request, url, name_getter, account_getter, *args, **kwargs ):
    if not account_getter:
        return
    
    try:
        account = account_getter( request, url, *args, **kwargs )
    except Account.DoesNotExist:
        return
    
    feed = Feed( source = request.path,
                 account = account )
    
    if feed.account.base_name:
        feed.name = feed.account.base_name + "_"
    else:
        feed.name = ""
    feed.name += name_getter( request, url, *args, **kwargs )
    feed.save()
    

def feed( request, 
          url,
          feed_dict,
          view = views.feed, 
          name_getter = lambda request, url,  *args, **kwargs: url.replace( "/", "_" ),
          account_getter = lambda request, url,  *args, **kwargs: Account.objects.filter( user__is_staff = True )[0],
          *args, **kwargs ):
    try:
        f = Feed.objects.get( source = request.path )
        if f.created and not FEEDBURNER_REG.match( request.META.get( "HTTP_USER_AGENT", "" ) ):
            return http.HttpResponsePermanentRedirect( f.get_feedburner_url() )
    except Feed.DoesNotExist:
        _create_feed( request, url, name_getter, account_getter, *args, **kwargs )
                
    return view(request, url, feed_dict)

@login_required
@staff_member_required
def add_to_feedburner( request, id ):
    feed = get_object_or_404( Feed, pk = id )
    feed.add()
    
    return http.HttpResponseRedirect( request.META.get( "HTTP_REFERER", "./" ) )