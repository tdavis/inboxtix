from django.db import models

class Signup(models.Model):
    FREQUENCY_OPTS = (
        ('d', 'Daily'),
        ('w', 'Weekly'),
        ('b', 'Bi-Monthly'),
        ('m', 'Monthly')
    )
    category_id = models.PositiveIntegerField(
        help_text="Start typing a <strong>team</strong>, <strong>league</strong>,\
        <strong>artist</strong>, or <strong>performer</strong> \
        name; we'll complete it for you.")
    min_price = models.PositiveSmallIntegerField(blank=True, null=True,
        help_text="<strong>Minimum</strong> ticket price (optional)")
    max_price = models.PositiveSmallIntegerField(blank=True, null=True,
        help_text="<strong>Max</strong> ticket price (optional)")
    email = models.EmailField(
        help_text="Now we just need your <strong>Email Address</strong>")
    frequency = models.CharField(max_length=1, choices=FREQUENCY_OPTS,
        help_text="What is your desired <strong>contact interval</strong>?")
    verified = models.BooleanField(default=False, editable=False)
    last_sent = models.DateField(auto_now_add=True)
