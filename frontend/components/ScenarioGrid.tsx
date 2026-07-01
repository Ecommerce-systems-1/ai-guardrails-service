import { Scenario } from '../types';

const DECISION_STYLES: Record<string, string> = {
  ALLOW: 'border-green-600 bg-green-950',
  WARN: 'border-yellow-500 bg-yellow-950',
  BLOCK: 'border-red-600 bg-red-950',
};

const DECISION_ICONS: Record<string, string> = {
  ALLOW: '✅',
  WARN: '⚠️',
  BLOCK: '🚫',
};

interface Props {
  scenarios: Scenario[];
  selectedId: string | null;
  onSelect: (scenario: Scenario) => void;
}

export default function ScenarioGrid({ scenarios, selectedId, onSelect }: Props) {
  return (
    <div className="grid grid-cols-2 sm:grid-cols-3 lg:grid-cols-5 gap-3">
      {scenarios.map((s) => (
        <button
          key={s.id}
          onClick={() => onSelect(s)}
          className={`border rounded-lg p-3 text-left transition-all cursor-pointer ${DECISION_STYLES[s.category_tag]} ${
            selectedId === s.id ? 'ring-2 ring-white' : 'opacity-75 hover:opacity-100'
          }`}
        >
          <div className="text-lg mb-1">{DECISION_ICONS[s.category_tag]}</div>
          <div className="text-xs font-semibold text-gray-200 leading-tight">{s.title}</div>
          <div className={`text-xs mt-1 font-bold ${
            s.category_tag === 'BLOCK' ? 'text-red-400' :
            s.category_tag === 'WARN' ? 'text-yellow-400' : 'text-green-400'
          }`}>{s.category_tag}</div>
        </button>
      ))}
    </div>
  );
}
