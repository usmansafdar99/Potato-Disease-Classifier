# Potato Disease Classification System - Frontend README

Modern, responsive web interface for potato disease classification.

## Directory Structure

```
frontend/
├── index.html               # Main HTML file
├── css/
│   └── style.css           # Complete styling
├── js/
│   └── app.js              # Application logic
└── assets/                 # Images, icons, etc.
```

## Features

### User Interface
- 🎨 Modern, responsive design
- 📱 Mobile-friendly layout
- ⚡ Smooth animations and transitions
- 🎯 Intuitive user experience

### Functionality
- 📤 Drag-and-drop image upload
- 🖼️ Image preview before upload
- 🔍 Real-time prediction display
- 📊 Confidence breakdown visualization
- 💾 Download results as text file
- ♿ Accessible design patterns

### Responsive Breakpoints
- 📺 Desktop (1200px+)
- 💻 Tablet (768px - 1199px)
- 📱 Mobile (480px - 767px)
- 📲 Small Mobile (< 480px)

## Component Structure

### HTML (`index.html`)
- Header with branding
- Upload section with drag-drop
- Preview section
- Results display
- Disease information
- Info cards
- Footer

### CSS (`css/style.css`)
- CSS Variables for theming
- Flexbox/Grid layout
- Animations and transitions
- Responsive media queries
- Print-friendly styles

### JavaScript (`js/app.js`)
- File handling and validation
- API integration
- Dynamic result rendering
- Error management
- Download functionality

## API Integration

Connects to FastAPI backend at:
```
http://localhost:8000/api/v1/predict
```

Request format:
```
POST /api/v1/predict
Content-Type: multipart/form-data

file: <image_file>
```

Response format:
```json
{
  "predicted_class": "Early Blight",
  "confidence": 0.95,
  "confidence_percentage": 95.0,
  "all_predictions": {
    "Early Blight": 0.95,
    "Late Blight": 0.03,
    "Healthy": 0.02
  },
  "timestamp": "2024-01-01T12:00:00"
}
```

## Colors & Theming

- Primary: Green (#10b981)
- Secondary: Blue (#3b82f6)
- Danger: Red (#ef4444)
- Warning: Amber (#f59e0b)

## Usage

1. Open `index.html` in a web browser
2. Upload a potato leaf image via:
   - Click "Select Image" button
   - Drag-and-drop into upload area
3. Click "Analyze Image"
4. View results and recommendations
5. Optionally download results

## Browser Support

- Chrome 90+
- Firefox 88+
- Safari 14+
- Edge 90+

## Performance Considerations

- Optimized CSS with GPU acceleration
- Minimal JavaScript dependencies
- Client-side file validation
- Responsive image handling
- Efficient DOM updates
