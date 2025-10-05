# Django GeoJSON Map Manager

A Django application for managing and displaying GeoJSON files with an interactive map interface.

## Features

- 📁 Upload and manage GeoJSON files
- 🎨 Color customization for each layer
- 🗺️ Interactive map with layer controls
- 📱 Responsive admin dashboard
- 🔄 Real-time updates between dashboard and embedded map
- 🌍 Embeddable map widget

## Deployment on Vercel

This project is configured for easy deployment on Vercel's free tier.

### Prerequisites

1. Create a [Vercel account](https://vercel.com/)
2. Install [Vercel CLI](https://vercel.com/cli) (optional)
3. Have your project in a Git repository (GitHub, GitLab, etc.)

### Deploy Steps

#### Option 1: Deploy via Vercel Dashboard (Recommended)

1. Go to [Vercel Dashboard](https://vercel.com/dashboard)
2. Click "New Project"
3. Import your Git repository
4. Vercel will automatically detect the Django project
5. Click "Deploy"

#### Option 2: Deploy via CLI

```bash
# Install Vercel CLI
npm i -g vercel

# Deploy from project directory
cd your-project-directory
vercel

# Follow the prompts
```

### Environment Variables

Set these in your Vercel dashboard:

- `DEBUG`: `False` (for production)
- `SECRET_KEY`: Your Django secret key

### Post-Deployment Setup

After deployment, access your admin dashboard:
- URL: `https://your-app.vercel.app/dashboard/`
- Default admin credentials: `admin` / `admin123`
- **Important**: Change the admin password immediately after first login

### Local Development

```bash
# Install dependencies
pip install -r requirements.txt

# Run migrations
python manage.py migrate

# Create superuser
python manage.py createsuperuser

# Run development server
python manage.py runserver
```

### API Endpoints

- `/api/geojson-files/` - CRUD operations for GeoJSON files
- `/api/map-layers/` - Layer visibility management
- `/api/map-data/` - Public map data for embed
- `/embed/` - Embeddable map view
- `/dashboard/` - Admin dashboard

### Usage

1. **Upload GeoJSON**: Drag & drop files or use the upload form
2. **Customize Colors**: Choose display colors for each layer
3. **Manage Visibility**: Toggle layer visibility in real-time
4. **Embed Map**: Use the provided iframe code to embed in other sites

### Technical Details

- **Framework**: Django 5.2.7
- **Database**: SQLite (suitable for Vercel's serverless environment)
- **API**: Django REST Framework
- **Frontend**: Vanilla JavaScript with Leaflet.js
- **Styling**: Custom CSS with responsive design

### Troubleshooting

Common issues and solutions:

1. **Static files not loading**: Ensure `whitenoise` is installed and configured
2. **Database issues**: Vercel automatically handles SQLite database
3. **CORS errors**: Check `CORS_ALLOW_ALL_ORIGINS` setting
4. **Admin access**: Use the setup credentials or create new superuser

### Support

For issues and questions:
- Check the Django documentation
- Review Vercel deployment logs
- Ensure all requirements are properly installed