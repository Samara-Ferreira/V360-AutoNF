from django.db import models

class DataEntry(models.Model):
    filename = models.CharField(max_length=255)
    cnpj_prestador = models.CharField(max_length=18, blank=True, null=True)
    nome_prestador = models.CharField(max_length=255, blank=True, null=True)
    extracted_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.filename} - {self.cnpj_prestador}"
