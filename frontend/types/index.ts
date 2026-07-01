export interface Scenario {
  id: string;
  title: string;
  category_tag: 'ALLOW' | 'WARN' | 'BLOCK';
  user_input: string;
}

export interface GuardResultOut {
  guard_name: string;
  triggered: boolean;
  severity: 'BLOCK' | 'WARN' | 'PASS';
  violations: string[];
  details: string;
}

export interface AnalysisResponse {
  scenario_id: string;
  user_input: string;
  final_decision: 'BLOCK' | 'WARN' | 'ALLOW';
  input_analysis: GuardResultOut[];
  output_analysis: GuardResultOut[];
  without_guardrails: string;
  with_guardrails: string;
}
