import { Routes, Route } from 'react-router-dom';
import FileListPage from './pages/FileListPage';
import ResultPage from './pages/ResultPage';
import './App.css';

function App() {
  return (
    <div className="bg-slate-900 text-white min-h-screen">
      <main className="container mx-auto p-4">
        <Routes>
          {/* Rota para a página inicial */}
          <Route path="/" element={<FileListPage />} />
          
          {/* Rota para a página de resultados, com um ID dinâmico */}
          <Route path="/results/:id" element={<ResultPage />} />
        </Routes>
      </main>
    </div>
  );
}

export default App;