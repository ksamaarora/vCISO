'use client';

import ReactMarkdown from 'react-markdown';
import { useState } from 'react';
import html2canvas from 'html2canvas';
import { jsPDF } from 'jspdf';
import { analyzeGaps } from '@/lib/api-client';
import { GapAnalysisReport } from './GapAnalysisReport';
import { GapAnalysisResult } from '@/types';

interface PlanPreviewProps {
  markdown: string;
  companyName: string;
}

export function PlanPreview({ markdown, companyName }: PlanPreviewProps) {
  const [isExporting, setIsExporting] = useState(false);
  const [isAnalyzing, setIsAnalyzing] = useState(false);
  const [gapAnalysis, setGapAnalysis] = useState<GapAnalysisResult | null>(null);
  const [error, setError] = useState<string | null>(null);

  const exportToPDF = async () => {
    setIsExporting(true);
    try {
      const element = document.getElementById('plan-content');
      if (!element) {
        alert('Could not find plan content to export');
        return;
      }

      const canvas = await html2canvas(element, {
        scale: 2,
        useCORS: true,
        logging: false,
      });

      const imgData = canvas.toDataURL('image/png');
      const pdf = new jsPDF('p', 'mm', 'a4');
      const pdfWidth = pdf.internal.pageSize.getWidth();
      const pdfHeight = pdf.internal.pageSize.getHeight();
      const imgWidth = canvas.width;
      const imgHeight = canvas.height;
      const ratio = Math.min(pdfWidth / imgWidth, pdfHeight / imgHeight);
      const imgScaledWidth = imgWidth * ratio;
      const imgScaledHeight = imgHeight * ratio;
      const xOffset = (pdfWidth - imgScaledWidth) / 2;
      const yOffset = 0;

      const pageHeight = imgScaledHeight;
      let heightLeft = pageHeight;

      let position = yOffset;

      pdf.addImage(imgData, 'PNG', xOffset, position, imgScaledWidth, imgScaledHeight);
      heightLeft -= pdfHeight;

      while (heightLeft > 0) {
        position = heightLeft - pageHeight;
        pdf.addPage();
        pdf.addImage(imgData, 'PNG', xOffset, position, imgScaledWidth, imgScaledHeight);
        heightLeft -= pdfHeight;
      }

      pdf.save('incident-response-plan.pdf');
    } catch (error) {
      console.error('Error exporting PDF:', error);
      alert('Failed to export PDF. Please try again.');
    } finally {
      setIsExporting(false);
    }
  };

  const copyToClipboard = () => {
    navigator.clipboard.writeText(markdown);
    alert('Plan copied to clipboard!');
  };

  const handleAnalyzeGaps = async () => {
    setIsAnalyzing(true);
    setError(null);
    try {
      const response = await analyzeGaps(markdown, companyName);
      setGapAnalysis(response.gap_analysis);
    } catch (err) {
      setError(err instanceof Error ? err.message : 'Failed to analyze plan');
    } finally {
      setIsAnalyzing(false);
    }
  };

  // If gap analysis is complete, show the report from iteration 2
  if (gapAnalysis) {
    return (
      <GapAnalysisReport
        analysis={gapAnalysis}
        onBack={() => setGapAnalysis(null)}
      />
    );
  }

  // Default view: iteration 1 plan preview + iteration 2 actions
  return (
    <div className="min-h-screen bg-gray-50 py-12 px-4 sm:px-6 lg:px-8">
      <div className="max-w-5xl mx-auto">
        {/* Header */}
        <div className="bg-white rounded-lg shadow-md p-6 mb-6">
          <div className="flex justify-between items-center flex-wrap gap-4">
            <div>
              <h1 className="text-3xl font-bold text-gray-900 mb-2">
                Your Incident Response Plan
              </h1>
              <p className="text-gray-600">
                Your customized plan is ready to use
              </p>
            </div>
            <div className="flex gap-3">
              <button
                onClick={copyToClipboard}
                className="px-4 py-2 border border-gray-300 rounded-lg text-gray-700 hover:bg-gray-50 transition-colors"
              >
                Copy Text
              </button>
              <button
                onClick={exportToPDF}
                disabled={isExporting}
                className="px-6 py-2 bg-gray-600 text-white rounded-lg hover:bg-gray-700 disabled:opacity-50 disabled:cursor-not-allowed transition-colors"
              >
                {isExporting ? 'Exporting...' : 'Export as PDF'}
              </button>
              <button
                onClick={handleAnalyzeGaps}
                disabled={isAnalyzing}
                className="px-6 py-2 bg-blue-600 text-white rounded-lg hover:bg-blue-700 disabled:opacity-50 transition-colors flex items-center"
              >
                {isAnalyzing ? 'Analyzing…' : 'Analyze My Plan'}
              </button>
            </div>
          </div>

          {/* Error Message */}
          {error && (
            <div className="mt-4 p-4 bg-red-50 border border-red-200 rounded-lg">
              <p className="text-red-800 text-sm">{error}</p>
            </div>
          )}
        </div>

        {/* Plan Content with styled Markdown (from iteration 1) */}
        <div
          id="plan-content"
          className="bg-white rounded-lg shadow-md p-8 prose prose-lg max-w-none"
        >
          <ReactMarkdown
            components={{
              h1: ({ node, ...props }) => (
                <h1 className="text-3xl font-bold text-gray-900 mt-8 mb-4" {...props} />
              ),
              h2: ({ node, ...props }) => (
                <h2 className="text-2xl font-semibold text-gray-800 mt-6 mb-3" {...props} />
              ),
              h3: ({ node, ...props }) => (
                <h3 className="text-xl font-semibold text-gray-700 mt-4 mb-2" {...props} />
              ),
              p: ({ node, ...props }) => (
                <p className="text-gray-700 mb-4 leading-relaxed" {...props} />
              ),
              ul: ({ node, ...props }) => (
                <ul className="list-disc list-inside mb-4 space-y-2 text-gray-700" {...props} />
              ),
              ol: ({ node, ...props }) => (
                <ol className="list-decimal list-inside mb-4 space-y-2 text-gray-700" {...props} />
              ),
              li: ({ node, ...props }) => (
                <li className="ml-4" {...props} />
              ),
              strong: ({ node, ...props }) => (
                <strong className="font-semibold text-gray-900" {...props} />
              ),
              code: ({ node, ...props }) => (
                <code className="bg-gray-100 px-2 py-1 rounded text-sm font-mono" {...props} />
              ),
            }}
          >
            {markdown}
          </ReactMarkdown>
        </div>

        {/* Back Button */}
        <div className="mt-8 text-center">
          <button
            onClick={() => window.location.reload()}
            className="px-6 py-3 bg-gray-600 text-white rounded-lg hover:bg-gray-700 transition-colors"
          >
            Create Another Plan
          </button>
        </div>
      </div>
    </div>
  );
}

