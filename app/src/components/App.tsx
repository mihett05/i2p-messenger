import React, { useEffect, useState } from 'react';
import { createAccount, signInAccount } from '../api/account';
import Storage from '../storage/storage';
import Layout from './Layout';
import Chat from './chat/Chat';

function App() {
  useEffect(() => {
    console.log(Storage.getItem('token'));
    (async () => {
      const result = await signInAccount('123', '123');
      if (result !== null) Storage.setItem('token', result);
    })();
  }, []);
  return (
    <Layout>
      <Chat />
    </Layout>
  );
}

export default App;
