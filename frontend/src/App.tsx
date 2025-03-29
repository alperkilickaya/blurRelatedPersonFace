import { useState, useEffect } from "react";
import {
  Container,
  Box,
  Typography,
  TextField,
  Button,
  FormControlLabel,
  Checkbox,
  Card,
  CardContent,
  FormControl,
  InputLabel,
  Select,
  MenuItem,
  Dialog,
  DialogTitle,
  DialogContent,
  DialogActions,
  Snackbar,
  Alert,
} from "@mui/material";
import {
  CloudUpload,
  PersonAdd,
  PhotoCamera,
  Delete,
} from "@mui/icons-material";
import { studentService } from "./services/api";
import { Student, StudentResponse } from "./types/student";
import { AxiosError } from "axios";

interface ApiError {
  detail: string;
}

function App() {
  const [classes, setClasses] = useState<string[]>([]);
  const [newStudent, setNewStudent] = useState<Student>({
    name: "",
    class_name: "",
    photo_path: "",
    blur_face: true,
  });
  const [selectedClass, setSelectedClass] = useState("");
  const [selectedPhoto, setSelectedPhoto] = useState<File | null>(null);
  const [resultPhoto, setResultPhoto] = useState<string | null>(null);
  const [profilePhotoUrl, setProfilePhotoUrl] = useState<string | null>(null);
  const [showProfilePhoto, setShowProfilePhoto] = useState(false);
  const [openResetDialog, setOpenResetDialog] = useState(false);
  const [error, setError] = useState<string | null>(null);
  const [openSnackbar, setOpenSnackbar] = useState(false);
  const [snackbarMessage, setSnackbarMessage] = useState("");
  const [snackbarSeverity, setSnackbarSeverity] = useState<"success" | "error">(
    "success"
  );

  useEffect(() => {
    fetchClasses();
  }, []);

  const fetchClasses = async () => {
    try {
      const data = await studentService.getClasses();
      setClasses(data);
    } catch (error) {
      console.error("Error fetching classes:", error);
      setError("Failed to fetch classes");
      setSnackbarMessage("Failed to fetch classes");
      setSnackbarSeverity("error");
      setOpenSnackbar(true);
    }
  };

  const handleAddStudent = async (e: React.FormEvent) => {
    e.preventDefault();
    if (!selectedPhoto) return;

    try {
      await studentService.addStudent(newStudent, selectedPhoto);
      setNewStudent({
        name: "",
        class_name: "",
        photo_path: "",
        blur_face: true,
      });
      setSelectedPhoto(null);
      setProfilePhotoUrl(null);
      setShowProfilePhoto(false);
      fetchClasses();
      setSnackbarMessage("Student added successfully");
      setSnackbarSeverity("success");
      setOpenSnackbar(true);
    } catch (error) {
      console.error("Error adding student:", error);
      setError("Failed to add student");
      setSnackbarMessage("Failed to add student");
      setSnackbarSeverity("error");
      setOpenSnackbar(true);
    }
  };

  const handleProfilePhotoChange = (e: React.ChangeEvent<HTMLInputElement>) => {
    const file = e.target.files?.[0];
    if (file) {
      setSelectedPhoto(file);
      setProfilePhotoUrl(URL.createObjectURL(file));
      setShowProfilePhoto(true);
    }
  };

  const handleProcessPhoto = async () => {
    if (!selectedPhoto || !selectedClass) return;

    try {
      setError(null);
      const response: StudentResponse = await studentService.processPhoto(
        selectedPhoto,
        selectedClass
      );
      setResultPhoto(response.result_path || null);
      setSnackbarMessage("Photo processed successfully!");
      setSnackbarSeverity("success");
      setOpenSnackbar(true);
    } catch (error) {
      console.error("Error processing photo:", error);
      const axiosError = error as AxiosError<ApiError>;
      const errorMessage =
        axiosError.response?.data?.detail ||
        "An error occurred while processing the photo.";
      setError(errorMessage);
      setSnackbarMessage(errorMessage);
      setSnackbarSeverity("error");
      setOpenSnackbar(true);
      setResultPhoto(null);
    }
  };

  const handleReset = async () => {
    try {
      await studentService.resetData();
      setClasses([]);
      setNewStudent({
        name: "",
        class_name: "",
        photo_path: "",
        blur_face: true,
      });
      setSelectedClass("");
      setSelectedPhoto(null);
      setResultPhoto(null);
      setProfilePhotoUrl(null);
      setShowProfilePhoto(false);
      setOpenResetDialog(false);
    } catch (error) {
      console.error("Error resetting data:", error);
    }
  };

  const handleCloseSnackbar = () => {
    setOpenSnackbar(false);
  };

  return (
    <Container maxWidth="lg">
      <Box sx={{ my: 4 }}>
        <Box
          sx={{
            display: "flex",
            justifyContent: "space-between",
            alignItems: "center",
            mb: 4,
          }}
        >
          <Typography variant="h5" component="h1" fontWeight="bold">
            Face Recognition and Blurring System
          </Typography>
          <Button
            variant="outlined"
            color="error"
            startIcon={<Delete />}
            onClick={() => setOpenResetDialog(true)}
          >
            Reset All Data
          </Button>
        </Box>

        {/* Reset Confirmation Dialog */}
        <Dialog
          open={openResetDialog}
          onClose={() => setOpenResetDialog(false)}
        >
          <DialogTitle>Reset All Data</DialogTitle>
          <DialogContent>
            <Typography>
              This action will delete all student photos, class photos, and
              student data. This action cannot be undone. Are you sure you want
              to continue?
            </Typography>
          </DialogContent>
          <DialogActions>
            <Button onClick={() => setOpenResetDialog(false)}>Cancel</Button>
            <Button onClick={handleReset} color="error" variant="contained">
              Reset All Data
            </Button>
          </DialogActions>
        </Dialog>

        {/* Student Addition and Profile */}
        <Box
          sx={{
            display: "grid",
            gridTemplateColumns: { xs: "1fr", md: "1fr 1fr" },
            gap: 4,
            mb: 4,
          }}
        >
          <Card>
            <CardContent>
              <Typography variant="h6" gutterBottom>
                Add New Student
              </Typography>
              <form onSubmit={handleAddStudent}>
                <Box sx={{ display: "grid", gap: 2 }}>
                  <Box
                    sx={{
                      display: "grid",
                      gridTemplateColumns: { xs: "1fr", sm: "1fr 1fr" },
                      gap: 2,
                    }}
                  >
                    <TextField
                      fullWidth
                      label="Full Name"
                      value={newStudent.name}
                      onChange={(e) =>
                        setNewStudent({ ...newStudent, name: e.target.value })
                      }
                      required
                    />
                    <TextField
                      fullWidth
                      label="Class"
                      value={newStudent.class_name}
                      onChange={(e) =>
                        setNewStudent({
                          ...newStudent,
                          class_name: e.target.value,
                        })
                      }
                      required
                    />
                  </Box>
                  <FormControlLabel
                    control={
                      <Checkbox
                        checked={newStudent.blur_face}
                        onChange={(e) =>
                          setNewStudent({
                            ...newStudent,
                            blur_face: e.target.checked,
                          })
                        }
                      />
                    }
                    label="Blur Face"
                  />
                  <Button
                    component="label"
                    variant="outlined"
                    startIcon={<CloudUpload />}
                  >
                    Select Profile Photo
                    <input
                      type="file"
                      hidden
                      accept="image/*"
                      onChange={handleProfilePhotoChange}
                    />
                  </Button>
                  <Button
                    type="submit"
                    variant="contained"
                    startIcon={<PersonAdd />}
                    disabled={!selectedPhoto}
                  >
                    Add Student
                  </Button>
                </Box>
              </form>
            </CardContent>
          </Card>

          {/* Student Profile */}
          {showProfilePhoto && profilePhotoUrl && (
            <Card>
              <CardContent>
                <Typography variant="h6" gutterBottom>
                  Student Profile
                </Typography>
                <Box
                  sx={{
                    width: 200,
                    height: 250,
                    overflow: "hidden",
                    display: "flex",
                    alignItems: "center",
                    justifyContent: "center",
                  }}
                >
                  <img
                    src={profilePhotoUrl}
                    alt="Student profile"
                    style={{
                      width: "100%",
                      height: "100%",
                      objectFit: "cover",
                    }}
                  />
                </Box>
              </CardContent>
            </Card>
          )}
        </Box>

        {/* Photo Processing and Result */}
        <Box
          sx={{
            display: "grid",
            gridTemplateColumns: { xs: "1fr", md: "1fr 1fr" },
            gap: 4,
          }}
        >
          <Card>
            <CardContent>
              <Typography variant="h6" gutterBottom>
                Upload Class Photo
              </Typography>
              <Box sx={{ display: "grid", gap: 2 }}>
                <Box
                  sx={{
                    display: "grid",
                    gridTemplateColumns: { xs: "1fr", sm: "1fr 1fr" },
                    gap: 2,
                  }}
                >
                  <FormControl fullWidth>
                    <InputLabel>Select Class</InputLabel>
                    <Select
                      value={selectedClass}
                      label="Select Class"
                      onChange={(e) => setSelectedClass(e.target.value)}
                    >
                      {classes.map((cls) => (
                        <MenuItem key={cls} value={cls}>
                          {cls}
                        </MenuItem>
                      ))}
                    </Select>
                  </FormControl>
                  <Button
                    component="label"
                    variant="outlined"
                    startIcon={<PhotoCamera />}
                  >
                    Select Class Photo
                    <input
                      type="file"
                      hidden
                      accept="image/*"
                      onChange={(e) =>
                        setSelectedPhoto(e.target.files?.[0] || null)
                      }
                    />
                  </Button>
                </Box>
                <Button
                  variant="contained"
                  onClick={handleProcessPhoto}
                  disabled={!selectedPhoto || !selectedClass}
                >
                  Upload Class Photo
                </Button>
                {error && (
                  <Typography color="error" sx={{ mt: 1 }}>
                    {error}
                  </Typography>
                )}
              </Box>
            </CardContent>
          </Card>

          {/* Processed Photo */}
          {resultPhoto && (
            <Card>
              <CardContent>
                <Typography variant="h6" gutterBottom>
                  Processed Photo
                </Typography>
                <img
                  src={`http://localhost:8000/api/photos/${resultPhoto}`}
                  alt="Processed photo"
                  style={{ maxWidth: 450, height: "auto" }}
                />
              </CardContent>
            </Card>
          )}
        </Box>

        <Snackbar
          open={openSnackbar}
          autoHideDuration={6000}
          onClose={handleCloseSnackbar}
          anchorOrigin={{ vertical: "top", horizontal: "center" }}
        >
          <Alert
            onClose={handleCloseSnackbar}
            severity={snackbarSeverity}
            sx={{ width: "100%" }}
          >
            {snackbarMessage}
          </Alert>
        </Snackbar>
      </Box>
    </Container>
  );
}

export default App;
