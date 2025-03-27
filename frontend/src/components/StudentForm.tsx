import React, { useState } from "react";
import { Student } from "../types/student";

interface StudentFormProps {
  onSubmit: (student: Student, photo: File) => Promise<void>;
  classes: string[];
}

export const StudentForm: React.FC<StudentFormProps> = ({
  onSubmit,
  classes,
}) => {
  const [formData, setFormData] = useState<Student>({
    name: "",
    class_name: "",
    photo_path: "",
    blur_face: true,
  });
  const [photo, setPhoto] = useState<File | null>(null);

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    if (photo) {
      await onSubmit(formData, photo);
      // Reset form
      setFormData({
        name: "",
        class_name: "",
        photo_path: "",
        blur_face: true,
      });
      setPhoto(null);
    }
  };

  const handleChange = (
    e: React.ChangeEvent<HTMLInputElement | HTMLSelectElement>
  ) => {
    const { name, value, type } = e.target;
    setFormData((prev) => ({
      ...prev,
      [name]:
        type === "checkbox" ? (e.target as HTMLInputElement).checked : value,
    }));
  };

  const handlePhotoChange = (e: React.ChangeEvent<HTMLInputElement>) => {
    if (e.target.files && e.target.files[0]) {
      setPhoto(e.target.files[0]);
    }
  };

  return (
    <form onSubmit={handleSubmit} className="space-y-4">
      <div>
        <label className="block text-sm font-medium text-gray-700">
          Name
          <input
            type="text"
            name="name"
            value={formData.name}
            onChange={handleChange}
            required
            className="mt-1 block w-full rounded-md border-gray-300 shadow-sm"
          />
        </label>
      </div>

      <div>
        <label className="block text-sm font-medium text-gray-700">
          Class
          <select
            name="class_name"
            value={formData.class_name}
            onChange={handleChange}
            required
            className="mt-1 block w-full rounded-md border-gray-300 shadow-sm"
          >
            <option value="">Select a class</option>
            {classes.map((className) => (
              <option key={className} value={className}>
                {className}
              </option>
            ))}
          </select>
        </label>
      </div>

      <div>
        <label className="block text-sm font-medium text-gray-700">
          Photo
          <input
            type="file"
            accept="image/*"
            onChange={handlePhotoChange}
            required
            className="mt-1 block w-full"
          />
        </label>
      </div>

      <div>
        <label className="flex items-center space-x-2">
          <input
            type="checkbox"
            name="blur_face"
            checked={formData.blur_face}
            onChange={handleChange}
            className="rounded border-gray-300 text-indigo-600"
          />
          <span className="text-sm font-medium text-gray-700">
            Blur face in class photos
          </span>
        </label>
      </div>

      <button
        type="submit"
        className="w-full bg-indigo-600 text-white py-2 px-4 rounded-md hover:bg-indigo-700"
      >
        Add Student
      </button>
    </form>
  );
};
