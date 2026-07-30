export interface PointDTO {
  x: number;
  y: number;
}

export interface EvaluateRequest {
  func: string;
  points_type: 'equispaced' | 'custom';
  a: number;
  b: number;
  n: number;
  x_eval: number;
  custom_points?: PointDTO[];
}

export interface EvaluateResponse {
  x_eval: number;
  interpolated_value: number;
  derivative_approx: number;
  derivative_exact: number;
  absolute_error: number;
  relative_error: number;
  execution_time: number;
  num_points: number;
}

export interface ExperimentRequest {
  func: string;
  a: number;
  b: number;
  x_eval: number;
  n_values: number[];
  plot_n?: number;
}

export interface ExperimentResultDTO {
  n: number;
  result: number;
  exact_value: number;
  absolute_error: number;
  relative_error: number;
  execution_time: number;
  iterations: number;
}

export interface FunctionPlotPoint {
  x: number;
  f_x: number;
  p_x: number;
}

export interface ExperimentResponse {
  function_name: string;
  a: number;
  b: number;
  x_eval: number;
  results: ExperimentResultDTO[];
  function_plot_data: FunctionPlotPoint[];
  interpolation_points: PointDTO[];
}

export interface FunctionInfo {
  name: string;
  expression: string;
  label: string;
}

export interface FunctionsListResponse {
  functions: FunctionInfo[];
}

export interface BasisStep {
  i: number;
  basis_term: string;
  basis_simplified: string;
  contribution: string;
}

export interface StepsRequest {
  points: PointDTO[];
  x_eval: number;
}

export interface StepsResponse {
  points: PointDTO[];
  steps: BasisStep[];
  polynomial: string;
  derivative: string;
  evaluated: number;
  x_eval: number;
}
