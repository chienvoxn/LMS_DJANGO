import { useEffect, useRef } from 'react';

import RagIcon from './RagIcon';
import RagMessage from './RagMessage';
import RagUploader from './RagUploader';

const suggestions = [
  {
    title: 'Tóm tắt tài liệu',
    description: 'Rút gọn thành các ý chính dễ ghi nhớ',
    prompt: 'Tóm tắt các ý chính của tài liệu đang chọn.',
    icon: 'list',
  },
  {
    title: 'Giải thích dễ hiểu',
    description: 'Diễn giải nội dung cho người mới bắt đầu',
    prompt: 'Giải thích nội dung quan trọng trong tài liệu như cho người mới bắt đầu.',
    icon: 'book',
  },
  {
    title: 'Tạo câu hỏi ôn tập',
    description: 'Sinh 10 câu hỏi bám sát tài liệu',
    prompt: 'Tạo 10 câu hỏi ôn tập kèm đáp án ngắn từ tài liệu.',
    icon: 'chat',
  },
  {
    title: 'Tạo flashcard',
    description: 'Biến khái niệm chính thành thẻ ghi nhớ',
    prompt: 'Tạo flashcard cho những khái niệm quan trọng trong tài liệu.',
    icon: 'cards',
  },
];

const RagChatWindow = ({
  messages,
  loading,
  documents,
  selectedDocuments,
  onUpload,
  onSuggestion,
  onOpenDocuments,
}) => {
  const bottomRef = useRef(null);
  const hasDocuments = documents.length > 0;
  const hasSelectedDocuments = selectedDocuments.length > 0;

  useEffect(() => {
    bottomRef.current?.scrollIntoView({ behavior: 'smooth', block: 'end' });
  }, [messages, loading]);

  if (!messages.length) {
    return (
      <div className="min-h-0 flex-1 overflow-y-auto bg-[radial-gradient(circle_at_top,_rgba(37,99,235,0.08),_transparent_34%)] px-4 py-8 dark:bg-[radial-gradient(circle_at_top,_rgba(37,99,235,0.13),_transparent_35%)] sm:px-8 sm:py-12">
        <div className="mx-auto flex min-h-full w-full max-w-3xl flex-col justify-center">
          <div className="text-center">
            <div className="relative mx-auto mb-6 flex h-16 w-16 items-center justify-center rounded-2xl bg-gradient-to-br from-blue-600 to-indigo-600 text-white shadow-xl shadow-blue-600/25">
              <RagIcon name="sparkles" size={29} />
              <span className="absolute -right-1 -top-1 h-4 w-4 rounded-full border-2 border-white bg-emerald-400 dark:border-slate-950" />
            </div>
            <p className="mb-2 text-xs font-bold uppercase tracking-[0.2em] text-blue-600 dark:text-blue-400">
              Document intelligence
            </p>
            <h1 className="text-3xl font-bold tracking-tight text-slate-950 dark:text-white sm:text-4xl">
              Học nhanh hơn cùng tài liệu của bạn
            </h1>
            <p className="mx-auto mt-4 max-w-2xl text-sm leading-6 text-slate-500 dark:text-slate-400 sm:text-base">
              Hỏi đáp, tóm tắt, giải thích và tạo nội dung ôn tập. Mỗi câu trả lời đều truy xuất từ tài liệu bạn chọn và hiển thị nguồn tham khảo.
            </p>
          </div>

          {!hasDocuments ? (
            <div className="mx-auto mt-8 w-full max-w-xl">
              <RagUploader onUpload={onUpload} />
            </div>
          ) : !hasSelectedDocuments ? (
            <button
              type="button"
              onClick={onOpenDocuments}
              className="mx-auto mt-8 inline-flex items-center gap-2 rounded-xl bg-blue-600 px-5 py-3 text-sm font-semibold text-white shadow-lg shadow-blue-600/20 transition hover:-translate-y-0.5 hover:bg-blue-700"
            >
              <RagIcon name="files" size={17} />
              Chọn tài liệu để bắt đầu
              <RagIcon name="arrowRight" size={16} />
            </button>
          ) : (
            <div className="mx-auto mt-7 flex max-w-xl flex-wrap justify-center gap-2">
              {selectedDocuments.slice(0, 3).map((document) => (
                <span
                  key={document.id}
                  className="inline-flex max-w-56 items-center gap-1.5 rounded-full border border-slate-200 bg-white px-3 py-1.5 text-xs font-medium text-slate-600 shadow-sm dark:border-slate-700 dark:bg-slate-900 dark:text-slate-300"
                >
                  <RagIcon name="file" size={13} />
                  <span className="truncate">{document.name}</span>
                </span>
              ))}
              {selectedDocuments.length > 3 && (
                <span className="rounded-full bg-slate-100 px-3 py-1.5 text-xs font-semibold text-slate-500 dark:bg-slate-800 dark:text-slate-300">
                  +{selectedDocuments.length - 3} tài liệu
                </span>
              )}
            </div>
          )}

          <div className="mt-10 grid gap-3 sm:grid-cols-2">
            {suggestions.map((suggestion) => (
              <button
                key={suggestion.title}
                type="button"
                onClick={() => onSuggestion(suggestion.prompt)}
                disabled={!hasSelectedDocuments || loading}
                className="group flex items-start gap-3 rounded-2xl border border-slate-200 bg-white/90 p-4 text-left shadow-sm backdrop-blur transition hover:-translate-y-0.5 hover:border-blue-200 hover:shadow-md disabled:cursor-not-allowed disabled:opacity-45 disabled:hover:translate-y-0 dark:border-slate-700 dark:bg-slate-900/85 dark:hover:border-blue-800"
              >
                <span className="flex h-10 w-10 shrink-0 items-center justify-center rounded-xl bg-slate-100 text-slate-600 transition group-hover:bg-blue-600 group-hover:text-white dark:bg-slate-800 dark:text-slate-300">
                  <RagIcon name={suggestion.icon} size={18} />
                </span>
                <span>
                  <span className="block text-sm font-semibold text-slate-900 dark:text-white">
                    {suggestion.title}
                  </span>
                  <span className="mt-1 block text-xs leading-5 text-slate-500 dark:text-slate-400">
                    {suggestion.description}
                  </span>
                </span>
              </button>
            ))}
          </div>
        </div>
      </div>
    );
  }

  return (
    <div className="min-h-0 flex-1 overflow-y-auto bg-slate-50/80 px-4 py-6 dark:bg-slate-950/80 sm:px-8 sm:py-8">
      <div className="mx-auto flex w-full max-w-4xl flex-col gap-7">
        {messages.map((message, index) => (
          <RagMessage key={message.id || `temp-${index}`} message={message} />
        ))}

        {loading && (
          <div className="flex w-full gap-3 sm:gap-4">
            <div className="mt-0.5 flex h-9 w-9 shrink-0 items-center justify-center rounded-xl bg-gradient-to-br from-blue-600 to-indigo-600 text-white shadow-md shadow-blue-600/20">
              <RagIcon name="sparkles" size={18} />
            </div>
            <div className="rounded-2xl rounded-tl-md border border-slate-200 bg-white px-4 py-3.5 shadow-sm dark:border-slate-700 dark:bg-slate-900">
              <div className="flex items-center gap-3">
                <div className="flex gap-1">
                  {[0, 1, 2].map((item) => (
                    <span
                      key={item}
                      className="h-2 w-2 animate-bounce rounded-full bg-blue-500"
                      style={{ animationDelay: `${item * 120}ms` }}
                    />
                  ))}
                </div>
                <span className="text-xs font-medium text-slate-500 dark:text-slate-400">
                  Đang truy xuất và tổng hợp câu trả lời...
                </span>
              </div>
            </div>
          </div>
        )}
        <div ref={bottomRef} />
      </div>
    </div>
  );
};

export default RagChatWindow;
