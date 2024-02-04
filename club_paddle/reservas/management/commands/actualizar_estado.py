from django.core.management.base import BaseCommand
from django.utils import timezone

from reservas.models import Reserva


class Command(BaseCommand):
    help = "actualiza estado de reserva y estado de pagada"

    def handle(self, *args, **options):

        reservas = Reserva.objects.filter(
            estado="P", fecha_hora_reserva__lte=timezone.datetime.now()
        )
        self.stdout.write(str(reservas))
        reservas.update(estado="F", pagada=True)
