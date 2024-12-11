import React from 'react';
import ReactDOM from 'react-dom/client';
import { Layout } from './components/Layout';
import './index.css';

// Initialize React root
const rootElement = document.getElementById('root');
if (!rootElement) {
  throw new Error('Root element not found in document');
}

ReactDOM.createRoot(rootElement).render(
  <React.StrictMode>
    <Layout />
  </React.StrictMode>
);