import React, { useEffect, useState } from 'react';
import { createAccount, signInAccount } from '../api/account';
import Storage from '../storage/storage';

import Auth from './auth/Auth';

import ChatLayout from './chat/ChatLayout';
import Chat from './chat/Chat';

function App() {
  // useEffect(() => {
  //   console.log(Storage.getItem('token'));
  //   (async () => {
  //     const result = await signInAccount('123', '123');
  //     console.log(result);
  //     if (result !== null) Storage.setItem('token', result);
  //   })();
  // }, []);

  // return (
  //   <div
  //     style={{
  //       height: '100vh',
  //     }}
  //   >
  //     <Auth />
  //   </div>
  // );

  return (
    <ChatLayout>
      <Chat />
    </ChatLayout>
  );
}

export default App;
