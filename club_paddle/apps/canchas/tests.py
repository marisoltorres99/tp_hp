from django.test import TestCase

from apps.canchas.models import Cancha


class Test1:
    def __init__(self):
        cancha = Cancha(numero=1, valoracion=3.8)
        cancha.save()

        cancha = Cancha(numero=2, valoracion=3.1)
        cancha.save()

        cancha = Cancha(numero=3)
        cancha.save()
