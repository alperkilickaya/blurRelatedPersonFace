# Yüz Tanıma ve Bulanıklaştırma Sistemi

Bu proje, öğrenci fotoğraflarında yüz tanıma ve bulanıklaştırma işlemlerini gerçekleştiren bir web uygulamasıdır.

## Özellikler

- Öğrenci profil fotoğrafı yükleme
- Sınıf bazlı öğrenci yönetimi
- Yüz tanıma ve bulanıklaştırma
- Sınıf fotoğraflarında otomatik yüz bulanıklaştırma
- Kullanıcı dostu arayüz

## Teknolojiler

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

## Kurulum

### Backend Kurulumu

1. Python bağımlılıklarını yükleyin:

```bash
cd backend
pip install -r requirements.txt
```

2. Backend sunucusunu başlatın:

```bash
uvicorn src.api:app --reload --host 0.0.0.0 --port 8000
```

### Frontend Kurulumu

1. Node.js bağımlılıklarını yükleyin:

```bash
cd frontend
npm install
```

2. Frontend geliştirme sunucusunu başlatın:

```bash
npm run dev
```

## Kullanım

1. Tarayıcınızda `http://localhost:5173` adresine gidin
2. "Yeni Öğrenci Ekle" bölümünden:

   - Öğrenci adı ve sınıf bilgilerini girin
   - Profil fotoğrafı yükleyin
   - "Yüzünü Bulanıklaştır" seçeneğini işaretleyin
   - "Öğrenci Ekle" butonuna tıklayın

3. "Sınıf Fotoğrafı Yükle" bölümünden:
   - Sınıf seçin
   - Sınıf fotoğrafı yükleyin
   - "Sınıf Fotoğrafı Yükle" butonuna tıklayın
   - İşlenmiş fotoğrafı görüntüleyin

## Proje Yapısı

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

- `POST /api/students`: Yeni öğrenci ekleme
- `GET /api/students`: Tüm öğrencileri listeleme
- `POST /api/photos`: Sınıf fotoğrafı işleme
- `GET /api/classes`: Tüm sınıfları listeleme

## Geliştirme

### Backend Geliştirme

- `src/api.py`: API endpoint'leri ve iş mantığı
- `src/face_blur.py`: Yüz tanıma ve bulanıklaştırma işlemleri
- `data/`: Profil ve sınıf fotoğrafları için depolama alanı

### Frontend Geliştirme

- `src/App.tsx`: Ana uygulama bileşeni
- Material-UI bileşenleri ile modern ve responsive tasarım
- TypeScript ile tip güvenliği

## Lisans

Bu proje MIT lisansı altında lisanslanmıştır.
