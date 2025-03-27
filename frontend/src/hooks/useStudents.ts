import { useState, useEffect } from "react";
import { Student } from "../types/student";
import { studentService } from "../services/api";

export const useStudents = () => {
  const [students, setStudents] = useState<Record<string, Student>>({});
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);

  const fetchStudents = async () => {
    try {
      setLoading(true);
      const data = await studentService.getStudents();
      setStudents(data);
      setError(null);
    } catch (err) {
      setError(err instanceof Error ? err.message : "Failed to fetch students");
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    fetchStudents();
  }, []);

  const addStudent = async (student: Student, photo: File) => {
    try {
      await studentService.addStudent(student, photo);
      await fetchStudents(); // Refresh the list
      return true;
    } catch (err) {
      setError(err instanceof Error ? err.message : "Failed to add student");
      return false;
    }
  };

  return {
    students,
    loading,
    error,
    addStudent,
    refreshStudents: fetchStudents,
  };
};
