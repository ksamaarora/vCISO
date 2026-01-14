'use client';

import { useState } from 'react';
import { GapAnalysisResult, GapSeverity } from '@/types';
import { GapCard } from '@/components/ui/GapCard';
import { ComplianceScore } from '@/components/ui/ComplianceScore';

interface GapAnalysisReportProps {
  analysis: GapAnalysisResult;
  onBack: () => void;
}

export function GapAnalysisReport({ analysis, onBack }: GapAnalysisReportProps) {
  const [severityFilter, setSeverityFilter] = useState<GapSeverity | 'all'>('all');

  const filteredGaps =
    severityFilter === 'all'
      ? analysis.gaps
      : analysis.gaps.filter((gap) => gap.severity === severityFilter);

  const exportReport = () => {
    // Simple export as JSON (can be enhanced to PDF later)
    const dataStr = JSON.stringify(analysis, null, 2);
    const blob = new Blob([dataStr], { type: 'application/json' });
    const url = URL.createObjectURL(blob);
    const link = document.createElement('a');
    link.href = url;
    link.download = `gap-analysis-${analysis.company_name}-${Date.now()}.json`;
    link.click();
    URL.revokeObjectURL(url);
  };

  return (
    <div className="min-h-screen bg-gray-50 py-12 px-4 sm:px-6 lg:px-8">
      <div className="max-w-7xl mx-auto">
        {/* Header */}
        <div className="mb-8">
          <button
            onClick={onBack}
            className="flex items-center text-blue-600 hover:text-blue-700 mb-4"
          >
            <span className="mr-2">{'←'}</span>
            Back to Plan
          </button>
          <div className="flex justify-between items-start flex-wrap gap-4">
            <div>
              <h1 className="text-4xl font-bold text-gray-900 mb-2">
                Gap Analysis Report
              </h1>
              <p className="text-lg text-gray-600">
                {analysis.company_name} •{' '}
                {new Date(analysis.analysis_timestamp).toLocaleDateString()}
              </p>
            </div>
            <button
              onClick={exportReport}
              className="flex items-center px-4 py-2 bg-blue-600 text-white rounded-lg hover:bg-blue-700 transition-colors"
            >
              <span className="mr-2">⬇️</span>
              Export Report (JSON)
            </button>
          </div>
        </div>

        <div className="grid grid-cols-1 lg:grid-cols-3 gap-8 mb-8">
          {/* Left Column: Compliance Score */}
          <div className="lg:col-span-1">
            <ComplianceScore
              overallScore={analysis.overall_score}
              frameworkCompliance={analysis.framework_compliance}
            />

            {/* Strengths */}
            {analysis.strengths.length > 0 && (
              <div className="bg-green-50 border-2 border-green-300 rounded-lg p-6 mt-6">
                <h3 className="text-xl font-semibold text-green-900 mb-4 flex items-center">
                  <span className="w-5 h-5 mr-2">✅</span>
                  What You're Doing Well
                </h3>
                <ul className="space-y-2">
                  {analysis.strengths.map((strength, idx) => (
                    <li key={idx} className="text-green-800 flex items-start">
                      <span className="mr-2">✓</span>
                      <span>{strength}</span>
                    </li>
                  ))}
                </ul>
              </div>
            )}

            {/* Priority Actions */}
            {analysis.priority_actions.length > 0 && (
              <div className="bg-blue-50 border-2 border-blue-300 rounded-lg p-6 mt-6">
                <h3 className="text-xl font-semibold text-blue-900 mb-4 flex items-center">
                  <span className="w-5 h-5 mr-2">🎯</span>
                  Priority Actions
                </h3>
                <ol className="space-y-3">
                  {analysis.priority_actions.map((action, idx) => (
                    <li key={idx} className="text-blue-800">
                      <span className="font-bold mr-2">{idx + 1}.</span>
                      {action}
                    </li>
                  ))}
                </ol>
              </div>
            )}
          </div>

          {/* Right Column: Gaps */}
          <div className="lg:col-span-2">
            {/* Filter */}
            <div className="bg-white rounded-lg shadow-md p-4 mb-6">
              <div className="flex items-center justify-between flex-wrap gap-4">
                <h3 className="text-lg font-semibold text-gray-900">
                  Identified Gaps ({filteredGaps.length})
                </h3>
                <div className="flex gap-2">
                  <button
                    onClick={() => setSeverityFilter('all')}
                    className={`px-3 py-1 rounded-lg text-sm font-medium transition-colors ${
                      severityFilter === 'all'
                        ? 'bg-gray-800 text-white'
                        : 'bg-gray-200 text-gray-700 hover:bg-gray-300'
                    }`}
                  >
                    All
                  </button>
                  {Object.values(GapSeverity).map((severity) => (
                    <button
                      key={severity}
                      onClick={() => setSeverityFilter(severity)}
                      className={`px-3 py-1 rounded-lg text-sm font-medium transition-colors ${
                        severityFilter === severity
                          ? 'bg-gray-800 text-white'
                          : 'bg-gray-200 text-gray-700 hover:bg-gray-300'
                      }`}
                    >
                      {severity.charAt(0).toUpperCase() + severity.slice(1)}
                    </button>
                  ))}
                </div>
              </div>
            </div>

            {/* Gap Cards */}
            {filteredGaps.length === 0 ? (
              <div className="bg-white rounded-lg shadow-md p-12 text-center">
                <p className="text-gray-500 text-lg">No gaps found in this category</p>
              </div>
            ) : (
              <div>
                {filteredGaps.map((gap) => (
                  <GapCard key={gap.id} gap={gap} />
                ))}
              </div>
            )}
          </div>
        </div>
      </div>
    </div>
  );
}