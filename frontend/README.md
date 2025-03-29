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

- `POST /api/student/add-student`: Add new student with profile photo
- `GET /api/student/get-students`: List all students
- `GET /api/student/get-classes`: List all classes
- `POST /api/student/process-photo`: Process class photo and blur faces
- `POST /api/student/reset-data`: Reset all data
- `GET /api/student/test-connection`: Test Supabase connection

## Usage

1. Adding a Student:

   - Enter student name and class information
   - Upload profile photo
   - Choose whether to blur face in class photos
   - Click "Add Student" button

2. Processing Class Photo:

   - Select class from dropdown
   - Upload class photo
   - Click "Process Photo" button
   - View processed photo with blurred faces

3. Resetting Data:
   - Click "Reset All Data" button
   - Select "Confirm" in the confirmation dialog
   - All students, photos, and data will be deleted

## Development

### Backend Development

- Creating API endpoints with FastAPI
- Face recognition and blurring operations
- Data management with Supabase
- Environment variable management
- File handling for photos

### Frontend Development

- Creating React components with Material-UI
- Type safety with TypeScript
- API integration
- User interface design
- Photo preview functionality

## License

MIT
