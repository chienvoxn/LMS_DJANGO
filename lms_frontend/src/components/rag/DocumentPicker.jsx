import { useMemo, useState } from 'react';

import RagIcon from './RagIcon';
import RagUploader from './RagUploader';

const statusStyles = {
  ready: {
    label: 'Sẵn sàng',
    className:
      'bg-emerald-50 text-emerald-700 ring-emerald-100 dark:bg-emerald-950/40 dark:text-emerald-300 dark:ring-emerald-900',
  },
  processing: {
    label: 'Đang xử lý',
    className:
      'bg-amber-50 text-amber-700 ring-amber-100 dark:bg-amber-950/40 dark:text-amber-300 dark:ring-amber-900',
  },
  pending: {
    label: 'Đang chờ',
    className:
      'bg-slate-100 text-slate-600 ring-slate-200 dark:bg-slate-800 dark:text-slate-300 dark:ring-slate-700',
  },
  failed: {
    label: 'Lỗi',
    className:
      'bg-red-50 text-red-700 ring-red-100 dark:bg-red-950/40 dark:text-red-300 dark:ring-red-900',
  },
};

const fileTypeStyles = {
  pdf: 'bg-red-50 text-red-600 dark:bg-red-950/40 dark:text-red-300',
  docx: 'bg-blue-50 text-blue-600 dark:bg-blue-950/40 dark:text-blue-300',
  pptx: 'bg-orange-50 text-orange-600 dark:bg-orange-950/40 dark:text-orange-300',
  txt: 'bg-slate-100 text-slate-600 dark:bg-slate-800 dark:text-slate-300',
};

const formatBytes = (bytes) => {
  if (!bytes) return '';
  if (bytes < 1024) return `${bytes} B`;
  if (bytes < 1024 * 1024) return `${(bytes / 1024).toFixed(1)} KB`;
  return `${(bytes / (1024 * 1024)).toFixed(1)} MB`;
};

