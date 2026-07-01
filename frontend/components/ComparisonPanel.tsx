const DECISION_BANNER: Record<string, { bg: string; text: string; label: string }> = {
  BLOCK: { bg: 'bg-red-900 border-red-600', text: 'text-red-300', label: '🚫 BLOCKED' },
  WARN: { bg: 'bg-yellow-900 border-yellow-600', text: 'text-yellow-300', label: '⚠️ FLAGGED' },
  ALLOW: { bg: 'bg-green-900 border-green-600', text: 'text-green-300', label: '✅ ALLOWED' },
};

interface Props {
  without: string;
  withGuards: string;
  decision: 'BLOCK' | 'WARN' | 'ALLOW';
}

export default function ComparisonPanel({ without, withGuards, decision }: Props) {
  const banner = DECISION_BANNER[decision];

  return (
    <div>
      <div className={`border rounded-lg px-4 py-2 mb-4 ${banner.bg}`}>
        <span className={`font-bold text-sm ${banner.text}`}>
          Final Decision: {banner.label}
        </span>
      </div>

      <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
        <div className="bg-gray-900 border border-gray-700 rounded-xl p-4">
          <div className="text-xs font-semibold text-gray-400 uppercase tracking-wider mb-2">
            Without Guardrails
          </div>
          <p className="text-sm text-gray-200 leading-relaxed">{without}</p>
        </div>

        <div className={`border rounded-xl p-4 ${banner.bg}`}>
          <div className={`text-xs font-semibold uppercase tracking-wider mb-2 ${banner.text}`}>
            With Guardrails
          </div>
          <p className="text-sm text-gray-100 leading-relaxed">{withGuards}</p>
        </div>
      </div>
    </div>
  );
}
