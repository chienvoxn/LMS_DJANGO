import { useCallback, useEffect, useMemo, useState } from 'react';

import ragAPI from '../api/ragApi';
import DocumentPicker from '../components/rag/DocumentPicker';
import RagChatWindow from '../components/rag/RagChatWindow';
import RagComposer from '../components/rag/RagComposer';
import RagIcon from '../components/rag/RagIcon';
import RagSidebar from '../components/rag/RagSidebar';

const unwrapList = (response) => {
  const data = response?.data;
  return Array.isArray(data) ? data : data?.results || [];
};

const errorMessage = (error, fallback) =>
  error?.response?.data?.detail ||
  error?.response?.data?.file?.[0] ||
  error?.message ||
  fallback;

const noticeStyles = {
  success:
    'border-emerald-200 bg-emerald-50 text-emerald-800 dark:border-emerald-900 dark:bg-emerald-950/90 dark:text-emerald-200',
  error:
    'border-red-200 bg-red-50 text-red-800 dark:border-red-900 dark:bg-red-950/90 dark:text-red-200',
  info:
    'border-blue-200 bg-blue-50 text-blue-800 dark:border-blue-900 dark:bg-blue-950/90 dark:text-blue-200',
};

const noticeIcon = {
  success: 'success',
  error: 'alert',
  info: 'info',
};

