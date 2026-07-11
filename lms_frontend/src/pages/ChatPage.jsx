import { useState, useEffect, useCallback, useRef } from 'react';
import { useAuth } from '../context/AuthContext';
import { chatAPI } from '../api/client';
import ConversationList from '../components/chat/ConversationList';
import ChatWindow from '../components/chat/ChatWindow';

const POLL_INTERVAL = 5000;

const ChatPage = () => {
  const { user } = useAuth();
  const [conversations, setConversations] = useState([]);
  const [activeConversationId, setActiveConversationId] = useState(null);
  const [activeConversation, setActiveConversation] = useState(null);
  const [messages, setMessages] = useState([]);
  const [loading, setLoading] = useState(true);
  const [sending, setSending] = useState(false);
  const pollRef = useRef(null);

  const fetchConversations = useCallback(async () => {
    try {
      const response = await chatAPI.getConversations();
      const data = response.data.results || response.data || [];
      setConversations((prev) => {
        const merged = [...data];
        prev.forEach((c) => {
          if (!merged.find((m) => m.id === c.id)) {
            merged.push(c);
          }
        });
        return merged;
      });
    } catch (err) {
      console.error('Failed to fetch conversations:', err);
    } finally {
      setLoading(false);
    }
  }, []);

  useEffect(() => {
    fetchConversations();
    pollRef.current = setInterval(fetchConversations, POLL_INTERVAL);
    return () => {
      if (pollRef.current) clearInterval(pollRef.current);
    };
  }, [fetchConversations]);

  useEffect(() => {
    if (activeConversationId) {
      const fetchDetail = async () => {
        try {
          const response = await chatAPI.getConversationDetail(activeConversationId);
          setActiveConversation(response.data);
          setMessages(response.data.messages || []);
        } catch (err) {
          console.error('Failed to fetch conversation detail:', err);
        }
      };
      fetchDetail();
      const detailInterval = setInterval(fetchDetail, POLL_INTERVAL);
      return () => clearInterval(detailInterval);
    } else {
      setActiveConversation(null);
      setMessages([]);
    }
  }, [activeConversationId]);

  const handleSelectConversation = (id) => {
    setActiveConversationId(id);
  };

  const handleConversationCreated = (newConversation) => {
    setConversations((prev) => {
      const exists = prev.find((c) => c.id === newConversation.id);
      if (exists) return prev;
      return [newConversation, ...prev];
    });
    setActiveConversationId(newConversation.id);
  };

  const handleSendMessage = async (content) => {
    if (!activeConversationId || !content.trim()) return;
    setSending(true);
    try {
      const response = await chatAPI.sendMessage(activeConversationId, content);
      const newMessage = response.data;
      setMessages((prev) => [...prev, newMessage]);
      setConversations((prev) =>
        prev.map((c) =>
          c.id === activeConversationId
            ? { ...c, last_message: newMessage, updated_at: new Date().toISOString() }
            : c
        )
      );
    } catch (err) {
      console.error('Failed to send message:', err);
    } finally {
      setSending(false);
    }
  };

  return (
    <div className="h-[calc(100vh-64px)] flex">
      <div className="w-80 lg:w-96 border-r border-slate-200 dark:border-slate-700 bg-white dark:bg-slate-800 flex-shrink-0">
        {loading ? (
          <div className="flex items-center justify-center h-full">
            <div className="animate-spin rounded-full h-8 w-8 border-2 border-primary-500 border-t-transparent" />
          </div>
        ) : (
          <ConversationList
            conversations={conversations}
            activeId={activeConversationId}
            onSelect={handleSelectConversation}
            onConversationCreated={handleConversationCreated}
          />
        )}
      </div>

      <ChatWindow
        conversation={activeConversation}
        messages={messages}
        onSendMessage={handleSendMessage}
        loading={sending}
      />
    </div>
  );
};

export default ChatPage;
