'use client';

import { useState } from 'react';
import { useForm, Controller } from 'react-hook-form';
import { zodResolver } from '@hookform/resolvers/zod';
import { 
  onboardingSchema, 
  OnboardingData,
  step1Schema,
  step2Schema,
  step3Schema,
  step4Schema,
  step5Schema,
  step6Schema,
} from '@/lib/validation';
import { generatePlan } from '@/lib/api-client';
import { PlanPreview } from '@/components/plan/PlanPreview';

const TOTAL_STEPS = 6;

const INDUSTRIES = [
  { value: 'healthcare', label: 'Healthcare' },
  { value: 'finance', label: 'Finance' },
  { value: 'retail', label: 'Retail' },
  { value: 'manufacturing', label: 'Manufacturing' },
  { value: 'tech', label: 'Technology' },
  { value: 'services', label: 'Professional Services' },
  { value: 'other', label: 'Other' },
];

const EMAIL_TOOLS = ['Gmail', 'Outlook', 'Other'];
const STORAGE_TOOLS = ['Google Drive', 'Dropbox', 'OneDrive'];
const COMMUNICATION_TOOLS = ['Slack', 'Teams', 'Zoom'];
const CRM_TOOLS = ['Salesforce', 'HubSpot', 'None'];

const SECURITY_OPTIONS = [
  'Multi-factor authentication (MFA)',
  'Antivirus software',
  'Data backups',
  'Security training',
  'None of the above',
];

const CONCERN_OPTIONS = [
  'Ransomware',
  'Phishing attacks',
  'Data breaches',
  'Insider threats',
  'Downtime',
];

