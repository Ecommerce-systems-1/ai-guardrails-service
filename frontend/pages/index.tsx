import { useState, useEffect } from 'react';
import type { Scenario, AnalysisResponse } from '../types';
import ScenarioGrid from '../components/ScenarioGrid';
import GuardPipelineView from '../components/GuardPipelineView';
import ComparisonPanel from '../components/ComparisonPanel';

export default function Home() {
  const [scenarios, setScenarios] = useState<Scenario[]>([]);
  const [selectedScenario, setSelectedScenario] = useState<Scenario | null>(null);
  const [analysis, setAnalysis] = useState<AnalysisResponse | null>(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    fetch('/scenarios')
      .then((r) => r.json())
      .then((d) => {
        if (d.scenarios && Array.isArray(d.scenarios)) {
          setScenarios(d.scenarios);
        } else {
          setError('Invalid scenarios response from server');
        }
      })
      .catch(() => setError('Failed to load scenarios'));
  }, []);

  async function handleSelect(scenario: Scenario) {
    setSelectedScenario(scenario);
    setAnalysis(null);
    setError(null);
    setLoading(true);
    try {
      const resp = await fetch('/analyze', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ scenario_id: scenario.id, user_input: scenario.user_input }),
      });
      if (!resp.ok) {
        throw new Error(`Server error: ${resp.status}`);
      }
      const data: AnalysisResponse = await resp.json();
      setAnalysis(data);
    } catch (err) {
      setError(err instanceof Error ? err.message : 'Analysis request failed');
    } finally {
      setLoading(false);
    }
  }

  return (
    <div className="min-h-screen bg-gray-950 text-gray-100 p-6 max-w-6xl mx-auto">
      <header className="mb-8">
        <h1 className="text-3xl font-bold">🛡️ AI Guardrails Service</h1>
        <p className="text-gray-400 mt-1">
          Live guard detection · Pre-computed responses · Zero API cost
        </p>
      </header>

      <section className="mb-6">
        <h2 className="text-sm font-semibold text-gray-400 uppercase tracking-wider mb-3">
          Select a Scenario
        </h2>
        <ScenarioGrid
          scenarios={scenarios}
          selectedId={selectedScenario?.id ?? null}
          onSelect={handleSelect}
        />
      </section>

      {error && (
        <div className="bg-red-900 border border-red-600 rounded-lg px-4 py-3 text-red-200 text-sm mb-4">
          {error}
        </div>
      )}

      {loading && (
        <div className="text-center text-gray-400 py-12">Running guardrail checks...</div>
      )}

      {analysis && selectedScenario && !loading && (
        <>
          <section className="mb-6 bg-gray-900 rounded-xl p-4">
            <div className="text-sm text-gray-400 mb-1">User Input</div>
            <div className="font-mono text-sm text-white">{analysis.user_input}</div>
          </section>

          <section className="mb-6">
            <h2 className="text-sm font-semibold text-gray-400 uppercase tracking-wider mb-3">
              Input Guard Pipeline
            </h2>
            <GuardPipelineView results={analysis.input_analysis} phase="input" />
          </section>

          {analysis.output_analysis.length > 0 && (
            <section className="mb-6">
              <h2 className="text-sm font-semibold text-gray-400 uppercase tracking-wider mb-3">
                Output Guard Pipeline
              </h2>
              <GuardPipelineView results={analysis.output_analysis} phase="output" />
            </section>
          )}

          <section>
            <ComparisonPanel
              without={analysis.without_guardrails}
              withGuards={analysis.with_guardrails}
              decision={analysis.final_decision}
            />
          </section>
        </>
      )}
    </div>
  );
}
