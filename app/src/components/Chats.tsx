import React from 'react';
import { Box } from '@chakra-ui/react';
import ChatItem from './ChatItem';

function Chats() {
  return (
    <div>
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
    </div>
  );
}

export default Chats;
