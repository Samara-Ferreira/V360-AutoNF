import { Loader2 } from 'lucide-react';

interface SubmitButtonProps {
  isUploading: boolean;
  isFileSelected: boolean;
}

export function SubmitButton({ isUploading, isFileSelected }: SubmitButtonProps) {
  return (
    <button 
      type="submit" 
      disabled={!isFileSelected || isUploading}
      className="btn-primary w-full flex items-center justify-center"
    >
      {isUploading ? (
        <>
          <Loader2 className="mr-2 h-5 w-5 animate-spin" />
          Enviando...
        </>
      ) : (
        'Enviar e Extrair'
      )}
    </button>
  );
}