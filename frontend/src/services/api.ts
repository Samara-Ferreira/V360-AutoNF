import axios from 'axios';

const API_URL = 'http://127.0.0.1:8000/api/';

// Exporte o apiClient para ser usado diretamente
export const apiClient = axios.create({
  baseURL: API_URL,
});