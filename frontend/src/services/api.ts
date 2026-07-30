import axios from 'axios';
import type {
  EvaluateRequest,
  EvaluateResponse,
  ExperimentRequest,
  ExperimentResponse,
  FunctionsListResponse,
  StepsRequest,
  StepsResponse,
} from '../types/lagrange';

const API_BASE = '/api/v1/lagrange';

const client = axios.create({
  baseURL: API_BASE,
  timeout: 30000,
});

export async function fetchFunctions(): Promise<FunctionsListResponse> {
  const { data } = await client.get<FunctionsListResponse>('/functions');
  return data;
}

export async function evaluateDerivative(
  req: EvaluateRequest
): Promise<EvaluateResponse> {
  const { data } = await client.post<EvaluateResponse>('/evaluate', req);
  return data;
}

export async function runExperiment(
  req: ExperimentRequest
): Promise<ExperimentResponse> {
  const { data } = await client.post<ExperimentResponse>('/experiment', req);
  return data;
}

export async function computeSteps(
  req: StepsRequest
): Promise<StepsResponse> {
  const { data } = await client.post<StepsResponse>('/steps', req);
  return data;
}
