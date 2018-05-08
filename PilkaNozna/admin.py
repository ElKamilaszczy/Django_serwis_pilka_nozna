from django.contrib import admin
from .models import Liga
from .models import Pilkarz
from .models import Klub
from .models import Pozycja
from .models import Mecz
from .models import Statystyki_gracza
# Register your models here.

admin.site.register(Liga)
admin.site.register(Pilkarz)
admin.site.register(Klub)
admin.site.register(Pozycja)
admin.site.register(Mecz)
admin.site.register(Statystyki_gracza)
