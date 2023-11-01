from django.contrib import admin

from .models import Cancha, CanchaPrecios, HorariosCancha

admin.site.register(Cancha)
admin.site.register(CanchaPrecios)
admin.site.register(HorariosCancha)
