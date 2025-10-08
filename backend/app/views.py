import os
from django.conf import settings
from django.core.files.storage import default_storage
from django.core.files.base import ContentFile

from rest_framework.response import Response
from rest_framework import status
from rest_framework.views import APIView

from .models import DataEntry
from .serializers import DataEntrySerializer
from .extraction.extraction_flow import run_extraction_flow


class DataEntryView(APIView):
    """
    Classe de API para listar e criar entradas de dados.
    1. GET: Lista todas as entradas de dados.
    2. POST: Recebe o nome de um arquivo, processa-o e cria uma nova entrada.
    """
    
    def get(self, request):
        """Lida com requisições GET para listar todas as entradas."""
        entries = DataEntry.objects.all().order_by('-extracted_at')
        serializer = DataEntrySerializer(entries, many=True)
        return Response(serializer.data)

    def post(self, request):
        """Lida com requisições POST para extrair dados de um novo arquivo."""
        filename = request.data.get('filename')

        if not filename:
            return Response(
                {"error": "O campo 'filename' é obrigatório."},
                status=status.HTTP_400_BAD_REQUEST
            )

        file_path = settings.SAMPLES_DIR / filename
        
        if not file_path.exists():
            return Response(
                {"error": f"Arquivo '{filename}' não encontrado."},
                status=status.HTTP_404_NOT_FOUND
            )
            
        try:
            extracted_data = run_extraction_flow(file_path)
            
            new_entry = DataEntry.objects.create(
                filename=filename,
                cnpj_prestador=extracted_data.get('cnpj_prestador'),
                nome_prestador=extracted_data.get('nome_prestador'),
                email_prestador=extracted_data.get('email_prestador'),
                telefone_prestador=extracted_data.get('telefone_prestador'),
            )
            
            serializer = DataEntrySerializer(new_entry)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
            
        except Exception as e:
            return Response(
                {"error": f"Falha na extração: {str(e)}"},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )
        

class SampleFilesView(APIView):
    """
    Classe de API para listar arquivos de amostra disponíveis.
    """
    def get(self, request):
        try:
            files = os.listdir(settings.SAMPLES_DIR)

            # is_file() para garantir que são arquivos, não diretórios
            file_list = [f for f in files if (settings.SAMPLES_DIR / f).is_file()]
            return Response(file_list, status=status.HTTP_200_OK)
        except FileNotFoundError:
            return Response({"error": "Diretório 'samples' não encontrado."}, status=status.HTTP_404_NOT_FOUND)


class FileUploadView(APIView):
    """
    Classe de API para upload de arquivos.
    1. POST: Recebe um arquivo, processa-o e cria uma nova entrada.
    2. Salva o arquivo na pasta 'samples' para referência futura.
    """
    def post(self, request):
        file_obj = request.FILES.get('file')

        if not file_obj:
            return Response({"error": "Nenhum arquivo enviado."}, status=status.HTTP_400_BAD_REQUEST)

        file_path_on_server = default_storage.save(f"samples/{file_obj.name}", ContentFile(file_obj.read()))
        full_path = settings.PROJECT_ROOT / file_path_on_server
        
        try:
            extracted_data = run_extraction_flow(full_path)
            
            new_entry = DataEntry.objects.create(
                filename=file_obj.name,
                cnpj_prestador=extracted_data.get('cnpj_prestador'),
                nome_prestador=extracted_data.get('nome_prestador'),
                email_prestador=extracted_data.get('email_prestador'),
                telefone_prestador=extracted_data.get('telefone_prestador'),
            )
            
            serializer = DataEntrySerializer(new_entry)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
            
        except Exception as e:
            return Response(
                {"error": f"Falha na extração: {str(e)}"},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )

        except Exception as e:
            default_storage.delete(file_path_on_server)
            return Response(
                {"error": f"Falha na extração do arquivo enviado: {str(e)}"},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )
        