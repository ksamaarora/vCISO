import axios from 'axios';
import { OnboardingData } from './validation';

const API_BASE_URL = process.env.NEXT_PUBLIC_API_URL || 'http://localhost:8000';

export interface PlanResponse {
  success: boolean;
  plan: string;
  metadata: {
    company: string;
    industry: string;
    employee_count: string;
    generated_at: string;
  };
}

export async function generatePlan(data: OnboardingData): Promise<PlanResponse> {
  try {
    const response = await axios.post<PlanResponse>(
      `${API_BASE_URL}/api/v1/plans/generate`,
      data,
      {
        headers: {
          'Content-Type': 'application/json',
        },
      }
    );
    return response.data;
  } catch (error) {
    if (axios.isAxiosError(error)) {
      throw new Error(
        error.response?.data?.detail || 
        error.message || 
        'Failed to generate plan. Please try again.'
      );
    }
    throw error;
  }
}
