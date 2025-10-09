export interface DataEntry {
  id: number;
  filename: string;
  cnpj_prestador: string | null;
  nome_prestador: string | null;
  email_prestador: string | null;
  telefone_prestador: string | null;
  extracted_at: string; 
}