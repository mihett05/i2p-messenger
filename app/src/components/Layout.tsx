import React from 'react';
import { Box, Container, Flex, Grid, GridItem } from '@chakra-ui/react';

import Chats from './Chats';
import '../styles/Layout.css';

interface LayoutProps {
  children: React.ReactNode;
}

function Layout({ children }: LayoutProps) {
  return (
    <Flex>
      <Container maxW="30%" px={0}>
        <nav
          className="chats-container"
          style={{
            overflow: 'none',
            overflowY: 'scroll',
            height: '100vh',
          }}
        >
          <Chats />
        </nav>
      </Container>

      <Box flex="1">{children}</Box>
    </Flex>
  );
}

export default Layout;
