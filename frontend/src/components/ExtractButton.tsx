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
      className="btn-secondary flex items-center justify-center min-w-[100px]"
    >
      {isExtracting ? (
        <>
          <Loader2 className="mr-2 h-2 w-2 animate-spin" />
          Extraindo...
        </>
      ) : (
        'Extrair'
      )}
    </button>
  );
}
