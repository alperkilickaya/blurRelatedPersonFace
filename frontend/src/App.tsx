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
} from "@mui/material";
import { CloudUpload, PersonAdd, PhotoCamera } from "@mui/icons-material";
import axios from "axios";

interface Student {
  name: string;
  class_name: string;
  blur_face: boolean;
}

function App() {
  const [classes, setClasses] = useState<string[]>([]);
  const [newStudent, setNewStudent] = useState<Student>({
    name: "",
    class_name: "",
    blur_face: true,
  });
  const [selectedClass, setSelectedClass] = useState("");
  const [selectedPhoto, setSelectedPhoto] = useState<File | null>(null);
  const [resultPhoto, setResultPhoto] = useState<string | null>(null);
  const [profilePhotoUrl, setProfilePhotoUrl] = useState<string | null>(null);
  const [showProfilePhoto, setShowProfilePhoto] = useState(false);

  useEffect(() => {
    fetchClasses();
  }, []);

  const fetchClasses = async () => {
    try {
      const response = await axios.get("http://localhost:8000/api/classes");
      setClasses(response.data);
    } catch (error) {
      console.error("Error fetching classes:", error);
    }
  };

  const handleAddStudent = async (e: React.FormEvent) => {
    e.preventDefault();
    const formData = new FormData();
    formData.append("student_data", JSON.stringify(newStudent));
    formData.append("photo", selectedPhoto as File);

    try {
      await axios.post("http://localhost:8000/api/students", formData);
      setNewStudent({ name: "", class_name: "", blur_face: true });
      setSelectedPhoto(null);
      setProfilePhotoUrl(null);
      setShowProfilePhoto(false);
      fetchClasses();
    } catch (error) {
      console.error("Error adding student:", error);
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

    const formData = new FormData();
    formData.append("photo", selectedPhoto);
    formData.append("class_name", selectedClass);

    try {
      const response = await axios.post(
        "http://localhost:8000/api/photos",
        formData
      );
      setResultPhoto(response.data.result_path);
    } catch (error) {
      console.error("Error processing photo:", error);
    }
  };

  return (
    <Container maxWidth="lg">
      <Box sx={{ my: 4 }}>
        <Typography variant="h4" component="h1" gutterBottom>
          Yüz Tanıma ve Bulanıklaştırma Sistemi
        </Typography>

        {/* Öğrenci Ekleme ve Profil */}
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
                Yeni Öğrenci Ekle
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
                      label="Ad Soyad"
                      value={newStudent.name}
                      onChange={(e) =>
                        setNewStudent({ ...newStudent, name: e.target.value })
                      }
                      required
                    />
                    <TextField
                      fullWidth
                      label="Sınıf"
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
                    label="Yüzünü Bulanıklaştır"
                  />
                  <Button
                    component="label"
                    variant="outlined"
                    startIcon={<CloudUpload />}
                  >
                    Profil Fotoğrafı Seç
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
                    Öğrenci Ekle
                  </Button>
                </Box>
              </form>
            </CardContent>
          </Card>

          {/* Öğrenci Profili */}
          {showProfilePhoto && profilePhotoUrl && (
            <Card>
              <CardContent>
                <Typography variant="h6" gutterBottom>
                  Öğrenci Profili
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
                    alt="Öğrenci profili"
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

        {/* Fotoğraf İşleme ve Sonuç */}
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
                Sınıf Fotoğrafı Yükle
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
                    <InputLabel>Sınıf Seç</InputLabel>
                    <Select
                      value={selectedClass}
                      label="Sınıf Seç"
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
                    Sınıf Fotoğrafı Seç
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
                  Sınıf Fotoğrafı Yükle
                </Button>
              </Box>
            </CardContent>
          </Card>

          {/* İşlenmiş Fotoğraf */}
          {resultPhoto && (
            <Card>
              <CardContent>
                <Typography variant="h6" gutterBottom>
                  İşlenmiş Fotoğraf
                </Typography>
                <img
                  src={`http://localhost:8000/api/photos/${resultPhoto}`}
                  alt="İşlenmiş fotoğraf"
                  style={{ maxWidth: "100%", height: "auto" }}
                />
              </CardContent>
            </Card>
          )}
        </Box>
      </Box>
    </Container>
  );
}

export default App;
