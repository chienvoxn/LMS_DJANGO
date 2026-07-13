import { useRef, useState } from 'react';

import RagIcon from './RagIcon';

const RagUploader = ({ onUpload, compact = false, className = '' }) => {
  const inputRef = useRef(null);
  const [uploading, setUploading] = useState(false);
  const [dragging, setDragging] = useState(false);

  const uploadFiles = async (fileList) => {
    const files = Array.from(fileList || []);
    if (!files.length || uploading) return;

    setUploading(true);
    try {
      await onUpload(files);
    } finally {
      setUploading(false);
      if (inputRef.current) inputRef.current.value = '';
    }
  };

  const handleDrop = (event) => {
    event.preventDefault();
    setDragging(false);
    uploadFiles(event.dataTransfer.files);
  };

  return (
    <div className={className}>
      <input
        ref={inputRef}
        type="file"
        accept=".pdf,.txt,.docx,.pptx"
        multiple
        className="hidden"
        onChange={(event) => uploadFiles(event.target.files)}
      />

      {compact ? (
        <button
          type="button"
          onClick={() => inputRef.current?.click()}
          disabled={uploading}
          className="flex w-full items-center justify-center gap-2 rounded-xl border border-slate-200 bg-white px-3 py-2.5 text-sm font-semibold text-slate-700 shadow-sm transition hover:border-blue-200 hover:bg-blue-50 hover:text-blue-700 disabled:cursor-not-allowed disabled:opacity-60 dark:border-slate-700 dark:bg-slate-900 dark:text-slate-200 dark:hover:border-blue-800 dark:hover:bg-blue-950/40"
        >
          <RagIcon
            name={uploading ? 'refresh' : 'upload'}
            size={17}
            className={uploading ? 'animate-spin' : ''}
          />
          {uploading ? 'Đang xử lý...' : 'Tải tài liệu lên'}
        </button>
      ) : (
        <button
          type="button"
          onClick={() => inputRef.current?.click()}
          onDragOver={(event) => {
            event.preventDefault();
            setDragging(true);
          }}
          onDragLeave={() => setDragging(false)}
          onDrop={handleDrop}
          disabled={uploading}
          className={`group w-full rounded-2xl border-2 border-dashed px-6 py-7 text-center transition disabled:cursor-not-allowed disabled:opacity-70 ${
            dragging
              ? 'border-blue-500 bg-blue-50 dark:bg-blue-950/30'
              : 'border-slate-200 bg-white hover:border-blue-300 hover:bg-blue-50/60 dark:border-slate-700 dark:bg-slate-900 dark:hover:border-blue-700 dark:hover:bg-blue-950/20'
          }`}
        >
          <span className="mx-auto flex h-12 w-12 items-center justify-center rounded-2xl bg-blue-600 text-white shadow-lg shadow-blue-600/20 transition group-hover:-translate-y-0.5">
            <RagIcon
              name={uploading ? 'refresh' : 'upload'}
              size={21}
              className={uploading ? 'animate-spin' : ''}
            />
          </span>
          <span className="mt-4 block text-sm font-semibold text-slate-900 dark:text-white">
            {uploading ? 'Đang đọc và lập chỉ mục...' : 'Chọn hoặc kéo thả tài liệu vào đây'}
          </span>
          <span className="mt-1 block text-xs leading-5 text-slate-500 dark:text-slate-400">
            PDF, DOCX, PPTX hoặc TXT · tối đa 30 MB mỗi tệp
          </span>
        </button>
      )}
    </div>
  );
};

export default RagUploader;
