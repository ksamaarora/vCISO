import { z } from 'zod';

// Step-specific schemas for validation
export const step1Schema = z.object({
  companyName: z.string().min(2, "Company name must be at least 2 characters"),
  employeeCount: z.enum(["10-50", "51-200", "201-500", "500+"], {
    message: "Please select an employee count range"
  }),
});

export const step2Schema = z.object({
  industry: z.enum(["healthcare", "finance", "retail", "manufacturing", "tech", "services", "other"], {
    message: "Please select an industry"
  }),
});

export const step3Schema = z.object({
  tools: z.object({
    email: z.array(z.string()).default([]),
    storage: z.array(z.string()).default([]),
    communication: z.array(z.string()).default([]),
    crm: z.array(z.string()).default([]),
  }),
});

export const step4Schema = z.object({
  currentSecurity: z.array(z.string()).default([]),
});

export const step5Schema = z.object({
  mainConcerns: z.array(z.string()).min(1, "Please select at least one security concern"),
});

export const step6Schema = z.object({
  securityLead: z.object({
    type: z.enum(["dedicated", "consultant", "owner", "none"], {
      message: "Please select who handles security"
    }),
    name: z.string().optional(),
  }),
});

// Full schema for final submission
export const onboardingSchema = z.object({
  companyName: z.string().min(2, "Company name must be at least 2 characters"),
  employeeCount: z.enum(["10-50", "51-200", "201-500", "500+"]),
  industry: z.enum(["healthcare", "finance", "retail", "manufacturing", "tech", "services", "other"]),
  tools: z.object({
    email: z.array(z.string()).default([]),
    storage: z.array(z.string()).default([]),
    communication: z.array(z.string()).default([]),
    crm: z.array(z.string()).default([]),
  }),
  currentSecurity: z.array(z.string()).default([]),
  mainConcerns: z.array(z.string()).min(1, "Please select at least one security concern"),
  securityLead: z.object({
    type: z.enum(["dedicated", "consultant", "owner", "none"]),
    name: z.string().optional(),
  }),
});

export type OnboardingData = z.infer<typeof onboardingSchema>;
