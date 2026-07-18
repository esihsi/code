# Dan·Moosa Hair Studio – Full-Stack Website

A modern, luxury salon website built with **React 19**, **FastAPI**, and **MongoDB** featuring:
- Service listings with real-time pricing
- Appointment booking system
- Customer testimonials & ratings
- Responsive design with editorial salon aesthetic
- Adaptive

## Quick Start

### Backend Setup
```bash
cd backend

# Install dependencies
pip install -r requirements.txt

# Create .env from example
cp .env.example .env
# Edit .env with your MongoDB URL and database name

# Run server
python server.py
```

Server runs on `http://localhost:8000`

### Frontend Setup
```bash
cd frontend

# Install dependencies
npm install

# Create .env from example
cp .env.example .env
# Edit .env with backend URL (default: http://localhost:8000)

# Development server
npm run dev
```

App runs on `http://localhost:3000`

## Project Structure

```
.
├── backend/
│   ├── server.py           # FastAPI app with all endpoints
│   ├── requirements.txt    # Python dependencies
│   └── .env.example       # Environment template
├── frontend/
│   ├── src/
│   │   ├── pages/
│   │   │   └── HomePage.jsx
│   │   ├── components/
│   │   │   ├── site/
│   │   │   │   ├── Navigation.jsx
│   │   │   │   ├── Hero.jsx
│   │   │   │   ├── Marquee.jsx
│   │   │   │   ├── About.jsx
│   │   │   │   ├── Services.jsx
│   │   │   │   ├── Gallery.jsx
│   │   │   │   ├── Testimonials.jsx
│   │   │   │   ├── BookingForm.jsx
│   │   │   │   ├── Contact.jsx
│   │   │   │   └── Footer.jsx
│   │   │   └── ui/
│   │   ├── App.jsx
│   │   ├── main.jsx
│   │   └── index.css      # Global styles & design system
│   ├── tailwind.config.js # Tailwind config with custom theme
│   ├── postcss.config.js  # PostCSS setup
│   ├── vite.config.js     # Vite bundler config
│   ├── package.json       # NPM dependencies
│   └── .env.example       # Environment template
└── README.md
```

## API Endpoints

- `GET /api/services` – List all services
- `GET /api/reviews` – Salon ratings & reviews
- `POST /api/bookings` – Create appointment
- `GET /api/bookings` – List all bookings
- `POST /api/contact` – Send contact message

## Design System

**Palette:**
- Cream: `#FAF9F6`
- Surface: `#F3EFEA`
- Terracotta (primary): `#9C5B42`
- Deep Olive (secondary): `#4A5340`
- Text: `#1C1B1A`
- Soft Text: `#5C5A56`
- Border: `#E5DFD5`

**Fonts:**
- Display: Cormorant Garamond (light 300, italic accents in terracotta)
- UI/Body: Outfit

**Styling:**
- Sharp corners (border-radius: 0.125rem)
- Asymmetric layouts, generous whitespace
- Subtle grain texture
- Image hover scale (1.06×)
- Uppercase overlines with tight letter-spacing

## Deployment

### Backend
Deploy to Heroku, Railway, or any Node-compatible platform:
```bash
gunicorn server:app
```

### Frontend
Build and deploy static files:
```bash
npm run build
# Upload `dist/` to GitHub Pages, Vercel, or Netlify
```

## Testing

All interactive elements include `data-testid` attributes for automated testing:
- Navigation: `nav-header`, `nav-book-btn`
- Hero: `hero-heading`, `hero-book-btn`
- Services: `service-item-{id}`
- Booking: `booking-form`, `booking-name`, `booking-phone`, etc.

## Contact

**Dan·Moosa Hair Studio**
- 📍 Krishnarajapuram, Bengaluru, Karnataka 560067
- 📞 088844 47703
- 🕒 9 AM – 9 PM, Daily
- ⭐ 4.7/5 (85+ reviews on Justdial & Google)