const DocumentPicker = ({
  documents,
  selectedIds,
  onChange,
  onUpload,
  onDeleteDocument,
  onReindexDocument,
  onClose,
}) => {
  const [query, setQuery] = useState('');
  const normalizedQuery = query.trim().toLowerCase();

  const filteredDocuments = useMemo(
    () =>
      documents.filter((document) =>
        `${document.name} ${document.original_name || ''} ${document.file_type || ''}`
          .toLowerCase()
          .includes(normalizedQuery),
      ),
    [documents, normalizedQuery],
  );

  const readyDocuments = documents.filter((item) => item.status === 'ready');
  const selectedReadyCount = readyDocuments.filter((item) =>
    selectedIds.includes(item.id),
  ).length;

  const toggle = (id) => {
    if (selectedIds.includes(id)) {
      onChange(selectedIds.filter((item) => item !== id));
    } else {
      onChange([...selectedIds, id]);
    }
  };

  return (
    <aside className="flex h-full w-full flex-col bg-white dark:bg-slate-950">
      <div className="border-b border-slate-200 px-4 py-4 dark:border-slate-800">
        <div className="flex items-start justify-between gap-3">
          <div>
            <div className="flex items-center gap-2">
              <span className="flex h-9 w-9 items-center justify-center rounded-xl bg-blue-50 text-blue-600 dark:bg-blue-950/40 dark:text-blue-400">
                <RagIcon name="files" size={18} />
              </span>
              <div>
                <h3 className="text-sm font-bold text-slate-900 dark:text-white">
                  Nguồn tài liệu
                </h3>
                <p className="mt-0.5 text-[11px] text-slate-500 dark:text-slate-400">
                  {selectedReadyCount}/{readyDocuments.length} tài liệu đang dùng
                </p>
              </div>
            </div>
          </div>
          {onClose && (
            <button
              type="button"
              onClick={onClose}
              className="flex h-9 w-9 items-center justify-center rounded-xl text-slate-500 transition hover:bg-slate-100 hover:text-slate-900 dark:hover:bg-slate-800 dark:hover:text-white"
              aria-label="Đóng danh sách tài liệu"
            >
              <RagIcon name="close" size={18} />
            </button>
          )}
        </div>

        <div className="relative mt-4">
          <RagIcon
            name="search"
            size={16}
            className="pointer-events-none absolute left-3 top-1/2 -translate-y-1/2 text-slate-400"
          />
          <input
            value={query}
            onChange={(event) => setQuery(event.target.value)}
            placeholder="Tìm tài liệu..."
            className="h-10 w-full rounded-xl border border-slate-200 bg-slate-50 pl-9 pr-3 text-sm text-slate-800 outline-none transition placeholder:text-slate-400 focus:border-blue-400 focus:bg-white focus:ring-4 focus:ring-blue-500/10 dark:border-slate-700 dark:bg-slate-900 dark:text-slate-100 dark:focus:bg-slate-900"
          />
        </div>

        {readyDocuments.length > 0 && (
          <div className="mt-3 flex items-center gap-2">
            <button
              type="button"
              onClick={() => onChange(readyDocuments.map((item) => item.id))}
              className="rounded-lg bg-blue-50 px-2.5 py-1.5 text-[11px] font-semibold text-blue-700 transition hover:bg-blue-100 dark:bg-blue-950/40 dark:text-blue-300 dark:hover:bg-blue-950/70"
            >
              Chọn tất cả
            </button>
            <button
              type="button"
              onClick={() => onChange([])}
              className="rounded-lg px-2.5 py-1.5 text-[11px] font-semibold text-slate-500 transition hover:bg-slate-100 hover:text-slate-800 dark:hover:bg-slate-800 dark:hover:text-slate-200"
            >
              Bỏ chọn
            </button>
          </div>
        )}
      </div>

      <div className="min-h-0 flex-1 overflow-y-auto p-3">
        {filteredDocuments.length === 0 ? (
          <div className="flex h-full min-h-48 flex-col items-center justify-center px-5 text-center">
            <span className="flex h-12 w-12 items-center justify-center rounded-2xl bg-slate-100 text-slate-400 dark:bg-slate-900">
              <RagIcon name="file" size={22} />
            </span>
            <p className="mt-3 text-sm font-semibold text-slate-700 dark:text-slate-200">
              {documents.length ? 'Không tìm thấy tài liệu' : 'Chưa có tài liệu'}
            </p>
            <p className="mt-1 text-xs leading-5 text-slate-500 dark:text-slate-400">
              {documents.length
                ? 'Thử tìm bằng tên hoặc định dạng khác.'
                : 'Tải tài liệu lên để bắt đầu truy xuất.'}
            </p>
          </div>
        ) : (
          <div className="space-y-2">
            {filteredDocuments.map((document) => {
              const status = statusStyles[document.status] || statusStyles.pending;
              const selectable = document.status === 'ready';
              const selected = selectedIds.includes(document.id);

              return (
                <div
                  key={document.id}
                  className={`group rounded-2xl border p-3 transition ${
                    selected
                      ? 'border-blue-300 bg-blue-50/70 shadow-sm dark:border-blue-800 dark:bg-blue-950/25'
                      : 'border-slate-200 bg-white hover:border-slate-300 hover:shadow-sm dark:border-slate-800 dark:bg-slate-900 dark:hover:border-slate-700'
                  }`}
                >
                  <div className="flex items-start gap-3">
                    <button
                      type="button"
                      onClick={() => selectable && toggle(document.id)}
                      disabled={!selectable}
                      className={`mt-0.5 flex h-5 w-5 shrink-0 items-center justify-center rounded-md border transition ${
                        selected
                          ? 'border-blue-600 bg-blue-600 text-white'
                          : selectable
                            ? 'border-slate-300 bg-white text-transparent hover:border-blue-400 dark:border-slate-600 dark:bg-slate-950'
                            : 'cursor-not-allowed border-slate-200 bg-slate-100 text-transparent opacity-60 dark:border-slate-700 dark:bg-slate-800'
                      }`}
                      aria-label={selected ? 'Bỏ chọn tài liệu' : 'Chọn tài liệu'}
                    >
                      <RagIcon name="check" size={13} strokeWidth={2.4} />
                    </button>

                    <div className="min-w-0 flex-1">
                      <div className="flex items-start gap-2">
                        <span
                          className={`flex h-9 w-9 shrink-0 items-center justify-center rounded-xl text-[10px] font-bold uppercase ${
                            fileTypeStyles[document.file_type] || fileTypeStyles.txt
                          }`}
                        >
                          {document.file_type || 'FILE'}
                        </span>
                        <div className="min-w-0 flex-1">
                          <p
                            className="truncate text-sm font-semibold text-slate-800 dark:text-slate-100"
                            title={document.name}
                          >
                            {document.name}
                          </p>
                          <div className="mt-1 flex flex-wrap items-center gap-x-2 gap-y-1 text-[10px] text-slate-500 dark:text-slate-400">
                            {document.chunk_count > 0 && (
                              <span>{document.chunk_count} chunks</span>
                            )}
                            {document.size_bytes > 0 && <span>{formatBytes(document.size_bytes)}</span>}
                          </div>
                        </div>
                      </div>

                      <div className="mt-3 flex items-center justify-between gap-2">
                        <span
                          className={`inline-flex items-center gap-1 rounded-full px-2 py-1 text-[10px] font-semibold ring-1 ${status.className}`}
                          title={document.error_message || ''}
                        >
                          {document.status === 'processing' && (
                            <RagIcon name="refresh" size={11} className="animate-spin" />
                          )}
                          {status.label}
                        </span>

                        <div className="flex items-center gap-1 opacity-100 sm:opacity-0 sm:transition sm:group-hover:opacity-100">
                          {(document.status === 'failed' || document.status === 'ready') && (
                            <button
                              type="button"
                              onClick={() => onReindexDocument(document.id)}
                              className="flex h-8 w-8 items-center justify-center rounded-lg text-slate-400 transition hover:bg-blue-50 hover:text-blue-600 dark:hover:bg-blue-950/40 dark:hover:text-blue-400"
                              title="Index lại"
                            >
                              <RagIcon name="refresh" size={15} />
                            </button>
                          )}
                          <button
                            type="button"
                            onClick={() => onDeleteDocument(document.id)}
                            className="flex h-8 w-8 items-center justify-center rounded-lg text-slate-400 transition hover:bg-red-50 hover:text-red-600 dark:hover:bg-red-950/40 dark:hover:text-red-400"
                            title="Xóa tài liệu"
                          >
                            <RagIcon name="trash" size={15} />
                          </button>
                        </div>
                      </div>

                      {document.status === 'failed' && document.error_message && (
                        <p className="mt-2 line-clamp-2 rounded-lg bg-red-50 px-2.5 py-2 text-[10px] leading-4 text-red-600 dark:bg-red-950/30 dark:text-red-300">
                          {document.error_message}
                        </p>
                      )}
                    </div>
                  </div>
                </div>
              );
            })}
          </div>
        )}
      </div>

      <div className="border-t border-slate-200 p-3 dark:border-slate-800">
        <RagUploader onUpload={onUpload} compact />
      </div>
    </aside>
  );
};

export default DocumentPicker;
