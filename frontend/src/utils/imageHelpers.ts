export const getImageUrl = (path: string): string => {
  if (!path) return "";
  return `http://localhost:8000/api/photos/${path}`;
};

export const validateImageFile = (file: File): boolean => {
  const validTypes = ["image/jpeg", "image/png", "image/jpg"];
  return validTypes.includes(file.type);
};

export const formatFileSize = (bytes: number): string => {
  if (bytes === 0) return "0 Bytes";
  const k = 1024;
  const sizes = ["Bytes", "KB", "MB", "GB"];
  const i = Math.floor(Math.log(bytes) / Math.log(k));
  return `${parseFloat((bytes / Math.pow(k, i)).toFixed(2))} ${sizes[i]}`;
};