export default function CreatePlanPage() {
  const [step, setStep] = useState(1);
  const [isGenerating, setIsGenerating] = useState(false);
  const [generatedPlan, setGeneratedPlan] = useState<string | null>(null);
  const [error, setError] = useState<string | null>(null);

  const {
    register,
    handleSubmit,
    control,
    watch,
    formState: { errors },
    trigger,
    setError: setFormFieldError,
    clearErrors,
  } = useForm<OnboardingData>({
    resolver: zodResolver(onboardingSchema),
    mode: 'onBlur',
    reValidateMode: 'onChange',
    defaultValues: {
      companyName: '',
      employeeCount: undefined as any,
      industry: undefined as any,
      tools: {
        email: [],
        storage: [],
        communication: [],
        crm: [],
      },
      currentSecurity: [],
      mainConcerns: [],
      securityLead: {
        type: undefined as any,
        name: '',
      },
    },
  });

  const watchedValues = watch();

  const handleNext = async () => {
    let stepSchema;
    let fieldsToValidate: (keyof OnboardingData)[] = [];
    
    switch (step) {
      case 1:
        stepSchema = step1Schema;
        fieldsToValidate = ['companyName', 'employeeCount'];
        break;
      case 2:
        stepSchema = step2Schema;
        fieldsToValidate = ['industry'];
        break;
      case 3:
        stepSchema = step3Schema;
        fieldsToValidate = ['tools'];
        break;
      case 4:
        stepSchema = step4Schema;
        fieldsToValidate = ['currentSecurity'];
        break;
      case 5:
        stepSchema = step5Schema;
        fieldsToValidate = ['mainConcerns'];
        break;
      case 6:
        stepSchema = step6Schema;
        fieldsToValidate = ['securityLead'];
        break;
      default:
        return;
    }

    // Get current form values
    const currentValues = watch();
    
    // Extract only the fields we're validating for this step
    const stepData: any = {};
    fieldsToValidate.forEach(field => {
      stepData[field] = currentValues[field];
    });

    // Validate using step-specific schema (not the full schema)
    try {
      stepSchema.parse(stepData);
      // Clear any previous errors
      clearErrors(fieldsToValidate as any);
      setError(null);
      // Move to next step
      setStep(step + 1);
    } catch (err: any) {
      // Show validation errors from Zod
      if (err.errors && err.errors.length > 0) {
        const firstError = err.errors[0];
        const fieldPath = firstError.path.join('.');
        const errorMessage = firstError.message;
        
        // Set form-level error
        setError(errorMessage);
        
        // Set field-level errors for React Hook Form
        if (fieldPath.includes('.')) {
          const [parent, child] = fieldPath.split('.');
          setFormFieldError(parent as any, {
            type: 'validation',
            message: errorMessage,
          });
        } else {
          setFormFieldError(fieldPath as any, {
            type: 'validation',
            message: errorMessage,
          });
        }
      } else {
        setError('Please complete all required fields');
      }
    }
  };

  const handleBack = () => {
    setStep(step - 1);
    setError(null);
  };

  const onSubmit = async (data: OnboardingData) => {
    setIsGenerating(true);
    setError(null);
    try {
      const plan = await generatePlan(data);
      setGeneratedPlan(plan.plan);
    } catch (err) {
      setError(err instanceof Error ? err.message : 'Something went wrong. Please try again.');
    } finally {
      setIsGenerating(false);
    }
  };

  if (generatedPlan) {
    return <PlanPreview markdown={generatedPlan} />;
  }

  return (
    <div className="min-h-screen bg-gradient-to-br from-blue-50 to-indigo-100 py-12 px-4 sm:px-6 lg:px-8">
      <div className="max-w-3xl mx-auto">
        {/* Header */}
        <div className="text-center mb-8">
          <h1 className="text-4xl font-bold text-gray-900 mb-2">
            Create Your Incident Response Plan
          </h1>
          <p className="text-lg text-gray-600">
            This takes about 5 minutes
          </p>
        </div>

        {/* Progress Bar */}
        <div className="mb-8">
          <div className="flex justify-between items-center mb-2">
            <span className="text-sm font-medium text-gray-700">
              Step {step} of {TOTAL_STEPS}
            </span>
            <span className="text-sm text-gray-500">
              {Math.round((step / TOTAL_STEPS) * 100)}% Complete
            </span>
          </div>
          <div className="w-full bg-gray-200 rounded-full h-2.5">
            <div
              className="bg-blue-600 h-2.5 rounded-full transition-all duration-300"
              style={{ width: `${(step / TOTAL_STEPS) * 100}%` }}
            />
          </div>
        </div>

        {/* Form */}
        <form onSubmit={handleSubmit(onSubmit)} className="bg-white rounded-lg shadow-xl p-8">
          {error && (
            <div className="mb-6 p-4 bg-red-50 border border-red-200 rounded-lg">
              <p className="text-red-800 text-sm">{error}</p>
            </div>
          )}

          {/* Step 1: Company Basics */}
          {step === 1 && (
            <div className="space-y-6">
              <div>
                <h2 className="text-2xl font-semibold text-gray-900 mb-2">
                  Great! Let's start with the basics
                </h2>
                <p className="text-gray-600 mb-6">
                  Tell us about your company
                </p>
              </div>

              <div>
                <label className="block text-sm font-medium text-gray-700 mb-2">
                  What's your company name?
                </label>
                <input
                  {...register('companyName')}
                  className="w-full px-4 py-3 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent"
                  placeholder="Acme Corporation"
                />
                {errors.companyName && (
                  <p className="mt-1 text-sm text-red-600">{errors.companyName.message}</p>
                )}
              </div>

              <div>
                <label className="block text-sm font-medium text-gray-700 mb-2">
                  How many employees do you have?
                </label>
                <select
                  {...register('employeeCount')}
                  className="w-full px-4 py-3 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent"
                >
                  <option value="">Select...</option>
                  <option value="10-50">10-50</option>
                  <option value="51-200">51-200</option>
                  <option value="201-500">201-500</option>
                  <option value="500+">500+</option>
                </select>
                {errors.employeeCount && (
                  <p className="mt-1 text-sm text-red-600">{errors.employeeCount.message}</p>
                )}
              </div>
            </div>
          )}

          {/* Step 2: Industry */}
          {step === 2 && (
            <div className="space-y-6">
              <div>
                <h2 className="text-2xl font-semibold text-gray-900 mb-2">
                  What industry are you in?
                </h2>
                <p className="text-gray-600 mb-6">
                  This helps us tailor compliance requirements
                </p>
              </div>

              <div className="space-y-3">
                {INDUSTRIES.map((industry) => (
                  <label
                    key={industry.value}
                    className="flex items-center p-4 border border-gray-300 rounded-lg cursor-pointer hover:bg-blue-50 transition-colors"
                  >
                    <input
                      type="radio"
                      {...register('industry')}
                      value={industry.value}
                      className="mr-3 h-4 w-4 text-blue-600"
                    />
                    <span className="text-gray-700">{industry.label}</span>
                  </label>
                ))}
                {errors.industry && (
                  <p className="text-sm text-red-600">{errors.industry.message}</p>
                )}
              </div>
            </div>
          )}

          {/* Step 3: Technology Tools */}
          {step === 3 && (
            <div className="space-y-6">
              <div>
                <h2 className="text-2xl font-semibold text-gray-900 mb-2">
                  What tools does your team use?
                </h2>
                <p className="text-gray-600 mb-6">
                  Select all that apply
                </p>
              </div>

              <Controller
                name="tools.email"
                control={control}
                render={({ field }) => (
                  <div>
                    <label className="block text-sm font-medium text-gray-700 mb-3">
                      Email
                    </label>
                    <div className="space-y-2">
                      {EMAIL_TOOLS.map((tool) => (
                        <label key={tool} className="flex items-center">
                          <input
                            type="checkbox"
                            checked={field.value?.includes(tool)}
                            onChange={(e) => {
                              const current = field.value || [];
                              if (e.target.checked) {
                                field.onChange([...current, tool]);
                              } else {
                                field.onChange(current.filter((t) => t !== tool));
                              }
                            }}
                            className="mr-2 h-4 w-4 text-blue-600"
                          />
                          <span className="text-gray-700">{tool}</span>
                        </label>
                      ))}
                    </div>
                  </div>
                )}
              />

              <Controller
                name="tools.storage"
                control={control}
                render={({ field }) => (
                  <div>
                    <label className="block text-sm font-medium text-gray-700 mb-3">
                      File Storage
                    </label>
                    <div className="space-y-2">
                      {STORAGE_TOOLS.map((tool) => (
                        <label key={tool} className="flex items-center">
                          <input
                            type="checkbox"
                            checked={field.value?.includes(tool)}
                            onChange={(e) => {
                              const current = field.value || [];
                              if (e.target.checked) {
                                field.onChange([...current, tool]);
                              } else {
                                field.onChange(current.filter((t) => t !== tool));
                              }
                            }}
                            className="mr-2 h-4 w-4 text-blue-600"
                          />
                          <span className="text-gray-700">{tool}</span>
                        </label>
                      ))}
                    </div>
                  </div>
                )}
              />

              <Controller
                name="tools.communication"
                control={control}
                render={({ field }) => (
                  <div>
                    <label className="block text-sm font-medium text-gray-700 mb-3">
                      Communication
                    </label>
                    <div className="space-y-2">
                      {COMMUNICATION_TOOLS.map((tool) => (
                        <label key={tool} className="flex items-center">
                          <input
                            type="checkbox"
                            checked={field.value?.includes(tool)}
                            onChange={(e) => {
                              const current = field.value || [];
                              if (e.target.checked) {
                                field.onChange([...current, tool]);
                              } else {
                                field.onChange(current.filter((t) => t !== tool));
                              }
                            }}
                            className="mr-2 h-4 w-4 text-blue-600"
                          />
                          <span className="text-gray-700">{tool}</span>
                        </label>
                      ))}
                    </div>
                  </div>
                )}
              />

              <Controller
                name="tools.crm"
                control={control}
                render={({ field }) => (
                  <div>
                    <label className="block text-sm font-medium text-gray-700 mb-3">
                      CRM
                    </label>
                    <div className="space-y-2">
                      {CRM_TOOLS.map((tool) => (
                        <label key={tool} className="flex items-center">
                          <input
                            type="checkbox"
                            checked={field.value?.includes(tool)}
                            onChange={(e) => {
                              const current = field.value || [];
                              if (e.target.checked) {
                                field.onChange([...current, tool]);
                              } else {
                                field.onChange(current.filter((t) => t !== tool));
                              }
                            }}
                            className="mr-2 h-4 w-4 text-blue-600"
                          />
                          <span className="text-gray-700">{tool}</span>
                        </label>
                      ))}
                    </div>
                  </div>
                )}
              />
            </div>
          )}

          {/* Step 4: Current Security */}
          {step === 4 && (
            <div className="space-y-6">
              <div>
                <h2 className="text-2xl font-semibold text-gray-900 mb-2">
                  Do you have any of these security measures?
                </h2>
                <p className="text-gray-600 mb-6">
                  Select all that apply
                </p>
              </div>

              <Controller
                name="currentSecurity"
                control={control}
                render={({ field }) => (
                  <div className="space-y-3">
                    {SECURITY_OPTIONS.map((option) => (
                      <label
                        key={option}
                        className="flex items-center p-4 border border-gray-300 rounded-lg cursor-pointer hover:bg-blue-50 transition-colors"
                      >
                        <input
                          type="checkbox"
                          checked={field.value?.includes(option)}
                          onChange={(e) => {
                            const current = field.value || [];
                            if (e.target.checked) {
                              field.onChange([...current, option]);
                            } else {
                              field.onChange(current.filter((s) => s !== option));
                            }
                          }}
                          className="mr-3 h-4 w-4 text-blue-600"
                        />
                        <span className="text-gray-700">{option}</span>
                      </label>
                    ))}
                  </div>
                )}
              />
            </div>
          )}

          {/* Step 5: Main Concerns */}
          {step === 5 && (
            <div className="space-y-6">
              <div>
                <h2 className="text-2xl font-semibold text-gray-900 mb-2">
                  What keeps you up at night?
                </h2>
                <p className="text-gray-600 mb-6">
                  Select at least one security concern
                </p>
              </div>

              <Controller
                name="mainConcerns"
                control={control}
                render={({ field }) => (
                  <div className="space-y-3">
                    {CONCERN_OPTIONS.map((concern) => (
                      <label
                        key={concern}
                        className="flex items-center p-4 border border-gray-300 rounded-lg cursor-pointer hover:bg-blue-50 transition-colors"
                      >
                        <input
                          type="checkbox"
                          checked={field.value?.includes(concern)}
                          onChange={(e) => {
                            const current = field.value || [];
                            if (e.target.checked) {
                              field.onChange([...current, concern]);
                            } else {
                              field.onChange(current.filter((c) => c !== concern));
                            }
                          }}
                          className="mr-3 h-4 w-4 text-blue-600"
                        />
                        <span className="text-gray-700">{concern}</span>
                      </label>
                    ))}
                    {errors.mainConcerns && (
                      <p className="text-sm text-red-600">{errors.mainConcerns.message}</p>
                    )}
                  </div>
                )}
              />
            </div>
          )}

          {/* Step 6: Security Lead */}
          {step === 6 && (
            <div className="space-y-6">
              <div>
                <h2 className="text-2xl font-semibold text-gray-900 mb-2">
                  Who handles IT/security issues?
                </h2>
                <p className="text-gray-600 mb-6">
                  This helps us define the incident response lead
                </p>
              </div>

              <Controller
                name="securityLead.type"
                control={control}
                render={({ field }) => (
                  <div className="space-y-3">
                    <label className="flex items-center p-4 border border-gray-300 rounded-lg cursor-pointer hover:bg-blue-50 transition-colors">
                      <input
                        type="radio"
                        {...field}
                        value="dedicated"
                        className="mr-3 h-4 w-4 text-blue-600"
                      />
                      <span className="text-gray-700">Dedicated IT person</span>
                    </label>
                    {watchedValues.securityLead?.type === 'dedicated' && (
                      <div className="ml-7">
                        <input
                          {...register('securityLead.name')}
                          className="w-full px-4 py-3 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent"
                          placeholder="Name (e.g., Jane Smith)"
                        />
                      </div>
                    )}

                    <label className="flex items-center p-4 border border-gray-300 rounded-lg cursor-pointer hover:bg-blue-50 transition-colors">
                      <input
                        type="radio"
                        {...field}
                        value="consultant"
                        className="mr-3 h-4 w-4 text-blue-600"
                      />
                      <span className="text-gray-700">External consultant</span>
                    </label>

                    <label className="flex items-center p-4 border border-gray-300 rounded-lg cursor-pointer hover:bg-blue-50 transition-colors">
                      <input
                        type="radio"
                        {...field}
                        value="owner"
                        className="mr-3 h-4 w-4 text-blue-600"
                      />
                      <span className="text-gray-700">CEO/Owner</span>
                    </label>

                    <label className="flex items-center p-4 border border-gray-300 rounded-lg cursor-pointer hover:bg-blue-50 transition-colors">
                      <input
                        type="radio"
                        {...field}
                        value="none"
                        className="mr-3 h-4 w-4 text-blue-600"
                      />
                      <span className="text-gray-700">No one specifically</span>
                    </label>
                    {errors.securityLead?.type && (
                      <p className="text-sm text-red-600">{errors.securityLead.type.message}</p>
                    )}
                  </div>
                )}
              />
            </div>
          )}

          {/* Navigation Buttons */}
          <div className="flex justify-between mt-8 pt-6 border-t border-gray-200">
            <button
              type="button"
              onClick={handleBack}
              disabled={step === 1}
              className="px-6 py-3 border border-gray-300 rounded-lg text-gray-700 hover:bg-gray-50 disabled:opacity-50 disabled:cursor-not-allowed transition-colors"
            >
              Back
            </button>

            {step < TOTAL_STEPS ? (
              <button
                type="button"
                onClick={handleNext}
                className="px-6 py-3 bg-blue-600 text-white rounded-lg hover:bg-blue-700 transition-colors"
              >
                Next
              </button>
            ) : (
              <button
                type="submit"
                disabled={isGenerating}
                className="px-6 py-3 bg-green-600 text-white rounded-lg hover:bg-green-700 disabled:opacity-50 disabled:cursor-not-allowed transition-colors"
              >
                {isGenerating ? 'Generating Your Plan...' : 'Generate My IR Plan'}
              </button>
            )}
          </div>
        </form>
      </div>
    </div>
  );
}
