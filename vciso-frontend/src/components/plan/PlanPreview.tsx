import ReactMarkdown from 'react-markdown';
import { jsPDF } from 'jspdf';

export function PlanPreview({ markdown }: { markdown: string }) {
  const exportToPDF = () => {
    const doc = new jsPDF();
    doc.text(markdown, 10, 10);  // Simplified - use html2canvas for better formatting
    doc.save('incident-response-plan.pdf');
  };

  return (
    <div className="max-w-4xl mx-auto p-6">
      <div className="flex justify-between items-center mb-6">
        <h1 className="text-3xl font-bold">Your IR Plan</h1>
        <button 
          onClick={exportToPDF}
          className="bg-blue-600 text-white px-4 py-2 rounded hover:bg-blue-700"
        >
          Export as PDF
        </button>
      </div>
      
      <div className="prose prose-lg max-w-none bg-white p-8 rounded shadow">
        <ReactMarkdown>{markdown}</ReactMarkdown>
      </div>
    </div>
  );
}