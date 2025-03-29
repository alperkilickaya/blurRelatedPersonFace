# Face Recognition App

This application is a web application developed to manage student photos and perform face blurring operations on class photos.

## Features

- Student profile photo upload
- Class photo upload and processing
- Face recognition and blurring
- Class-based student management
- Reset all data functionality
- Supabase integration for data storage

## Technologies

### Backend

- Python 3.8+
- FastAPI
- face_recognition
- OpenCV
- NumPy
- Supabase
- python-dotenv

### Frontend

- React
- TypeScript
- Material-UI
- Vite

## Project Structure

```
.
├── backend/
│   ├── app/
│   │   ├── models/         # Data models
│   │   ├── schemas/        # Pydantic schemas
│   │   ├── controllers/    # Business logic
│   │   ├── routers/        # API endpoints
│   │   ├── services/       # Service layer
│   │   └── main.py         # Main application
│   ├── data/
│   │   ├── profile_photos/ # Student profile photos
│   │   └── class_photos/   # Class photos
│   ├── .env               # Environment variables
│   └── requirements.txt
└── frontend/
    └── src/
        ├── components/     # React components
        ├── services/       # API services
        ├── hooks/         # Custom React hooks
        ├── types/         # TypeScript types
        ├── utils/         # Helper functions
        ├── assets/        # Static files
        └── contexts/      # React contexts
```

## Installation

### Backend

1. Create and activate Python virtual environment:

```bash
cd backend
python -m venv venv
source venv/bin/activate  # Linux/Mac
# or
.\venv\Scripts\activate  # Windows
```

2. Install required packages:

```bash
pip install -r requirements.txt
```

3. Set up environment variables:
   Create a `.env` file in the backend directory with the following variables:

   ```
   SUPABASE_URL=your_project_url
   SUPABASE_ANON_KEY=your_anon_key
   SUPABASE_SERVICE_KEY=your_service_key
   ```

4. Start the application:

```bash
cd backend
uvicorn app.main:app --reload
```

### Frontend

1. Install dependencies:

```bash
cd frontend
npm install
```

2. Start development server:

```bash
npm run dev
```

## API Endpoints

- `POST /api/student/add-student`: Add new student
- `GET /api/student/get-students`: List all students
- `GET /api/student/get-classes`: List all classes
- `POST /api/student/process-photo`: Process class photo
- `POST /api/student/reset-data`: Reset all data
- `GET /api/student/test-connection`: Test Supabase connection

## Usage

1. Adding a Student:

   - Enter student name and class information
   - Upload profile photo
   - Click "Add Student" button

2. Processing Class Photo:

   - Select class
   - Upload class photo
   - Click "Process Photo" button
   - View processed photo

3. Resetting Data:
   - Click "Reset All Data" button
   - Select "Confirm" in the confirmation dialog

## Development

### Backend Development

- Creating API endpoints with FastAPI
- Face recognition and blurring operations
- Data management with Supabase
- Environment variable management

### Frontend Development

- Creating React components with Material-UI
- Type safety with TypeScript
- API integration
- User interface design

## License

MIT
