import { useState, useEffect } from 'react';
import { useParams, Link } from 'react-router-dom';
import { apiClient } from '../services/api';
import type { DataEntry } from '../types/DataEntry';

function ResultPage() {
  const { id } = useParams<{ id: string }>(); 
  const [entry, setEntry] = useState<DataEntry | null>(null);
  const [loading, setLoading] = useState<boolean>(true);

  useEffect(() => {
    if (!id) return;
    const fetchResult = async () => {
      try {
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
    <div className="py-8">
      <header className="text-center mb-8">
        <h1 className="text-title-logo text-3xl">Resultado da Extração</h1>
        <p className="text-accent-highlight text-slate-500 mt-2 max-w-2xl mx-auto">Detalhes extraídos do documento</p>
      </header>

      <main className="max-w-3xl mx-auto">
        <div className="bg-white rounded-lg shadow-md overflow-hidden">
          <div className="bg-slate-800">
            <div className="px-6 pb-6 mt-4 bg-slate-800">
              <div className="divide-y divide-[#777777] rounded-md overflow-hidden">
                <div className="flex items-center justify-between py-3">
                  <span className="text-body-description-large text-slate-400">Arquivo</span>
                  <span className="text-body-description-large text-slate-200">{entry.filename}</span>
                </div>
                <div className="flex items-center justify-between py-3">
                  <span className="text-body-description-large text-slate-400">CNPJ do Prestador</span>
                  <span className="text-body-description-large text-slate-200">{entry.cnpj_prestador || 'Não encontrado'}</span>
                </div>
                <div className="flex items-center justify-between py-3">
                  <span className="text-body-description-large text-slate-400">Nome do Prestador</span>
                  <span className="text-body-description-large text-slate-200">{entry.nome_prestador || 'Não encontrado'}</span>
                </div>
              </div>
            </div>
          </div>
          <div className="p-4 bg-white">
            <Link to="/" className="btn-primary btn-primary--light inline-block">
              &larr; Voltar para a página de envio
            </Link>
          </div>
        </div>
      </main>
    </div>
  );
}

export default ResultPage;
