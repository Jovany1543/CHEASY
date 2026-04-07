import React from 'react';
import ReactDOM from 'react-dom/client';
import { BrowserRouter } from 'react-router-dom';
import Layout from './js/Layout';
import { StoreProvider } from './js/flux/appContext';


const root = ReactDOM.createRoot(document.getElementById('root'));
root.render(
  <React.StrictMode>
    <StoreProvider>
      <BrowserRouter>
        <Layout />
      </BrowserRouter>
    </StoreProvider>
  </React.StrictMode>
);

