import React from 'react';

import { Box, Container, FormControl, Heading } from '@chakra-ui/react';

import AuthForm from './AuthForm';

function Auth() {
  return (
    <div
      style={{
        position: 'absolute',
        top: '50%',
        left: '50%',
        transform: 'translate(-50%, -50%)',
      }}
    >
      <Box borderRadius="lg" borderWidth="1px" p="4">
        <Heading>Auth</Heading>
      </Box>
    </div>
  );
}

export default Auth;
