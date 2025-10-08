import { useState } from 'react';
import { FileUploadForm } from '../components/FileUploadForm';
import { SampleFilesTable } from '../components/SampleFilesTable';
import logo from '../assets/logo.png';

function FileListPage() {
  const [uploadInProgress, setUploadInProgress] = useState(false);
  const [extractInProgress, setExtractInProgress] = useState(false);

  return (
    <div className="py-8">
      
      <header className="text-center mb-16">
        
        <img src={logo} 
        alt="AutoNF" 
        className="mx-auto h-[180px] w-auto" />

        <p className="text-accent-highlight mt-2">
          Automação de Extração de Dados de Documentos Fiscais
        </p>
      </header>

  <div className="grid grid-cols-1 lg:grid-cols-5 gap-8 items-start">
        
        <div className="lg:col-span-2">
          <FileUploadForm
            onUploadingChange={(v) => setUploadInProgress(v)}
            externalExtracting={extractInProgress}
          />
        </div>
        
        <div className="lg:col-span-3">
          <SampleFilesTable
            externalLock={uploadInProgress}
            onExtractingChange={(v) => setExtractInProgress(v)}
          />
        </div>

      </div>
      
    </div>
  );
}

export default FileListPage;
