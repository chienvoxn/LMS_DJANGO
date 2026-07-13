import { useState } from 'react';

import CitationList from './CitationList';
import RagIcon from './RagIcon';

const formatTime = (value) => {
  if (!value) return '';
  const date = new Date(value);
  if (Number.isNaN(date.getTime())) return '';
  return date.toLocaleTimeString('vi-VN', { hour: '2-digit', minute: '2-digit' });
};

const RagMessage = ({ message }) => {
  const isUser = message.role === 'user';
  const [copied, setCopied] = useState(false);

  const copyContent = async () => {
    try {
      await navigator.clipboard.writeText(message.content || '');
      setCopied(true);
      window.setTimeout(() => setCopied(false), 1600);
    } catch {
      // Clipboard có thể bị chặn trên một số trình duyệt.
    }
  };

  if (isUser) {
    return (
      <div className="flex w-full justify-end">
        <div className="max-w-[88%] sm:max-w-[78%]">
          <div className="rounded-3xl rounded-br-lg bg-blue-600 px-4 py-3 text-sm leading-7 text-white shadow-sm shadow-blue-600/10">
            <div className="whitespace-pre-wrap break-words">{message.content}</div>
          </div>
          {message.created_at && (
            <p className="mr-1 mt-1.5 text-right text-[10px] text-slate-400">
              {formatTime(message.created_at)}
            </p>
          )}
        </div>
      </div>
    );
  }

  return (
    <article className="group flex w-full gap-3 sm:gap-4">
      <div className="mt-0.5 flex h-9 w-9 shrink-0 items-center justify-center rounded-xl bg-gradient-to-br from-blue-600 to-indigo-600 text-white shadow-md shadow-blue-600/20">
        <RagIcon name="sparkles" size={18} />
      </div>

      <div className="min-w-0 flex-1">
        <div className="mb-2 flex flex-wrap items-center gap-x-2 gap-y-1">
          <span className="text-sm font-bold text-slate-900 dark:text-white">LMS AI</span>
          <span className="rounded-full bg-emerald-50 px-2 py-0.5 text-[10px] font-semibold text-emerald-700 ring-1 ring-emerald-100 dark:bg-emerald-950/40 dark:text-emerald-300 dark:ring-emerald-900">
            RAG
          </span>
          {message.response_time_ms > 0 && (
            <span className="text-[11px] text-slate-400">
              {(message.response_time_ms / 1000).toFixed(1)} giây
            </span>
          )}
        </div>

        <div className="rounded-2xl rounded-tl-md border border-slate-200 bg-white px-4 py-4 shadow-sm dark:border-slate-700 dark:bg-slate-900 sm:px-5">
          <div className="whitespace-pre-wrap break-words text-sm leading-7 text-slate-700 dark:text-slate-200">
            {message.content}
          </div>
          <CitationList citations={message.citations} />
        </div>

        <div className="mt-2 flex min-h-7 items-center gap-1 text-slate-400">
          <button
            type="button"
            onClick={copyContent}
            className="inline-flex items-center gap-1.5 rounded-lg px-2 py-1 text-[11px] font-medium transition hover:bg-slate-100 hover:text-slate-700 dark:hover:bg-slate-800 dark:hover:text-slate-200"
          >
            <RagIcon name={copied ? 'check' : 'copy'} size={13} />
            {copied ? 'Đã sao chép' : 'Sao chép'}
          </button>
          {message.model_name && (
            <span className="ml-1 hidden text-[10px] sm:inline">{message.model_name}</span>
          )}
          {message.created_at && (
            <span className="ml-auto text-[10px]">{formatTime(message.created_at)}</span>
          )}
        </div>
      </div>
    </article>
  );
};

export default RagMessage;
