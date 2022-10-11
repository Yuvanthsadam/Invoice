from atexit import register
from django.contrib import admin
from billing.models import *

admin.site.register(Admin)
admin.site.register(Main)
admin.site.register(Sub_Title_One)
admin.site.register(Sub_Title_Two)
admin.site.register(Product)
admin.site.register(Drafted)
admin.site.register(Pending)
admin.site.register(Completed)