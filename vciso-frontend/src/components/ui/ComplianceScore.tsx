'use client';

import { PieChart, Pie, Cell, ResponsiveContainer, Legend, Tooltip } from 'recharts';

interface ComplianceScoreProps {
  overallScore: number;
  frameworkCompliance: Record<string, number>;
}

export function ComplianceScore({ overallScore, frameworkCompliance }: ComplianceScoreProps) {
  // Prepare data for pie chart
  const chartData = Object.entries(frameworkCompliance).map(([framework, score]) => ({
    name: framework,
    value: score,
  }));

  const COLORS = ['#3b82f6', '#10b981', '#f59e0b'];

  // Determine overall score color
  const getScoreColor = (score: number) => {
    if (score >= 80) return 'text-green-600';
    if (score >= 60) return 'text-yellow-600';
    if (score >= 40) return 'text-orange-600';
    return 'text-red-600';
  };

  const getScoreLabel = (score: number) => {
    if (score >= 80) return 'Excellent';
    if (score >= 60) return 'Good';
    if (score >= 40) return 'Needs Improvement';
    return 'Critical Gaps';
  };

  return (
    <div className="bg-white rounded-lg shadow-md p-6">
      <h2 className="text-2xl font-bold text-gray-900 mb-6">Compliance Score</h2>

      {/* Overall Score */}
      <div className="text-center mb-8">
        <div className={`text-6xl font-bold ${getScoreColor(overallScore)} mb-2`}>
          {overallScore}
          <span className="text-2xl">/100</span>
        </div>
        <div className="text-lg text-gray-600">{getScoreLabel(overallScore)}</div>
      </div>

      {/* Framework Breakdown */}
      <div className="mb-6">
        <h3 className="text-lg font-semibold text-gray-900 mb-4">Framework Breakdown</h3>
        <div className="space-y-3">
          {Object.entries(frameworkCompliance).map(([framework, score]) => (
            <div key={framework}>
              <div className="flex justify-between items-center mb-1">
                <span className="text-sm font-medium text-gray-700">{framework}</span>
                <span className="text-sm font-semibold text-gray-900">{score}/100</span>
              </div>
              <div className="w-full bg-gray-200 rounded-full h-2">
                <div
                  className="bg-blue-600 h-2 rounded-full transition-all duration-500"
                  style={{ width: `${score}%` }}
                />
              </div>
            </div>
          ))}
        </div>
      </div>

      {/* Pie Chart */}
      <div className="h-64">
        <ResponsiveContainer width="100%" height="100%">
          <PieChart>
            <Pie
              data={chartData}
              cx="50%"
              cy="50%"
              labelLine={false}
              label={({ name, value }) => `${name}: ${value}`}
              outerRadius={80}
              fill="#8884d8"
              dataKey="value"
            >
              {chartData.map((entry, index) => (
                <Cell key={`cell-${index}`} fill={COLORS[index % COLORS.length]} />
              ))}
            </Pie>
            <Tooltip />
            <Legend />
          </PieChart>
        </ResponsiveContainer>
      </div>
    </div>
  );
}