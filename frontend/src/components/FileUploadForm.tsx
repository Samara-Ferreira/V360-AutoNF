import { useState } from 'react';
import type { FormEvent } from 'react';
import { useNavigate } from 'react-router-dom';
import { apiClient } from '../services/api';
import { FileDropZone } from './FileDropZone';
interface FileUploadFormProps {
  onUploadingChange?: (uploading: boolean) => void;
  externalExtracting?: boolean;
}
import { SubmitButton } from './SubmitButton';

export function FileUploadForm({ onUploadingChange, externalExtracting = false }: FileUploadFormProps) {
  const [selectedFile, setSelectedFile] = useState<File | null>(null);
  const [isUploading, setIsUploading] = useState<boolean>(false);
  const navigate = useNavigate();

  const handleUpload = async (event: FormEvent<HTMLFormElement>) => {
    event.preventDefault();
    if (!selectedFile) return;

  setIsUploading(true);
  onUploadingChange?.(true);
    const formData = new FormData();
    formData.append('file', selectedFile);

    try {
      const response = await apiClient.post('/upload/', formData);
      navigate(`/results/${response.data.id}`);
    } catch (error) {
      console.error("Falha ao fazer upload do arquivo.", error);
      alert("Ocorreu um erro ao fazer o upload do arquivo.");
      setIsUploading(false);
      onUploadingChange?.(false);
    }
  };

  return (
  <div className="bg-white p-6 py-1 px-1 rounded-lg border border-[#404040] border-b-0 border-l-0 border-r-0 shadow-sm h-full">
      
      <h2 className="text-table-title mb-4">
        Faça upload de um arquivo
      </h2>

      <form onSubmit={handleUpload} className="space-y-8">
        <FileDropZone selectedFile={selectedFile} setSelectedFile={setSelectedFile} disableSelect={isUploading || externalExtracting} />
        <SubmitButton isUploading={isUploading} isFileSelected={!!selectedFile} />
      </form>
    </div>
  );
}
