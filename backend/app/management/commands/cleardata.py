from django.core.management.base import BaseCommand
from app.models import DataEntry

class Command(BaseCommand):
    help = 'Apaga todos os registros da tabela DataEntry.'

    def handle(self, *args, **options):
        # Executa o comando para deletar todos os objetos
        count, _ = DataEntry.objects.all().delete()
        
        # Exibe uma mensagem de sucesso no terminal
        self.stdout.write(self.style.SUCCESS(f'Sucesso! {count} registros foram apagados da tabela DataEntry.'))
        