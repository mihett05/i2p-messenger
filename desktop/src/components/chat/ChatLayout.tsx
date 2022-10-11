import React from 'react';
import { Box, Container, Flex, Grid, GridItem } from '@chakra-ui/react';

import ChatList from './ChatList';
import '../../styles/Layout.css';

interface LayoutProps {
  children: React.ReactNode;
}

function ChatLayout({ children }: LayoutProps) {
  return (
    <Flex>
      <Container maxW="25%" w="25%" px={0}>
        <nav
          className="chats-container"
          style={{
            overflow: 'none',
            overflowY: 'scroll',
            height: '100vh',
          }}
        >
          <ChatList />
        </nav>
      </Container>

      <Box flex="1">{children}</Box>
    </Flex>
  );
}

export default ChatLayout;
