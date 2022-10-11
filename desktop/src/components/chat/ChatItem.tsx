import React from 'react';

interface ChatItemProps {
  name: string;
  lastMessage: string;
}

function ChatItem({ name, lastMessage }: ChatItemProps) {
  return (
    <div className="chat-item">
      <b>{name}</b>
      <p>{lastMessage}</p>
    </div>
  );
}

export default ChatItem;
