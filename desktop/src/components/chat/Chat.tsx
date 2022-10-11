import React from 'react';
import { Container, Box, Stack, Flex } from '@chakra-ui/react';
import Message from './Message';
import ChatInput from './ChatInput';

function Chat() {
  return (
    <div>
      <Box m={4}>
        <Message
          username="Not me"
          message="Blah-blah-blah-blah-blah-blah-blah-blah-blah-blah-blah-blah-blah-blah-blah-blah"
        />
        <Message username="Me" message="blah-blah-blah" isSelf />
      </Box>
      <ChatInput />
    </div>
  );
}

export default Chat;
