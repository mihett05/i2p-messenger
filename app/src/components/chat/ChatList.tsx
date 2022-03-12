import React from 'react';
import { Box } from '@chakra-ui/react';
import ChatItem from './ChatItem';

function ChatList() {
  return (
    <Box bgColor="primary.100">
      {Array.from(Array(100)).map((_, i) => (
        <Box
          key={i}
          w="100%"
          style={{
            textOverflow: 'ellipsis',
            whiteSpace: 'nowrap',
            overflow: 'hidden',
          }}
          py={2}
        >
          <ChatItem name={`User ${i}`} lastMessage={`Blah-blah-blah-blah-blah`} />
        </Box>
      ))}
    </Box>
  );
}

export default ChatList;
