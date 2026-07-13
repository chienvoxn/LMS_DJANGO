import RagIcon from './RagIcon';

const CitationList = ({ citations = [] }) => {
  if (!citations.length) return null;

  return (
    <div className="mt-5 border-t border-slate-200/80 pt-4 dark:border-slate-700">
      <div className="mb-3 flex items-center gap-2 text-xs font-semibold uppercase tracking-[0.14em] text-slate-500 dark:text-slate-400">
        <RagIcon name="book" size={14} />
        Nguồn đã truy xuất
      </div>
      <div className="grid gap-2 sm:grid-cols-2">
        {citations.map((citation, index) => (
          <div
            key={`${citation.document_id}-${citation.chunk_index}-${index}`}
            className="flex min-w-0 items-center gap-3 rounded-xl border border-slate-200 bg-slate-50/80 px-3 py-2.5 transition hover:border-blue-200 hover:bg-blue-50/70 dark:border-slate-700 dark:bg-slate-900/70 dark:hover:border-blue-800 dark:hover:bg-blue-950/30"
            title={
              citation.distance == null
                ? undefined
                : `Khoảng cách vector: ${Number(citation.distance).toFixed(3)}`
            }
          >
            <span className="flex h-8 w-8 shrink-0 items-center justify-center rounded-lg bg-white text-xs font-bold text-blue-600 shadow-sm ring-1 ring-slate-200 dark:bg-slate-800 dark:text-blue-400 dark:ring-slate-700">
              {citation.source_number || index + 1}
            </span>
            <div className="min-w-0">
              <p className="truncate text-xs font-semibold text-slate-800 dark:text-slate-100">
                {citation.document_name || 'Tài liệu'}
              </p>
              <p className="mt-0.5 text-[11px] text-slate-500 dark:text-slate-400">
                {citation.page_number
                  ? `Trang / slide ${citation.page_number}`
                  : `Đoạn ${Number(citation.chunk_index || 0) + 1}`}
              </p>
            </div>
          </div>
        ))}
      </div>
    </div>
  );
};

export default CitationList;
