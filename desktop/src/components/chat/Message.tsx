import React from 'react';
import { Box, Flex } from '@chakra-ui/react';

import '../../styles/Message.css';

interface MessageProps {
  isSelf?: boolean;
  username: string;
  message: string;
}

function Message({ isSelf, username, message }: MessageProps) {
  return (
    <Flex justify={isSelf ? 'right' : 'left'}>
      <Box bgColor={isSelf ? 'telegram.500' : 'telegram.900'} my={1} px={1} maxW="45%">
        <p className="message-username">
          <b>{username}</b>
        </p>
        <p className="message-text">{message}</p>
        <p className="message-time">17:00 12.03.2022</p>
      </Box>
    </Flex>
  );
}

export default Message;
