import MessageList from './MessageList';
import MessageInput from './MessageInput';

const ChatWindow = ({ conversation, messages, onSendMessage, loading }) => {
  const isGroup = conversation?.is_group;
  const members = conversation?.members || [];

  if (!conversation) {
    return (
      <div className="flex-1 flex items-center justify-center bg-slate-50 dark:bg-slate-900/50">
        <div className="text-center">
          <div className="w-16 h-16 mx-auto mb-4 rounded-full bg-slate-100 dark:bg-slate-700 flex items-center justify-center">
            <svg className="w-8 h-8 text-slate-400" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M8 12h.01M12 12h.01M16 12h.01M21 12c0 4.418-4.03 8-9 8a9.863 9.863 0 01-4.255-.949L3 20l1.395-3.72C3.512 15.042 3 13.574 3 12c0-4.418 4.03-8 9-8s9 3.582 9 8z" />
            </svg>
          </div>
          <p className="text-slate-500 dark:text-slate-400 text-sm">Select a conversation to start chatting</p>
        </div>
      </div>
    );
  }

  return (
    <div className="flex-1 flex flex-col">
      <div className="px-4 py-3 border-b border-slate-200 dark:border-slate-700 bg-white dark:bg-slate-800 flex items-center gap-3">
        <div className="w-9 h-9 rounded-full bg-primary-100 dark:bg-primary-800 flex items-center justify-center flex-shrink-0">
          {isGroup ? (
            <svg className="w-4 h-4 text-primary-600 dark:text-primary-300" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M17 20h5v-2a3 3 0 00-5.356-1.857M17 20H7m10 0v-2c0-.656-.126-1.283-.356-1.857M7 20H2v-2a3 3 0 015.356-1.857M7 20v-2c0-.656.126-1.283.356-1.857m0 0a5.002 5.002 0 019.288 0M15 7a3 3 0 11-6 0 3 3 0 016 0z" />
            </svg>
          ) : (
            <span className="text-sm font-semibold text-primary-600 dark:text-primary-300">
              {conversation.display_name?.[0]?.toUpperCase() || '?'}
            </span>
          )}
        </div>
        <div className="flex-1 min-w-0">
          <p className="text-sm font-semibold text-slate-900 dark:text-slate-100 truncate">
            {conversation.display_name}
          </p>
          {isGroup && members.length > 0 && (
            <p className="text-xs text-slate-500 dark:text-slate-400 truncate">
              {members.map((m) => m.full_name || m.email).join(', ')}
            </p>
          )}
        </div>
      </div>

      <MessageList messages={messages} members={members} conversation={conversation} />

      <MessageInput onSend={onSendMessage} disabled={false} />
    </div>
  );
};

export default ChatWindow;
