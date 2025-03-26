# Face Recognition and Blurring System

This project is a web application that performs face recognition and blurring operations on student photos.

## Features

- Student profile photo upload
- Class-based student management
- Face recognition and blurring
- Automatic face blurring in class photos
- User-friendly interface

## Technologies

### Backend

- Python 3.8+
- FastAPI
- OpenCV
- face_recognition
- NumPy

### Frontend

- React
- TypeScript
- Material-UI
- Axios

## Installation

### Backend Setup

1. Install Python dependencies:

```bash
cd backend
pip install -r requirements.txt
```

2. Start the backend server:

```bash
uvicorn src.api:app --reload --host 0.0.0.0 --port 8000
```

### Frontend Setup

1. Install Node.js dependencies:

```bash
cd frontend
npm install
```

2. Start the frontend development server:

```bash
npm run dev
```

## Usage

1. Open `http://localhost:5173` in your browser
2. From the "Add New Student" section:

   - Enter student name and class information
   - Upload profile photo
   - Check "Blur Face" option
   - Click "Add Student"

3. From the "Upload Class Photo" section:
   - Select class
   - Upload class photo
   - Click "Upload Class Photo"
   - View the processed photo

## Project Structure

```
.
├── backend/
│   ├── src/
│   │   ├── api.py
│   │   ├── face_blur.py
│   │   └── __init__.py
│   ├── data/
│   │   ├── profile_photos/
│   │   └── class_photos/
│   └── requirements.txt
└── frontend/
    ├── src/
    │   ├── App.tsx
    │   └── main.tsx
    ├── package.json
    └── tsconfig.json
```

## API Endpoints

- `POST /api/students`: Add new student
- `GET /api/students`: List all students
- `POST /api/photos`: Process class photo
- `GET /api/classes`: List all classes

## Development

### Backend Development

- `src/api.py`: API endpoints and business logic
- `src/face_blur.py`: Face recognition and blurring operations
- `data/`: Storage area for profile and class photos

### Frontend Development

- `src/App.tsx`: Main application component
- Modern and responsive design with Material-UI components
- Type safety with TypeScript

## License

This project is licensed under the MIT License.
