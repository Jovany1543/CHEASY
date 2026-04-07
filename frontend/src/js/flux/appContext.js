import React, { createContext, useContext } from 'react';

import { useStoreState } from './store';

const AppContext = createContext(null);

export function StoreProvider({ children }) {
  const store = useStoreState();

  return <AppContext.Provider value={store}>{children}</AppContext.Provider>;
}

export function useStore() {
  const context = useContext(AppContext);

  if (!context) {
    throw new Error('useStore must be used inside StoreProvider');
  }

  return context;
}