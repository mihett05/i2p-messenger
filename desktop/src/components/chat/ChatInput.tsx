import React, { useEffect, useState } from 'react';
import _ from 'lodash';
import { Box, Button, Center, Flex, IconButton, Input, Textarea, useTheme } from '@chakra-ui/react';
import { ArrowForwardIcon } from '@chakra-ui/icons';
import '../../styles/ChatInput.css';

function ChatInput() {
  const theme = useTheme();
  const [rows, setRows] = useState(1);
  const [text, setText] = useState('');

  useEffect(() => {
    const result = _.clamp(
      text
        .split('\n')
        .map((v) => Math.ceil((v.length + 1) / 128))
        .reduce((prev, curr) => prev + curr, 0),
      1,
      10,
    );
    setRows(result);
  }, [text]);

  return (
    <Box className="chat-input-container" bgColor="primary.100" w="75vw">
      <Flex>
        <Textarea
          className="chat-input"
          rows={rows}
          w="70vw"
          resize="none"
          variant="unstyled"
          _selection={{
            backgroundColor: theme.colors.telegram[500],
          }}
          value={text}
          onChange={(v) => setText(v.target.value)}
        />
        <Center>
          <IconButton aria-label="Send" icon={<ArrowForwardIcon />} size="sm" bgColor="primary.100" w="5vw" />
        </Center>
      </Flex>
    </Box>
  );
}

export default ChatInput;
