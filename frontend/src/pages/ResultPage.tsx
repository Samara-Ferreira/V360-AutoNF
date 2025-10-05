import { useState, useEffect } from 'react';
import { useParams, Link } from 'react-router-dom';
import { apiClient } from '../services/api';
import type { DataEntry } from '../types/DataEntry';

function ResultPage() {
  const { id } = useParams<{ id: string }>(); // Pega o ID da URL
  const [entry, setEntry] = useState<DataEntry | null>(null);
  const [loading, setLoading] = useState<boolean>(true);

  useEffect(() => {
    if (!id) return;
    const fetchResult = async () => {
      try {
        // Idealmente, a API teria um endpoint /data-entries/${id}/
        // Por agora, vamos buscar todos e filtrar
        const response = await apiClient.get<DataEntry[]>('/data-entries/');
        const foundEntry = response.data.find(e => e.id === parseInt(id));
        setEntry(foundEntry || null);
      } catch (error) {
        console.error("Falha ao buscar resultado.", error);
      } finally {
        setLoading(false);
      }
    };
    fetchResult();
  }, [id]);

  if (loading) return <p>Carregando resultado...</p>;

  if (!entry) return <p>Resultado não encontrado.</p>;

  return (
    <div>
      <h1 className="text-4xl font-bold mb-6 text-cyan-400">Resultado da Extração</h1>
      <div className="bg-slate-800 p-6 rounded-lg">
        <p className="mb-2"><strong className="text-slate-400">Arquivo:</strong> {entry.filename}</p>
        <p className="mb-2"><strong className="text-slate-400">CNPJ do Prestador:</strong> {entry.cnpj_prestador || 'Não encontrado'}</p>
        <p><strong className="text-slate-400">Nome do Prestador:</strong> {entry.nome_prestador || 'Não encontrado'}</p>
      </div>
      <Link to="/" className="mt-6 inline-block bg-cyan-600 hover:bg-cyan-700 text-white font-bold py-2 px-4 rounded">
        &larr; Voltar para a Lista
      </Link>
    </div>
  );
}

export default ResultPage;