import React from 'react';
import { Box, Input, Textarea } from '@chakra-ui/react';
import '../../styles/ChatInput.css';

function ChatInput() {
  return (
    <Box className="chat-input-container" bgColor="primary.100">
      <Textarea rows={1} w="inherit" />
    </Box>
  );
}

export default ChatInput;
