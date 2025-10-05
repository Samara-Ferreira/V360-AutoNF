import { useState, useEffect } from 'react';
import type { ChangeEvent, FormEvent } from 'react';
import { useNavigate } from 'react-router-dom';
import { apiClient } from '../services/api';

function FileListPage() {
  // Estados para a lista de arquivos de exemplo
  const [files, setFiles] = useState<string[]>([]);
  const [listLoading, setListLoading] = useState<boolean>(true);
  const [extractingFile, setExtractingFile] = useState<string | null>(null);
  
  // Estados para a funcionalidade de upload
  const [selectedFile, setSelectedFile] = useState<File | null>(null);
  const [isUploading, setIsUploading] = useState<boolean>(false);
  
  const navigate = useNavigate();

  // Busca a lista de arquivos de exemplo do backend QUANDO a página carrega
  useEffect(() => {
    const fetchFiles = async () => {
      try {
        const response = await apiClient.get<string[]>('/sample-files/');
        setFiles(response.data);
      } catch (error) {
        console.error("Falha ao buscar arquivos de exemplo.", error);
      } finally {
        setListLoading(false);
      }
    };
    fetchFiles();
  }, []); // O array vazio [] garante que isso só rode uma vez

  // Função para extrair um arquivo da LISTA de exemplos
  const handleExtract = async (filename: string) => {
    setExtractingFile(filename);
    try {
      const response = await apiClient.post('/data-entries/', { filename });
      navigate(`/results/${response.data.id}`);
    } catch (error) {
      console.error("Falha ao iniciar extração.", error);
      alert("Ocorreu um erro ao extrair o arquivo.");
      setExtractingFile(null);
    }
  };

  // Função para lidar com a seleção de um arquivo no formulário de UPLOAD
  const handleFileChange = (event: ChangeEvent<HTMLInputElement>) => {
    if (event.target.files && event.target.files[0]) {
      setSelectedFile(event.target.files[0]);
    }
  };

  // Função para ENVIAR o arquivo selecionado
  const handleUpload = async (event: FormEvent<HTMLFormElement>) => {
    event.preventDefault();
    if (!selectedFile) {
      alert("Por favor, selecione um arquivo primeiro.");
      return;
    }
    setIsUploading(true);
    
    const formData = new FormData();
    formData.append('file', selectedFile);

    try {
      const response = await apiClient.post('/upload/', formData);
      navigate(`/results/${response.data.id}`);
    } catch (error) {
      console.error("Falha ao fazer upload do arquivo.", error);
      alert("Ocorreu um erro ao fazer o upload do arquivo.");
    } finally {
      setIsUploading(false);
    }
  };

  return (
    <div>
      <h1 className="text-4xl font-bold mb-6 text-cyan-400">Extrair Dados de Nota Fiscal</h1>
      
      {/* SEÇÃO DE UPLOAD */}
      <div className="bg-slate-800 p-6 rounded-lg mb-8">
        <h2 className="text-2xl font-bold mb-4">Faça upload de um arquivo</h2>
        <form onSubmit={handleUpload}>
          <input 
            type="file" 
            onChange={handleFileChange}
            accept=".pdf,.png,.jpg,.jpeg"
            className="mb-4 block w-full text-sm text-slate-400 file:mr-4 file:py-2 file:px-4 file:rounded-full file:border-0 file:text-sm file:font-semibold file:bg-cyan-50 file:text-cyan-700 hover:file:bg-cyan-100"
          />
          <button 
            type="submit" 
            disabled={!selectedFile || isUploading}
            className="bg-green-600 hover:bg-green-700 text-white font-bold py-2 px-4 rounded disabled:bg-slate-500"
          >
            {isUploading ? 'Enviando...' : 'Enviar e Extrair'}
          </button>
        </form>
      </div>
      
      {/* TABELA DE ARQUIVOS DE EXEMPLO */}
      <h2 className="text-2xl font-bold mb-4">Ou escolha um arquivo de exemplo</h2>
      {listLoading ? (
        <p>Carregando lista de arquivos...</p>
      ) : (
        <table className="w-full text-left">
          <thead className="bg-slate-800">
            <tr>
              <th className="p-4">Nome do Arquivo</th>
              <th className="p-4">Ação</th>
            </tr>
          </thead>
          <tbody>
            {files.map((file) => (
              <tr key={file} className="border-b border-slate-700 hover:bg-slate-800">
                <td className="p-4">{file}</td>
                <td className="p-4">
                  <button
                    onClick={() => handleExtract(file)}
                    disabled={extractingFile === file || isUploading}
                    className="bg-cyan-600 hover:bg-cyan-700 text-white font-bold py-2 px-4 rounded disabled:bg-slate-500"
                  >
                    {extractingFile === file ? 'Extraindo...' : 'Extrair Dados'}
                  </button>
                </td>
              </tr>
            ))}
          </tbody>
        </table>
      )}
    </div>
  );
}

export default FileListPage;