const AIAssistant = () => {
  const [documents, setDocuments] = useState([]);
  const [conversations, setConversations] = useState([]);
  const [activeConversation, setActiveConversation] = useState(null);
  const [selectedDocumentIds, setSelectedDocumentIds] = useState([]);
  const [loadingPage, setLoadingPage] = useState(true);
  const [sending, setSending] = useState(false);
  const [notice, setNotice] = useState(null);
  const [sidebarOpen, setSidebarOpen] = useState(false);
  const [documentsOpen, setDocumentsOpen] = useState(false);

  const showNotice = useCallback((text, type = 'info') => {
    setNotice({ text, type });
  }, []);

  const loadDocuments = useCallback(async () => {
    const response = await ragAPI.getDocuments();
    const items = unwrapList(response);
    setDocuments(items);
    return items;
  }, []);

  const loadConversations = useCallback(async () => {
    const response = await ragAPI.getConversations();
    const items = unwrapList(response);
    setConversations(items);
    return items;
  }, []);

  const openConversation = useCallback(async (id) => {
    const response = await ragAPI.getConversation(id);
    setActiveConversation(response.data);
    setSelectedDocumentIds(
      (response.data.documents || [])
        .filter((item) => item.status === 'ready')
        .map((item) => item.id),
    );
    setSidebarOpen(false);
  }, []);

  useEffect(() => {
    const initialize = async () => {
      setLoadingPage(true);
      try {
        const [documentItems, conversationItems] = await Promise.all([
          loadDocuments(),
          loadConversations(),
        ]);

        if (conversationItems.length) {
          await openConversation(conversationItems[0].id);
        } else {
          const firstReadyDocument = documentItems.find(
            (document) => document.status === 'ready',
          );
          if (firstReadyDocument) setSelectedDocumentIds([firstReadyDocument.id]);
        }
      } catch (error) {
        showNotice(errorMessage(error, 'Không thể tải AI Assistant.'), 'error');
      } finally {
        setLoadingPage(false);
      }
    };

    initialize();
  }, [loadDocuments, loadConversations, openConversation, showNotice]);

  const selectedDocuments = useMemo(
    () => documents.filter((item) => selectedDocumentIds.includes(item.id)),
    [documents, selectedDocumentIds],
  );

  const readyDocumentCount = useMemo(
    () => documents.filter((item) => item.status === 'ready').length,
    [documents],
  );

  const createConversation = async () => {
    const response = await ragAPI.createConversation({
      title: 'New chat',
      document_ids: selectedDocumentIds,
    });
    setActiveConversation(response.data);
    await loadConversations();
    return response.data;
  };

  const handleNewConversation = () => {
    setActiveConversation(null);
    setNotice(null);
    setSidebarOpen(false);
  };

  const handleDocumentSelection = async (ids) => {
    setSelectedDocumentIds(ids);
    if (!activeConversation) return;

    try {
      const response = await ragAPI.updateConversation(activeConversation.id, {
        document_ids: ids,
      });
      setActiveConversation(response.data);
      await loadConversations();
    } catch (error) {
      showNotice(errorMessage(error, 'Không thể cập nhật tài liệu.'), 'error');
    }
  };

  const handleUpload = async (files) => {
    setNotice(null);
    showNotice(`Đang xử lý ${files.length} tài liệu...`, 'info');

    const failures = [];
    const uploadedReadyIds = [];

    for (const file of files) {
      try {
        const response = await ragAPI.uploadDocument(file);
        if (response.data.status === 'ready') {
          uploadedReadyIds.push(response.data.id);
        } else if (response.data.status === 'failed') {
          failures.push(
            `${file.name}: ${response.data.error_message || 'Không thể lập chỉ mục'}`,
          );
        }
      } catch (error) {
        failures.push(`${file.name}: ${errorMessage(error, 'Upload thất bại')}`);
      }
    }

    await loadDocuments();

    if (!selectedDocumentIds.length && uploadedReadyIds.length) {
      await handleDocumentSelection(uploadedReadyIds);
    }

    if (failures.length) {
      showNotice(failures.join('\n'), 'error');
    } else {
      showNotice('Tài liệu đã sẵn sàng để truy xuất.', 'success');
    }
  };

  const handleSend = async (question) => {
    if (!selectedDocumentIds.length) {
      showNotice('Hãy chọn ít nhất một tài liệu có trạng thái sẵn sàng.', 'error');
      setDocumentsOpen(true);
      return;
    }

    setSending(true);
    setNotice(null);
    let conversation = activeConversation;

    try {
      if (!conversation) conversation = await createConversation();

      const optimisticMessage = {
        id: `temp-${Date.now()}`,
        role: 'user',
        content: question,
        citations: [],
        created_at: new Date().toISOString(),
      };

      setActiveConversation((current) => ({
        ...(current || conversation),
        messages: [
          ...(current?.messages || conversation.messages || []),
          optimisticMessage,
        ],
      }));

      await ragAPI.ask(conversation.id, {
        question,
        document_ids: selectedDocumentIds,
      });

      const detail = await ragAPI.getConversation(conversation.id);
      setActiveConversation(detail.data);
      await loadConversations();
    } catch (error) {
      showNotice(errorMessage(error, 'Không thể tạo câu trả lời.'), 'error');
      if (conversation?.id) {
        try {
          await openConversation(conversation.id);
        } catch {
          // Giữ trạng thái hiện tại nếu tải lại thất bại.
        }
      }
    } finally {
      setSending(false);
    }
  };

  const handleDeleteConversation = async (id) => {
    if (!window.confirm('Xóa hội thoại này?')) return;

    try {
      await ragAPI.deleteConversation(id);
      const items = await loadConversations();
      if (activeConversation?.id === id) {
        if (items.length) await openConversation(items[0].id);
        else setActiveConversation(null);
      }
      showNotice('Đã xóa hội thoại.', 'success');
    } catch (error) {
      showNotice(errorMessage(error, 'Không thể xóa hội thoại.'), 'error');
    }
  };

  const handleDeleteDocument = async (id) => {
    if (!window.confirm('Xóa tài liệu và toàn bộ vector liên quan?')) return;

    try {
      await ragAPI.deleteDocument(id);
      const nextIds = selectedDocumentIds.filter((item) => item !== id);
      setSelectedDocumentIds(nextIds);
      await loadDocuments();

      if (activeConversation) {
        await ragAPI.updateConversation(activeConversation.id, {
          document_ids: nextIds,
        });
        await openConversation(activeConversation.id);
      }
      showNotice('Đã xóa tài liệu.', 'success');
    } catch (error) {
      showNotice(errorMessage(error, 'Không thể xóa tài liệu.'), 'error');
    }
  };

  const handleReindexDocument = async (id) => {
    try {
      showNotice('Đang lập chỉ mục lại tài liệu...', 'info');
      await ragAPI.reindexDocument(id);
      await loadDocuments();
      showNotice('Đã lập chỉ mục lại tài liệu.', 'success');
    } catch (error) {
      await loadDocuments();
      showNotice(errorMessage(error, 'Re-index thất bại.'), 'error');
    }
  };

  if (loadingPage) {
    return (
      <div className="flex h-[calc(100vh-64px)] min-h-[560px] items-center justify-center bg-slate-50 dark:bg-slate-950">
        <div className="text-center">
          <span className="mx-auto flex h-14 w-14 items-center justify-center rounded-2xl bg-blue-600 text-white shadow-xl shadow-blue-600/25">
            <RagIcon name="refresh" size={23} className="animate-spin" />
          </span>
          <p className="mt-4 text-sm font-semibold text-slate-700 dark:text-slate-200">
            Đang mở AI Workspace...
          </p>
          <p className="mt-1 text-xs text-slate-400">Đang tải hội thoại và tài liệu</p>
        </div>
      </div>
    );
  }

  const conversationTitle = activeConversation?.title || 'Cuộc trò chuyện mới';

  return (
    <div className="relative flex h-[calc(100vh-64px)] min-h-[600px] overflow-hidden bg-slate-100 dark:bg-slate-950">
      {/* Desktop sidebar */}
      <div className="hidden h-full w-[292px] shrink-0 lg:block">
        <RagSidebar
          conversations={conversations}
          activeConversationId={activeConversation?.id}
          onOpenConversation={openConversation}
          onNewConversation={handleNewConversation}
          onDeleteConversation={handleDeleteConversation}
          documents={documents}
          onUpload={handleUpload}
          onOpenDocuments={() => setDocumentsOpen(true)}
        />
      </div>

      {/* Mobile sidebar */}
      {sidebarOpen && (
        <div className="absolute inset-0 z-50 lg:hidden">
          <button
            type="button"
            className="absolute inset-0 bg-slate-950/60 backdrop-blur-sm"
            onClick={() => setSidebarOpen(false)}
            aria-label="Đóng menu"
          />
          <div className="relative h-full w-[292px] max-w-[88vw] shadow-2xl">
            <RagSidebar
              conversations={conversations}
              activeConversationId={activeConversation?.id}
              onOpenConversation={openConversation}
              onNewConversation={handleNewConversation}
              onDeleteConversation={handleDeleteConversation}
              documents={documents}
              onUpload={handleUpload}
              onOpenDocuments={() => {
                setSidebarOpen(false);
                setDocumentsOpen(true);
              }}
              onClose={() => setSidebarOpen(false)}
            />
          </div>
        </div>
      )}

      <main className="flex min-w-0 flex-1 flex-col bg-white dark:bg-slate-950">
        <header className="flex h-[72px] shrink-0 items-center gap-3 border-b border-slate-200 bg-white px-3 dark:border-slate-800 dark:bg-slate-950 sm:px-5">
          <button
            type="button"
            onClick={() => setSidebarOpen(true)}
            className="flex h-10 w-10 shrink-0 items-center justify-center rounded-xl text-slate-500 transition hover:bg-slate-100 hover:text-slate-900 dark:hover:bg-slate-800 dark:hover:text-white lg:hidden"
            aria-label="Mở menu"
          >
            <RagIcon name="menu" size={20} />
          </button>

          <div className="min-w-0 flex-1">
            <div className="flex min-w-0 items-center gap-2">
              <h2 className="truncate text-sm font-bold text-slate-950 dark:text-white sm:text-base">
                {conversationTitle}
              </h2>
              <span className="hidden rounded-full bg-blue-50 px-2 py-0.5 text-[10px] font-semibold text-blue-700 dark:bg-blue-950/40 dark:text-blue-300 sm:inline-flex">
                RAG Assistant
              </span>
            </div>
            <div className="mt-1 flex items-center gap-2 text-[11px] text-slate-500 dark:text-slate-400">
              <span className="inline-flex items-center gap-1">
                <RagIcon name="files" size={12} />
                {selectedDocuments.length} nguồn đang chọn
              </span>
              <span className="h-1 w-1 rounded-full bg-slate-300 dark:bg-slate-700" />
              <span className="hidden sm:inline">Trả lời có trích dẫn</span>
            </div>
          </div>

          <div className="hidden items-center gap-2 text-[11px] text-slate-500 md:flex dark:text-slate-400">
            <span className="inline-flex items-center gap-1.5 rounded-full border border-slate-200 bg-slate-50 px-3 py-1.5 dark:border-slate-700 dark:bg-slate-900">
              <span className="h-2 w-2 rounded-full bg-emerald-500" />
              {readyDocumentCount} tài liệu ready
            </span>
          </div>

          <button
            type="button"
            onClick={() => setDocumentsOpen(true)}
            className="flex h-10 items-center gap-2 rounded-xl border border-slate-200 bg-white px-3 text-xs font-semibold text-slate-600 shadow-sm transition hover:border-blue-200 hover:bg-blue-50 hover:text-blue-700 dark:border-slate-700 dark:bg-slate-900 dark:text-slate-300 dark:hover:border-blue-800 dark:hover:bg-blue-950/40 xl:hidden"
          >
            <RagIcon name="panel" size={17} />
            <span className="hidden sm:inline">Tài liệu</span>
            {selectedDocuments.length > 0 && (
              <span className="flex h-5 min-w-5 items-center justify-center rounded-full bg-blue-600 px-1 text-[10px] text-white">
                {selectedDocuments.length}
              </span>
            )}
          </button>
        </header>

        <RagChatWindow
          messages={activeConversation?.messages || []}
          loading={sending}
          documents={documents}
          selectedDocuments={selectedDocuments}
          onUpload={handleUpload}
          onSuggestion={handleSend}
          onOpenDocuments={() => setDocumentsOpen(true)}
        />

        <RagComposer
          onSend={handleSend}
          onUpload={handleUpload}
          disabled={sending || selectedDocumentIds.length === 0}
          sending={sending}
          selectedDocuments={selectedDocuments}
          onOpenDocuments={() => setDocumentsOpen(true)}
        />
      </main>

      {/* Desktop document panel */}
      <div className="hidden h-full w-[336px] shrink-0 border-l border-slate-200 dark:border-slate-800 xl:block">
        <DocumentPicker
          documents={documents}
          selectedIds={selectedDocumentIds}
          onChange={handleDocumentSelection}
          onUpload={handleUpload}
          onDeleteDocument={handleDeleteDocument}
          onReindexDocument={handleReindexDocument}
        />
      </div>

      {/* Tablet/mobile document drawer */}
      {documentsOpen && (
        <div className="absolute inset-0 z-50 xl:hidden">
          <button
            type="button"
            className="absolute inset-0 bg-slate-950/55 backdrop-blur-sm"
            onClick={() => setDocumentsOpen(false)}
            aria-label="Đóng danh sách tài liệu"
          />
          <div className="absolute right-0 top-0 h-full w-[360px] max-w-[94vw] border-l border-slate-200 bg-white shadow-2xl dark:border-slate-800 dark:bg-slate-950">
            <DocumentPicker
              documents={documents}
              selectedIds={selectedDocumentIds}
              onChange={handleDocumentSelection}
              onUpload={handleUpload}
              onDeleteDocument={handleDeleteDocument}
              onReindexDocument={handleReindexDocument}
              onClose={() => setDocumentsOpen(false)}
            />
          </div>
        </div>
      )}

      {notice && (
        <div className="pointer-events-none absolute left-1/2 top-4 z-[70] w-[min(92vw,560px)] -translate-x-1/2">
          <div
            className={`pointer-events-auto flex items-start gap-3 rounded-2xl border px-4 py-3 shadow-xl backdrop-blur ${
              noticeStyles[notice.type] || noticeStyles.info
            }`}
          >
            <RagIcon
              name={noticeIcon[notice.type] || 'info'}
              size={18}
              className="mt-0.5 shrink-0"
            />
            <p className="min-w-0 flex-1 whitespace-pre-wrap text-xs font-medium leading-5">
              {notice.text}
            </p>
            <button
              type="button"
              onClick={() => setNotice(null)}
              className="flex h-7 w-7 shrink-0 items-center justify-center rounded-lg transition hover:bg-black/5 dark:hover:bg-white/10"
              aria-label="Đóng thông báo"
            >
              <RagIcon name="close" size={15} />
            </button>
          </div>
        </div>
      )}
    </div>
  );
};

export default AIAssistant;
