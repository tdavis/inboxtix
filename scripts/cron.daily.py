#! /usr/bin/env python

import re
from lxml import etree
from datetime import date, timedelta
from django.template.loader import render_to_string
from django.conf import settings
from django.core.mail import send_mail
from inboxtix.util import get_api_tree, indent
from inboxtix.util import wrap_onspace_strict as wrapper
from inboxtix.newsletter.models import Signup

# REMINDER: set $DJANGO_SETTINGS_MODULE prior to running this script!

if __name__ == '__main__':
    ticket_table_labels = ('Price (ea)', 'Section', 'Qty')
    today = date.today()
    todo = Signup.objects.filter(last_sent__lt=today)
    for nl in todo:
        if (nl.frequency == 'w' and nl.last_sent > today - timedelta(days=7) or
            nl.frequency == 'b' and nl.last_sent > today - timedelta(days=14)):
            continue
    
        if nl.frequency in ('d','w'):
            days = 7
            trange = 'week'
            if nl.frequency == 'd':
                frequency = 'daily'
            else:
                frequency = 'weekly'
        else:
            days = 14
            trange = 'two weeks'
            frequency = 'bi-monthly'
        wrange = (today, today + timedelta(days=days))
        kwargs = {
            'category_id': nl.category_id,
            'date_start': wrange[0],
            'date_end': wrange[1],
        }
        tree = get_api_tree('event', 'search', **kwargs)
        kwargs = {
            'frequency': frequency,
            'range': trange,
            'events' : []
        }
        count = 0
        total_count = 0
        for event in tree.iter('event'):
            total_count += 1
            if count == 0:
                # Get category stuff here
                catid = event.find('category_id').text
                cattree = get_api_tree('category', 'by_id', **{ 'id': catid })
                kwargs['category_name'] = cattree.find('name').text
                kwargs['category_slug'] = cattree.find('slug').text
            # Only show settings.EVENTS_PER_EMAIL events in the email; we still
            # want a total count, though.
            if count > settings.EVENTS_PER_EMAIL:
                continue
            # Event stuff
            e = {}
            e['tickets'] = []
            for label in ('min_price', 'max_price', 'venue_string', 'name', 'url'):
                e[label] = event.find(label).text
            # Ticket stuff
            tkwargs = {
                'event_id': event.find('id').text,
                'block': 1,
                # Cushion, in case of parking / vip listings
                'limit': 20
            }
            # Support for min/max price
            if nl.min_price:
                tkwargs['min_price'] = nl.min_price
            if nl.max_price:
                tkwargs['max_price'] = nl.max_price
            tixtree = get_api_tree('tickets', 'by_event', **tkwargs)
            for t in tixtree.iter('ticketdict'):
                ticket = []
                ticket_count = 0
                for label in ('price', 'section', 'quantity'):
                    ticket.append(t.find(label).text)
                # Let's filter out parking and VIP junk
                if re.search(r'(vip)|(parking)|(pass)', ticket[1], re.I):
                    continue
                e['tickets'].append(ticket)
                ticket_count += 1
                if ticket_count == 10:
                    break
            tix_table = indent([ticket_table_labels]+e['tickets'],
                hasHeader=True, separateRows=True, prefix='| ',
                postfix=' |', wrapfunc=lambda x: wrapper(x, 80))
            e['tickets'] = tix_table
            # Put it together
            kwargs['events'].append(e)
            count += 1

    if total_count > settings.EVENTS_PER_EMAIL:
        kwargs['count'] = total_count - settings.EVENTS_PER_EMAIL
    subject = render_to_string('newsletter/ticket_subject.txt',
        {'prefix': settings.EMAIL_PREFIX}).strip()
    message = render_to_string('newsletter/ticket_email.txt', kwargs)
    send_mail(subject, message, settings.EMAIL_HOST_USER, [nl.email])

    nl.last_sent = today
    nl.save()

