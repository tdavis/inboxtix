from django.forms import ModelForm, ValidationError, CharField
from django.forms.util import ErrorList
from inboxtix.util import get_api_tree
from inboxtix.newsletter.models import Signup


class SignupForm(ModelForm):
    category_id = CharField(help_text=Signup._meta.fields[1].help_text)
    class Meta:
        model = Signup

    def __init__(self, *args, **kwargs):
        super(SignupForm, self).__init__(*args, **kwargs)
        # Add the `required` class for styling
        for f in self.fields:
            if self.fields[f].required:
                self.fields[f].widget.attrs['class'] = 'required'

    def save(self, *args, **kwargs):
        obj = super(SignupForm, self).save(*args, **kwargs)
        # Verification stuff
        count = Signup.objects.filter(email=obj.email, verified=True).count()
        if count > 0:
            obj.verified = True
            obj.save()
        return obj

    def clean_category_id(self):
        val = self.cleaned_data['category_id']
        tree = get_api_tree('category', 'search', **{'name':val, 'limit':1})
        cat = tree.find('category')
        if not cat:
            msg = "You didn't choose a valid category!"
            raise ValidationError(msg)
        else:
            # We actually want the category's ID so we don't have to look it up
            # when querying for events and tickets.
            return int(cat.find('id').text)

