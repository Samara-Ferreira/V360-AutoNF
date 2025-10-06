import { useState, useEffect, useRef } from 'react';
import { useNavigate } from 'react-router-dom';
import { apiClient } from '../services/api';
import { FileText, FileImage, FolderX } from 'lucide-react'; 
import { ExtractButton } from './ExtractButton';
import { TableRowSkeleton } from './TableRowSkeleton';

interface SampleFilesTableProps {
  externalLock?: boolean;
  onExtractingChange?: (extracting: boolean) => void;
}

export function SampleFilesTable({ externalLock = false, onExtractingChange }: SampleFilesTableProps) {
  const [files, setFiles] = useState<string[]>([]);
  const [isLoading, setIsLoading] = useState<boolean>(true);
  const [extractingFile, setExtractingFile] = useState<string | null>(null);
  const extractingRef = useRef<string | null>(null);
  const navigate = useNavigate();

  useEffect(() => {
    const fetchFiles = async () => {
      try {
        const response = await apiClient.get<string[]>('/sample-files/');
        setFiles(response.data);
      } catch (error) {
        console.error("Falha ao buscar arquivos de exemplo.", error);
      } finally {
        setIsLoading(false);
      }
    };
    fetchFiles();
  }, []);

  const handleExtract = async (filename: string) => {
    if (extractingRef.current || externalLock) return;
    extractingRef.current = filename;
    setExtractingFile(filename);
    onExtractingChange?.(true);
    try {
      const response = await apiClient.post('/data-entries/', { filename });
      navigate(`/results/${response.data.id}`);
    } catch (error) {
      console.error("Falha ao iniciar extração.", error);
      alert("Ocorreu um erro ao extrair o arquivo.");
    } finally {
      extractingRef.current = null;
      setExtractingFile(null);
      onExtractingChange?.(false);
    }
  };

  const getFileIcon = (filename: string) => {
    const extension = filename.split('.').pop()?.toLowerCase();
    if (extension === 'pdf') {
      return (
        <>
          <FileText className="h-4 w-4 text-[#777777]" strokeWidth={1.5} aria-hidden />
          <span className="sr-only">PDF</span>
        </>
      );
    }
    if (['png', 'jpg', 'jpeg'].includes(extension || '')) {
      return (
        <>
          <FileImage className="h-4 w-4 text-[#777777]" strokeWidth={1.5} aria-hidden />
          <span className="sr-only">Imagem</span>
        </>
      );
    }
    return null;
  };

  return (
    <div className="bg-slate-800 p-6 rounded-lg shadow-lg">
      <h2 className="text-table-title mb-4">
        Escolha um arquivo de exemplo
      </h2>
      <div className="overflow-x-auto">
        <table className="w-full text-left border-separate" style={{ borderSpacing: '0 0.35rem' }}>
          <thead className="border-b border-slate-600">
            <tr>
              <th className="pl-3 pr-4 py-4 text-left whitespace-nowrap text-subtext-highlight">Nome do Arquivo</th>
              <th className="px-4 py-4 text-right whitespace-nowrap text-subtext-highlight"></th>
            </tr>
          </thead>
          <tbody>
            {isLoading ? (
              <>
                {/* Mostra 3 linhas de skeleton enquanto carrega */}
                <TableRowSkeleton />
                <TableRowSkeleton />
                <TableRowSkeleton />
              </>
            ) : files.length === 0 ? (
              <tr>
                <td colSpan={2} className="text-center p-8 text-slate-400">
                  <div className="flex flex-col items-center gap-2">
                    <FolderX className="text-table" />
                    <span>Nenhum arquivo de exemplo encontrado.</span>
                  </div>
                </td>
              </tr>
            ) : (
              files.map((file) => (
                <tr key={file} className="hover:drop-shadow-sm transition-all">
                  <td className="p-0 align-middle">
                    <div className="bg-slate-700/30 rounded-md px-4 py-3 flex items-center gap-3">
                      {getFileIcon(file)}
                      <span className="text-body-description font-medium text-white truncate">{file}</span>
                    </div>
                  </td>
                  <td className="p-0 align-middle">
                    <div className="bg-slate-700/30 rounded-md pl-4 pr-8 py-1 flex justify-end items-center">
                      <ExtractButton 
                        onClick={() => handleExtract(file)}
                        isExtracting={extractingFile === file}
                        globalLock={!!extractingFile || externalLock}
                      />
                    </div>
                  </td>
                </tr>
              ))
            )}
          </tbody>
        </table>
      </div>
    </div>
  );
}