import { useState } from 'react';
import CreateChatDialog from './CreateChatDialog';

const ConversationList = ({ conversations, activeId, onSelect, onConversationCreated }) => {
  const [showCreate, setShowCreate] = useState(false);
  const [search, setSearch] = useState('');

  const filtered = conversations.filter((c) => {
    const name = c.display_name?.toLowerCase() || '';
    return name.includes(search.toLowerCase());
  });

  return (
    <>
      <div className="flex flex-col h-full">
        <div className="px-4 py-3 border-b border-slate-200 dark:border-slate-700">
          <div className="flex items-center justify-between mb-3">
            <h2 className="text-lg font-semibold text-slate-900 dark:text-slate-100">Chats</h2>
            <button
              onClick={() => setShowCreate(true)}
              className="p-1.5 rounded-lg text-slate-500 hover:text-primary-500 hover:bg-slate-100 dark:hover:bg-slate-700 transition-colors"
              title="New conversation"
            >
              <svg className="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M12 4v16m8-8H4" />
              </svg>
            </button>
          </div>
          <input
            type="text"
            placeholder="Search conversations..."
            value={search}
            onChange={(e) => setSearch(e.target.value)}
            className="w-full px-3 py-2 rounded-lg bg-slate-50 dark:bg-slate-700 border border-slate-200 dark:border-slate-600 text-sm text-slate-900 dark:text-slate-100 placeholder-slate-400 focus:outline-none focus:ring-2 focus:ring-primary-400"
          />
        </div>

        <div className="flex-1 overflow-y-auto">
          {filtered.length === 0 ? (
            <div className="px-4 py-8 text-center text-sm text-slate-500 dark:text-slate-400">
              No conversations yet. Click + to start one.
            </div>
          ) : (
            filtered.map((conversation) => (
              <button
                key={conversation.id}
                onClick={() => onSelect(conversation.id)}
                className={`w-full px-4 py-3 flex items-center gap-3 hover:bg-slate-50 dark:hover:bg-slate-700/50 transition-colors text-left ${
                  activeId === conversation.id
                    ? 'bg-primary-50 dark:bg-primary-900/20 border-l-2 border-primary-500'
                    : 'border-l-2 border-transparent'
                }`}
              >
                <div className="w-10 h-10 rounded-full bg-primary-100 dark:bg-primary-800 flex items-center justify-center flex-shrink-0">
                  {conversation.is_group ? (
                    <svg className="w-5 h-5 text-primary-600 dark:text-primary-300" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                      <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M17 20h5v-2a3 3 0 00-5.356-1.857M17 20H7m10 0v-2c0-.656-.126-1.283-.356-1.857M7 20H2v-2a3 3 0 015.356-1.857M7 20v-2c0-.656.126-1.283.356-1.857m0 0a5.002 5.002 0 019.288 0M15 7a3 3 0 11-6 0 3 3 0 016 0z" />
                    </svg>
                  ) : (
                    <span className="text-sm font-semibold text-primary-600 dark:text-primary-300">
                      {conversation.display_name?.[0]?.toUpperCase() || '?'}
                    </span>
                  )}
                </div>
                <div className="flex-1 min-w-0">
                  <p className="text-sm font-medium text-slate-900 dark:text-slate-100 truncate">
                    {conversation.display_name}
                  </p>
                  {conversation.last_message ? (
                    <p className="text-xs text-slate-500 dark:text-slate-400 truncate mt-0.5">
                      <span className="font-medium">{conversation.last_message.sender.full_name || conversation.last_message.sender.email}: </span>
                      {conversation.last_message.content}
                    </p>
                  ) : (
                    <p className="text-xs text-slate-400 dark:text-slate-500 mt-0.5">No messages yet</p>
                  )}
                </div>
              </button>
            ))
          )}
        </div>
      </div>

      {showCreate && (
        <CreateChatDialog
          onClose={() => setShowCreate(false)}
          onConversationCreated={onConversationCreated}
        />
      )}
    </>
  );
};

export default ConversationList;
