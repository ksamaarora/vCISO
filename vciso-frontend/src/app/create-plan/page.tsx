// /app/create-plan/page.tsx
'use client';

import { useState } from 'react';
import { useForm } from 'react-hook-form';
import { zodResolver } from '@hookform/resolvers/zod';
import { onboardingSchema, OnboardingData } from '@/lib/validation';
import { generatePlan } from '@/lib/api-client';

export default function CreatePlanPage() {
  const [step, setStep] = useState(1);
  const [isGenerating, setIsGenerating] = useState(false);
  const [generatedPlan, setGeneratedPlan] = useState<string | null>(null);

  const { register, handleSubmit, formState: { errors } } = useForm<OnboardingData>({
    resolver: zodResolver(onboardingSchema),
  });

  const onSubmit = async (data: OnboardingData) => {
    setIsGenerating(true);
    try {
      const plan = await generatePlan(data);
      setGeneratedPlan(plan.plan);
    } catch (error) {
      console.error('Failed to generate plan:', error);
      alert('Something went wrong. Please try again.');
    } finally {
      setIsGenerating(false);
    }
  };

  if (generatedPlan) {
    return <PlanPreview markdown={generatedPlan} />;
  }

  return (
    <div className="max-w-2xl mx-auto p-6">
      <h1 className="text-3xl font-bold mb-6">Create Your IR Plan</h1>
      <p className="text-gray-600 mb-8">This will take about 5 minutes.</p>
      
      <form onSubmit={handleSubmit(onSubmit)} className="space-y-6">
        {/* Step 1: Company Basics */}
        {step === 1 && (
          <div>
            <label className="block text-sm font-medium mb-2">Company Name</label>
            <input 
              {...register('companyName')} 
              className="w-full border rounded px-3 py-2"
              placeholder="Acme Corp"
            />
            {errors.companyName && (
              <p className="text-red-500 text-sm mt-1">{
                errors.companyName.message}</p>
)}
                <label className="block text-sm font-medium mb-2 mt-4">Number of Employees</label>
                <select {...register('employeeCount')} className="w-full border rounded px-3 py-2">
          <option value="">Select...</option>
          <option value="10-50">10-50</option>
          <option value="51-200">51-200</option>
          <option value="201-500">201-500</option>
        </select>
        
        <button 
          type="button" 
          onClick={() => setStep(2)}
          className="mt-6 bg-blue-600 text-white px-6 py-2 rounded hover:bg-blue-700"
        >
          Next
        </button>
      </div>
    )}
    
    {/* Add steps 2-6 similarly */}
    
    {/* Final step: Submit */}
    {step === 6 && (
      <button 
        type="submit" 
        disabled={isGenerating}
        className="w-full bg-green-600 text-white px-6 py-3 rounded hover:bg-green-700 disabled:bg-gray-400"
      >
        {isGenerating ? 'Generating Your Plan...' : 'Generate My IR Plan'}
      </button>
    )}
  </form>
</div>
    );
}