'use client';

import { Gap, GapSeverity } from '@/types';
import { AlertCircle, AlertTriangle, Info, CheckCircle2 } from 'lucide-react';

interface GapCardProps {
  gap: Gap;
}

const severityConfig = {
  [GapSeverity.CRITICAL]: {
    icon: AlertCircle,
    bgColor: 'bg-red-50',
    borderColor: 'border-red-300',
    textColor: 'text-red-800',
    badgeColor: 'bg-red-100 text-red-800',
    label: 'Critical',
  },
  [GapSeverity.HIGH]: {
    icon: AlertTriangle,
    bgColor: 'bg-orange-50',
    borderColor: 'border-orange-300',
    textColor: 'text-orange-800',
    badgeColor: 'bg-orange-100 text-orange-800',
    label: 'High',
  },
  [GapSeverity.MEDIUM]: {
    icon: Info,
    bgColor: 'bg-yellow-50',
    borderColor: 'border-yellow-300',
    textColor: 'text-yellow-800',
    badgeColor: 'bg-yellow-100 text-yellow-800',
    label: 'Medium',
  },
  [GapSeverity.LOW]: {
    icon: CheckCircle2,
    bgColor: 'bg-blue-50',
    borderColor: 'border-blue-300',
    textColor: 'text-blue-800',
    badgeColor: 'bg-blue-100 text-blue-800',
    label: 'Low',
  },
};

export function GapCard({ gap }: GapCardProps) {
  const config = severityConfig[gap.severity];
  const Icon = config.icon;

  return (
    <div
      className={`${config.bgColor} ${config.borderColor} border-2 rounded-lg p-6 mb-4 transition-all hover:shadow-md`}
    >
      {/* Header */}
      <div className="flex items-start justify-between mb-4">
        <div className="flex items-center gap-3">
          <Icon className={`${config.textColor} w-6 h-6`} />
          <div>
            <h3 className="text-lg font-semibold text-gray-900">{gap.section}</h3>
            <span className={`${config.badgeColor} text-xs px-2 py-1 rounded-full font-medium`}>
              {config.label} Priority
            </span>
          </div>
        </div>
        <div className="text-sm text-gray-600 bg-white px-3 py-1 rounded-full border border-gray-200">
          {gap.estimated_effort}
        </div>
      </div>

      {/* Description */}
      <div className="mb-4">
        <h4 className="font-semibold text-gray-900 mb-2">What's Missing:</h4>
        <p className="text-gray-700">{gap.description}</p>
      </div>

      {/* Recommendation */}
      <div className="mb-4 bg-white p-4 rounded-md border border-gray-200">
        <h4 className="font-semibold text-gray-900 mb-2">Recommended Action:</h4>
        <p className="text-gray-700">{gap.recommendation}</p>
      </div>

      {/* Framework References */}
      {gap.framework_references.length > 0 && (
        <div>
          <h4 className="font-semibold text-gray-900 mb-2 text-sm">Framework References:</h4>
          <div className="flex flex-wrap gap-2">
            {gap.framework_references.map((ref, idx) => (
              <span
                key={idx}
                className="text-xs bg-gray-100 text-gray-700 px-2 py-1 rounded border border-gray-300"
              >
                {ref}
              </span>
            ))}
          </div>
        </div>
      )}
    </div>
  );
}