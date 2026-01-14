// frontend/types/index.ts

export enum GapSeverity {
  CRITICAL = 'critical',
  HIGH = 'high',
  MEDIUM = 'medium',
  LOW = 'low',
}

export interface Gap {
  id: string;
  section: string;
  severity: GapSeverity;
  description: string;
  recommendation: string;
  framework_references: string[];
  estimated_effort: string;
}

export interface GapAnalysisResult {
  company_name: string;
  analysis_timestamp: string;
  overall_score: number;
  gaps: Gap[];
  strengths: string[];
  priority_actions: string[];
  framework_compliance: Record<string, number>;
  enhanced_plan?: string;
}

export interface GapAnalysisResponse {
  success: boolean;
  gap_analysis: GapAnalysisResult;
}