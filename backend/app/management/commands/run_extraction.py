from django.core.management.base import BaseCommand
from django.conf import settings
import json

from app.extraction.extraction_flow import run_extraction_flow


class Command(BaseCommand):
    help = 'Executa o processo de extração de texto para um arquivo de exemplo.'

    def add_arguments(self, parser):
        """Argumentos opcionais, como o nome do arquivo."""
        parser.add_argument('filename', nargs='?', type=str, help='Nome do arquivo na pasta samples.')

    def handle(self, *args, **options):
        """Lógica do comando a ser executado.
        """
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
            result_dict = run_extraction_flow(file_path)
            
            json_result = json.dumps(result_dict, indent=4, ensure_ascii=False)

            self.stdout.write(json_result)

        except Exception as e:
            self.stdout.write(self.style.ERROR(f"Ocorreu um erro: {e}"))
            