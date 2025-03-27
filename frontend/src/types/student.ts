export interface Student {
  name: string;
  class_name: string;
  photo_path: string;
  blur_face: boolean;
}

export interface StudentResponse {
  message?: string;
  result_path?: string;
  error?: string;
}
