import { Student, StudentResponse } from "../types/student";

const API_BASE_URL = "http://localhost:8000/api";

export const studentService = {
  async addStudent(student: Student, photo: File): Promise<StudentResponse> {
    const formData = new FormData();
    formData.append("student_data", JSON.stringify(student));
    formData.append("photo", photo);

    const response = await fetch(`${API_BASE_URL}/student/add-student`, {
      method: "POST",
      body: formData,
    });

    if (!response.ok) {
      const error = await response.json();
      throw new Error(error.detail || "Failed to add student");
    }

    return response.json();
  },

  async getStudents(): Promise<Record<string, Student>> {
    const response = await fetch(`${API_BASE_URL}/student/get-students`);

    if (!response.ok) {
      throw new Error("Failed to fetch students");
    }

    return response.json();
  },

  async getClasses(): Promise<string[]> {
    const response = await fetch(`${API_BASE_URL}/student/get-classes`);

    if (!response.ok) {
      throw new Error("Failed to fetch classes");
    }

    return response.json();
  },

  async processPhoto(photo: File, className: string): Promise<StudentResponse> {
    const formData = new FormData();
    formData.append("photo", photo);
    formData.append("class_name", className);

    const response = await fetch(`${API_BASE_URL}/student/process-photo`, {
      method: "POST",
      body: formData,
    });

    if (!response.ok) {
      const error = await response.json();
      throw new Error(error.detail || "Failed to process photo");
    }

    return response.json();
  },

  async resetData(): Promise<StudentResponse> {
    const response = await fetch(`${API_BASE_URL}/student/reset-data`, {
      method: "POST",
    });

    if (!response.ok) {
      const error = await response.json();
      throw new Error(error.detail || "Failed to reset data");
    }

    return response.json();
  },
};
