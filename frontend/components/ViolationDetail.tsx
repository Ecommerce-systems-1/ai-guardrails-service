import { useState } from 'react';
import { GuardResultOut } from '../types';

const SEVERITY_STYLES: Record<string, string> = {
  BLOCK: 'bg-red-900 border-red-600 text-red-200',
  WARN: 'bg-yellow-900 border-yellow-600 text-yellow-200',
  PASS: 'bg-gray-800 border-gray-600 text-gray-400',
};

interface Props {
  result: GuardResultOut;
}

export default function ViolationDetail({ result }: Props) {
  const [open, setOpen] = useState(false);

  return (
    <div
      className={`border rounded-lg p-2 cursor-pointer ${SEVERITY_STYLES[result.severity]}`}
      onClick={() => setOpen((o) => !o)}
    >
      <div className="flex items-center justify-between">
        <span className="text-xs font-mono font-semibold">{result.guard_name}</span>
        <span className="text-xs opacity-60">{open ? '▲' : '▼'}</span>
      </div>
      <div className="text-xs opacity-75 mt-0.5">{result.details}</div>
      {open && result.violations.length > 0 && (
        <ul className="mt-2 space-y-1">
          {result.violations.map((v) => (
            <li key={v} className="text-xs font-mono bg-black bg-opacity-30 rounded px-2 py-1">
              {v}
            </li>
          ))}
        </ul>
      )}
    </div>
  );
}
