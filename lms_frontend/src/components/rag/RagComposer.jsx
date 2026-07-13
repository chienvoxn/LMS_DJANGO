import { useEffect, useRef, useState } from 'react';

import RagIcon from './RagIcon';

const RagComposer = ({
  onSend,
  onUpload,
  disabled,
  sending,
  selectedDocuments = [],
  onOpenDocuments,
}) => {
  const [value, setValue] = useState('');
  const textareaRef = useRef(null);
  const fileInputRef = useRef(null);
  const [uploading, setUploading] = useState(false);

  useEffect(() => {
    const textarea = textareaRef.current;
    if (!textarea) return;
    textarea.style.height = 'auto';
    textarea.style.height = `${Math.min(textarea.scrollHeight, 160)}px`;
  }, [value]);

  const submit = async () => {
    const question = value.trim();
    if (!question || disabled) return;
    setValue('');
    await onSend(question);
  };

  const handleKeyDown = (event) => {
    if (event.key === 'Enter' && !event.shiftKey) {
      event.preventDefault();
      submit();
    }
  };

  const uploadFiles = async (event) => {
    const files = Array.from(event.target.files || []);
    if (!files.length) return;
    setUploading(true);
    try {
      await onUpload(files);
    } finally {
      setUploading(false);
      event.target.value = '';
    }
  };

  return (
    <div className="border-t border-slate-200 bg-white/95 px-3 pb-3 pt-3 backdrop-blur-xl dark:border-slate-800 dark:bg-slate-950/95 sm:px-6 sm:pb-4">
      <div className="mx-auto w-full max-w-4xl">
        <div className="mb-2 flex min-h-7 items-center gap-2 overflow-hidden">
          <button
            type="button"
            onClick={onOpenDocuments}
            className="inline-flex shrink-0 items-center gap-1.5 rounded-lg px-2 py-1 text-[11px] font-semibold text-blue-600 transition hover:bg-blue-50 dark:text-blue-400 dark:hover:bg-blue-950/40"
          >
            <RagIcon name="files" size={13} />
            {selectedDocuments.length
              ? `${selectedDocuments.length} tài liệu đang dùng`
              : 'Chọn tài liệu'}
          </button>
          <div className="flex min-w-0 gap-1.5 overflow-hidden">
            {selectedDocuments.slice(0, 2).map((document) => (
              <span
                key={document.id}
                className="max-w-48 truncate rounded-full bg-slate-100 px-2.5 py-1 text-[11px] text-slate-600 dark:bg-slate-800 dark:text-slate-300"
              >
                {document.name}
              </span>
            ))}
            {selectedDocuments.length > 2 && (
              <span className="shrink-0 rounded-full bg-slate-100 px-2.5 py-1 text-[11px] font-medium text-slate-500 dark:bg-slate-800 dark:text-slate-300">
                +{selectedDocuments.length - 2}
              </span>
            )}
          </div>
        </div>

        <div className="flex items-end gap-1.5 rounded-2xl border border-slate-300 bg-white p-2 shadow-[0_8px_30px_rgba(15,23,42,0.08)] transition focus-within:border-blue-500 focus-within:ring-4 focus-within:ring-blue-500/10 dark:border-slate-700 dark:bg-slate-900">
          <input
            ref={fileInputRef}
            type="file"
            accept=".pdf,.txt,.docx,.pptx"
            multiple
            className="hidden"
            onChange={uploadFiles}
          />
          <button
            type="button"
            onClick={() => fileInputRef.current?.click()}
            disabled={uploading || sending}
            className="mb-0.5 flex h-10 w-10 shrink-0 items-center justify-center rounded-xl text-slate-500 transition hover:bg-slate-100 hover:text-blue-600 disabled:cursor-not-allowed disabled:opacity-50 dark:text-slate-400 dark:hover:bg-slate-800 dark:hover:text-blue-400"
            title="Tải thêm tài liệu"
          >
            <RagIcon
              name={uploading ? 'refresh' : 'paperclip'}
              size={19}
              className={uploading ? 'animate-spin' : ''}
            />
          </button>

          <textarea
            ref={textareaRef}
            value={value}
            onChange={(event) => setValue(event.target.value)}
            onKeyDown={handleKeyDown}
            rows={1}
            placeholder={
              selectedDocuments.length
                ? 'Hỏi bất cứ điều gì về tài liệu...'
                : 'Chọn ít nhất một tài liệu đã sẵn sàng...'
            }
            disabled={disabled}
            className="max-h-40 min-h-[44px] flex-1 resize-none bg-transparent px-1 py-2.5 text-sm leading-6 text-slate-900 outline-none placeholder:text-slate-400 disabled:cursor-not-allowed dark:text-slate-100"
          />

          <button
            type="button"
            onClick={submit}
            disabled={disabled || !value.trim()}
            className="mb-0.5 flex h-10 w-10 shrink-0 items-center justify-center rounded-xl bg-blue-600 text-white shadow-sm transition hover:bg-blue-700 disabled:cursor-not-allowed disabled:bg-slate-200 disabled:text-slate-400 disabled:shadow-none dark:disabled:bg-slate-800"
            aria-label="Gửi câu hỏi"
          >
            {sending ? (
              <RagIcon name="refresh" size={17} className="animate-spin" />
            ) : (
              <RagIcon name="send" size={17} />
            )}
          </button>
        </div>

        <p className="mt-2 text-center text-[10px] leading-4 text-slate-400">
          Enter để gửi · Shift + Enter để xuống dòng · Luôn kiểm tra nguồn trích dẫn
        </p>
      </div>
    </div>
  );
};

export default RagComposer;
