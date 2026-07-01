import { GuardResultOut } from '../types';
import ViolationDetail from './ViolationDetail';

const CHIP_STYLES: Record<string, string> = {
  BLOCK: 'bg-red-800 text-red-100 border-red-600',
  WARN: 'bg-yellow-800 text-yellow-100 border-yellow-600',
  PASS: 'bg-gray-700 text-gray-300 border-gray-600',
};

interface Props {
  results: GuardResultOut[];
  phase: 'input' | 'output';
}

export default function GuardPipelineView({ results, phase }: Props) {
  return (
    <div>
      <div className="flex flex-wrap gap-2 mb-3">
        {results.map((r) => (
          <span
            key={r.guard_name}
            className={`border rounded-full px-3 py-1 text-xs font-semibold ${CHIP_STYLES[r.severity]}`}
          >
            {r.guard_name} {r.severity === 'BLOCK' ? '🔴' : r.severity === 'WARN' ? '🟡' : '✅'}
          </span>
        ))}
      </div>
      <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 gap-2">
        {results.filter((r) => r.triggered).map((r) => (
          <ViolationDetail key={r.guard_name} result={r} />
        ))}
      </div>
      {results.every((r) => !r.triggered) && (
        <div className="text-sm text-green-400">
          ✅ All {phase} guards passed — no violations detected
        </div>
      )}
    </div>
  );
}
