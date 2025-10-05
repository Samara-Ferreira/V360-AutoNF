from fileinput import filename
from django.shortcuts import render
from rest_framework.decorators import api_view
from rest_framework.response import Response
from .models import DataEntry
from .serializers import DataEntrySerializer
from rest_framework import status
from rest_framework.views import APIView
from .services import run_extraction_flow
from django.conf import settings
import os
from django.core.files.storage import default_storage
from django.core.files.base import ContentFile


# @api_view(['GET'])
# def get_data_entries(request):
#     if request.method == 'GET':
#         entries = DataEntry.objects.all()
#         serializer = DataEntrySerializer(entries, many=True)
#         return Response(serializer.data)
#     return Response(status=status.HTTP_400_BAD_REQUEST)

class DataEntryView(APIView):
    """
    API para listar e criar entradas de dados extraídos.
    GET: Lista todas as extrações salvas.
    POST: Inicia uma nova extração e salva o resultado.
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
            # Chama nossa função de serviço para fazer o trabalho pesado
            extracted_data = run_extraction_flow(file_path)
            
            # Cria uma nova entrada no banco de dados com os resultados
            new_entry = DataEntry.objects.create(
                filename=filename,
                cnpj_prestador=extracted_data.get('cnpj_prestador'),
                nome_prestador=extracted_data.get('nome_prestador'),
            )
            
            # Serializa o objeto recém-criado para a resposta
            serializer = DataEntrySerializer(new_entry)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
            
        except Exception as e:
            # Se algo der errado durante a extração
            return Response(
                {"error": f"Falha na extração: {str(e)}"},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )
        

class SampleFilesView(APIView):
    """
    API para listar os arquivos disponíveis na pasta 'samples'.
    """
    def get(self, request):
        try:
            files = os.listdir(settings.SAMPLES_DIR)
            # Filtra para garantir que estamos enviando apenas arquivos, não pastas
            file_list = [f for f in files if (settings.SAMPLES_DIR / f).is_file()]
            return Response(file_list, status=status.HTTP_200_OK)
        except FileNotFoundError:
            return Response({"error": "Diretório 'samples' não encontrado."}, status=status.HTTP_404_NOT_FOUND)


class FileUploadView(APIView):
    """
    API para receber um arquivo via upload, salvá-lo, processá-lo e
    retornar os dados extraídos.
    """
    def post(self, request):
        # Pega o arquivo da requisição
        file_obj = request.FILES.get('file')

        if not file_obj:
            return Response({"error": "Nenhum arquivo enviado."}, status=status.HTTP_400_BAD_REQUEST)

        # Salva o arquivo na nossa pasta 'uploads'
        file_path_on_server = default_storage.save(f"samples/{file_obj.name}", ContentFile(file_obj.read()))
        full_path = settings.PROJECT_ROOT / file_path_on_server
        
        try:
            # Chama nossa mesma lógica de serviço, agora com o caminho do novo arquivo
            extracted_data = run_extraction_flow(full_path)
            
            new_entry = DataEntry.objects.create(
                filename=file_obj.name,
                cnpj_prestador=extracted_data.get('cnpj_prestador'),
                nome_prestador=extracted_data.get('nome_prestador'),
            )
            
            # Serializa o objeto recém-criado para a resposta
            serializer = DataEntrySerializer(new_entry)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
            
        except Exception as e:
            # Se algo der errado durante a extração
            return Response(
                {"error": f"Falha na extração: {str(e)}"},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )

        except Exception as e:
            # Limpeza em caso de erro
            default_storage.delete(file_path_on_server)
            return Response(
                {"error": f"Falha na extração do arquivo enviado: {str(e)}"},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )