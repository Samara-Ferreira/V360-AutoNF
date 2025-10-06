import { Loader2 } from 'lucide-react';

interface ExtractButtonProps {
  isExtracting: boolean;
  onClick: () => void;
  globalLock?: boolean;
}

export function ExtractButton({ isExtracting, onClick, globalLock = false }: ExtractButtonProps) {
  return (
    <button
      onClick={onClick}
      disabled={isExtracting || globalLock}
      className="btn-secondary flex items-center justify-center"
    >
      {isExtracting ? (
        <>
          <Loader2 className="mr-2 h-4 w-4 animate-spin" />
          Extraindo...
        </>
      ) : (
        'Extrair'
      )}
    </button>
  );
}