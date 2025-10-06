import { useState, useRef } from 'react';
import type { ChangeEvent, DragEvent } from 'react';
import { UploadCloud, File, X } from 'lucide-react';

interface FileDropZoneProps {
  selectedFile: File | null;
  setSelectedFile: (file: File | null) => void;
  disableSelect?: boolean;
}

export function FileDropZone({ selectedFile, setSelectedFile, disableSelect = false }: FileDropZoneProps) {
  const [isDragging, setIsDragging] = useState(false);
  const fileInputRef = useRef<HTMLInputElement>(null);

  const handleFileChange = (event: ChangeEvent<HTMLInputElement>) => {
    if (event.target.files && event.target.files[0]) {
      setSelectedFile(event.target.files[0]);
    }
  };

  const handleDragEvents = (event: DragEvent<HTMLDivElement>, dragging: boolean) => {
    event.preventDefault();
    event.stopPropagation();
    setIsDragging(dragging);
  };

  const handleDrop = (event: DragEvent<HTMLDivElement>) => {
    handleDragEvents(event, false);
    if (event.dataTransfer.files && event.dataTransfer.files[0]) {
      setSelectedFile(event.dataTransfer.files[0]);
    }
  };

  const triggerFileSelect = () => {
    if (disableSelect) return;
    fileInputRef.current?.click();
  };

  if (selectedFile) {
    return (
      <div className="bg-slate-700 p-4 rounded-lg flex items-center justify-between">
        <div className="text-body-description flex items-center gap-3">
          <File className="h-6 w-6 text-cyan-400" stroke="#777777" strokeWidth={1.4} />
          <span className="text-sm text-white font-medium">{selectedFile.name}</span>
        </div>
        <button
          onClick={() => setSelectedFile(null)}
          aria-label="Remover arquivo"
          className="items-center justify-center bg-[#bd4141] hover:bg-[#8a1c1c] transition-colors"
          title="Remover arquivo"
        >
          <span className="sr-only">Remover arquivo</span>
          <X className="h-5 w-5 text-white" stroke="#ffffff" strokeWidth={1.4} />
        </button>
      </div>
    );
  }

  return (
    <div
      onDragEnter={(e) => { if (!disableSelect) handleDragEvents(e, true); }}
      onDragLeave={(e) => handleDragEvents(e, false)}
      onDragOver={(e) => e.preventDefault()}
      onDrop={(e) => { if (!disableSelect) handleDrop(e); }}
      onClick={triggerFileSelect}
  className={`border border-b-0 border-dashed rounded-lg p-3 text-center transition-colors duration-200
        ${disableSelect ? 'opacity-60 cursor-not-allowed' : 'cursor-pointer'} ${isDragging ? 'border-cyan-400 bg-slate-700/50' : 'border-[#777777] hover:border-[#646464] border-2'}`}
    >
      <input 
        ref={fileInputRef}
        type="file" 
        onChange={handleFileChange}
        accept=".pdf,.png,.jpg,.jpeg"
        className="hidden"
      />
      <div className="flex flex-col items-center gap-1 text-slate-400">
        <UploadCloud className="h-10 w-10" stroke="#777777" strokeWidth={1.4} />
        <p className="font-semibold font-inter text-sm">Arraste e solte o arquivo aqui ou clique para selecionar</p>
        <p className="font-inter text-xs mt-1">(PDF, PNG, JPG ou JPEG)</p>
      </div>
    </div>
  );
}