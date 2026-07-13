import { useMemo, useState } from 'react';

import RagIcon from './RagIcon';
import RagUploader from './RagUploader';

const isSameDay = (a, b) =>
  a.getFullYear() === b.getFullYear() &&
  a.getMonth() === b.getMonth() &&
  a.getDate() === b.getDate();

const conversationGroup = (value) => {
  const date = new Date(value);
  if (Number.isNaN(date.getTime())) return 'Cũ hơn';
  const now = new Date();
  const diffDays = Math.floor((now - date) / 86400000);
  if (isSameDay(date, now)) return 'Hôm nay';
  if (diffDays <= 7) return '7 ngày qua';
  return 'Cũ hơn';
};

const groupsOrder = ['Hôm nay', '7 ngày qua', 'Cũ hơn'];

const RagSidebar = ({
  conversations,
  activeConversationId,
  onOpenConversation,
  onNewConversation,
  onDeleteConversation,
  documents,
  onUpload,
  onOpenDocuments,
  onClose,
}) => {
  const [query, setQuery] = useState('');
  const normalizedQuery = query.trim().toLowerCase();

  const filteredConversations = useMemo(
    () =>
      conversations.filter((conversation) =>
        (conversation.title || 'New chat').toLowerCase().includes(normalizedQuery),
      ),
    [conversations, normalizedQuery],
  );

  const groupedConversations = useMemo(() => {
    const result = Object.fromEntries(groupsOrder.map((group) => [group, []]));
    filteredConversations.forEach((conversation) => {
      const group = conversationGroup(conversation.updated_at || conversation.created_at);
      result[group].push(conversation);
    });
    return result;
  }, [filteredConversations]);

  const readyCount = documents.filter((document) => document.status === 'ready').length;

  return (
    <aside className="flex h-full w-full flex-col bg-slate-950 text-slate-100">
      <div className="border-b border-white/10 px-3 py-3">
        <div className="mb-3 flex items-center justify-between px-1">
          <div className="flex items-center gap-2">
            <span className="flex h-9 w-9 items-center justify-center rounded-xl bg-blue-600 text-white shadow-lg shadow-blue-600/20">
              <RagIcon name="sparkles" size={18} />
            </span>
            <div>
              <p className="text-sm font-bold">AI Workspace</p>
              <p className="text-[10px] text-slate-400">RAG trên tài liệu cá nhân</p>
            </div>
          </div>
          {onClose && (
            <button
              type="button"
              onClick={onClose}
              className="flex h-9 w-9 items-center justify-center rounded-xl text-slate-400 transition hover:bg-white/10 hover:text-white"
              aria-label="Đóng menu"
            >
              <RagIcon name="close" size={18} />
            </button>
          )}
        </div>

        <button
          type="button"
          onClick={onNewConversation}
          className="flex w-full items-center justify-center gap-2 rounded-xl bg-blue-600 px-4 py-2.5 text-sm font-semibold text-white shadow-lg shadow-blue-600/15 transition hover:bg-blue-500"
        >
          <RagIcon name="plus" size={17} />
          Cuộc trò chuyện mới
        </button>
        <RagUploader onUpload={onUpload} compact className="mt-2" />
      </div>

      <div className="px-3 pt-3">
        <div className="relative">
          <RagIcon
            name="search"
            size={15}
            className="pointer-events-none absolute left-3 top-1/2 -translate-y-1/2 text-slate-500"
          />
          <input
            value={query}
            onChange={(event) => setQuery(event.target.value)}
            placeholder="Tìm hội thoại..."
            className="h-9 w-full rounded-xl border border-white/10 bg-white/[0.06] pl-9 pr-3 text-xs text-white outline-none transition placeholder:text-slate-500 focus:border-blue-500/60 focus:bg-white/[0.08] focus:ring-4 focus:ring-blue-500/10"
          />
        </div>
      </div>

      <div className="min-h-0 flex-1 overflow-y-auto px-3 pb-4 pt-3">
        {filteredConversations.length === 0 ? (
          <div className="rounded-xl border border-dashed border-white/10 px-4 py-7 text-center">
            <RagIcon name="chat" size={22} className="mx-auto text-slate-600" />
            <p className="mt-2 text-xs font-medium text-slate-400">
              {conversations.length ? 'Không tìm thấy hội thoại' : 'Chưa có hội thoại'}
            </p>
          </div>
        ) : (
          groupsOrder.map((group) => {
            const items = groupedConversations[group];
            if (!items.length) return null;
            return (
              <section key={group} className="mb-5">
                <p className="mb-1.5 px-2 text-[10px] font-bold uppercase tracking-[0.16em] text-slate-500">
                  {group}
                </p>
                <div className="space-y-1">
                  {items.map((conversation) => {
                    const active = activeConversationId === conversation.id;
                    return (
                      <div
                        key={conversation.id}
                        className={`group relative flex items-center rounded-xl transition ${
                          active
                            ? 'bg-white/12 text-white ring-1 ring-white/10'
                            : 'text-slate-300 hover:bg-white/[0.07] hover:text-white'
                        }`}
                      >
                        <button
                          type="button"
                          onClick={() => onOpenConversation(conversation.id)}
                          className="min-w-0 flex-1 px-3 py-2.5 text-left"
                        >
                          <div className="flex items-center gap-2.5">
                            <RagIcon
                              name="chat"
                              size={15}
                              className={active ? 'text-blue-400' : 'text-slate-500'}
                            />
                            <div className="min-w-0 flex-1">
                              <p className="truncate text-xs font-medium" title={conversation.title}>
                                {conversation.title || 'New chat'}
                              </p>
                              <p className="mt-0.5 text-[10px] text-slate-500">
                                {conversation.message_count || 0} tin nhắn
                              </p>
                            </div>
                          </div>
                        </button>
                        <button
                          type="button"
                          onClick={() => onDeleteConversation(conversation.id)}
                          className="mr-1 flex h-8 w-8 items-center justify-center rounded-lg text-slate-500 opacity-100 transition hover:bg-red-500/10 hover:text-red-400 sm:opacity-0 sm:group-hover:opacity-100"
                          aria-label="Xóa hội thoại"
                        >
                          <RagIcon name="trash" size={14} />
                        </button>
                      </div>
                    );
                  })}
                </div>
              </section>
            );
          })
        )}
      </div>

      <div className="border-t border-white/10 p-3">
        <button
          type="button"
          onClick={onOpenDocuments}
          className="flex w-full items-center gap-3 rounded-xl px-3 py-2.5 text-left transition hover:bg-white/[0.07]"
        >
          <span className="flex h-9 w-9 items-center justify-center rounded-xl bg-white/[0.07] text-blue-400">
            <RagIcon name="database" size={17} />
          </span>
          <span className="min-w-0 flex-1">
            <span className="block text-xs font-semibold text-slate-200">Kho tài liệu</span>
            <span className="mt-0.5 block text-[10px] text-slate-500">
              {readyCount} sẵn sàng · {documents.length} tổng cộng
            </span>
          </span>
          <RagIcon name="arrowRight" size={15} className="text-slate-600" />
        </button>
      </div>
    </aside>
  );
};

export default RagSidebar;
