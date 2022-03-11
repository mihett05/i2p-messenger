import React, { useEffect, useState } from 'react';
import { createAccount, signInAccount } from '../api/account';
import Layout from './Layout';

function App() {
  useEffect(() => {
    (async () => {
      console.log(await signInAccount('123', '123'));
    })();
  }, []);
  return <Layout>123</Layout>;
}

export default App;
