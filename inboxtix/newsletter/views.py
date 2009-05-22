import time
from hashlib import md5
from django.http import HttpResponse, HttpResponseRedirect
from django.conf import settings
from django.core.mail import send_mail
from django.template.loader import render_to_string
from inboxtix.newsletter.models import Signup
from inboxtix.newsletter.forms import SignupForm

def signup(request):
    form = SignupForm(request.POST)
    if form.is_valid():
        obj = form.save()
        if obj.verified:
            verified = ''
        else:
            verified = 'verify'
            # CAUTION: if you fail to change the SECRET_KEY variable in your
            # settings.py, it would be quite simple for someone to `crack`
            # this verification scheme by looking at the next line ;)
            verify_hash = md5(obj.email+settings.SECRET_KEY).hexdigest()
            email_part = obj.email[0:obj.email.index('@')]
            subject = render_to_string('newsletter/verification_subject.txt',
                {'prefix':settings.EMAIL_PREFIX}).strip()
            message = render_to_string('newsletter/verification_email.txt',
                {'verify_url':'/'.join((settings.SITE_URL, 'newsletter',
                'verify', email_part, verify_hash))})
            send_mail(subject, message, settings.EMAIL_HOST_USER, [obj.email])

        return HttpResponse(verified)
    else:
        errors = '\n'.join(['%s::%s' % (k,v) for k,v in form.errors.items()])
        return HttpResponse(errors)

def verify(request, email_part, email_hash):
    possibles = Signup.objects.filter(email__startswith=email_part)
    possibles = possibles.distinct('email')
    for p in possibles:
        if md5(p.email+settings.SECRET_KEY).hexdigest() == email_hash:
            p.verified = True
            p.save()
            return HttpResponseRedirect('/?verified=True')
    return HttpResponseRedirect('/?verified=False')

