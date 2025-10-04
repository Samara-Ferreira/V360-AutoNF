from django.core.management.base import BaseCommand
from django.conf import settings
from api_rest.services import run_extraction_flow # Importa nossa lógica

class Command(BaseCommand):
    help = 'Executa o processo de extração de texto para um arquivo de exemplo.'

    def add_arguments(self, parser):
        # Argumento opcional para especificar o arquivo
        parser.add_argument('filename', nargs='?', type=str, help='Nome do arquivo na pasta samples.')

    def handle(self, *args, **options):
        filename = options['filename']
        
        if not filename:
            self.stdout.write(self.style.ERROR("Por favor, forneça um nome de arquivo da pasta 'samples'."))
            return

        file_path = settings.SAMPLES_DIR / filename
        
        if not file_path.exists():
            self.stdout.write(self.style.ERROR(f"Arquivo '{filename}' não encontrado em '{settings.SAMPLES_DIR}'."))
            return

        self.stdout.write(self.style.SUCCESS(f"Iniciando extração para o arquivo: {file_path}"))
        
        try:
            json_result = run_extraction_flow(file_path)
            self.stdout.write("\n--- RESULTADO DA EXTRAÇÃO ---\n")
            self.stdout.write(json_result)

        except Exception as e:
            self.stdout.write(self.style.ERROR(f"Ocorreu um erro: {e}"))