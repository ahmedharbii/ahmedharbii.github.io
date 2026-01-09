# ahmedharbii.github.io

Personal website and portfolio for Ahmed Harbi Elsayed - Robotics Researcher specializing in Marine and Maritime Intelligent Robotics.

## 🌐 Live Website

Visit: [ahmedharbii.github.io](https://ahmedharbii.github.io)

## 📁 Repository Structure

```
.
├── index.html              # Homepage
├── projects.html           # Projects showcase
├── publications.html       # Research publications
├── contact.html           # Contact information
├── styles.css             # Main stylesheet
├── particles.js           # Particle animation background
├── images/                # Image assets
│   ├── home/             # Homepage images
│   ├── projects/         # Project screenshots
│   └── publications/     # Publication thumbnails
├── media/                # Media files
│   └── press/           # Press articles and PDFs
├── tests/                # Automated test suite
└── .github/workflows/    # CI/CD workflows
```

## 🚀 Features

- Modern, responsive design with glassmorphism effects
- Dark/Light theme toggle
- 3D animated shark using Three.js
- Particle.js background effects
- SEO optimized with Open Graph tags
- Mobile-friendly navigation

## 🧪 Testing

Run automated tests to verify website integrity:

```bash
python tests/test_website.py
```

Tests cover:
- HTML structure validation
- Meta tags and SEO
- Image and asset verification
- Internal link checking
- Responsive design validation

See [tests/README.md](tests/README.md) for more details.

## 🛠️ Local Development

1. Clone the repository:
```bash
git clone https://github.com/ahmedharbii/ahmedharbii.github.io.git
cd ahmedharbii.github.io
```

2. Serve locally (Python):
```bash
python -m http.server 8000
```

3. Open in browser:
```
http://localhost:8000
```

## 📝 Content Management

### Update Publications

Publications are managed in `_data/publications.yml`. To fetch from Google Scholar:

```bash
pip install -r requirements.txt
python fetch_publications.py
```

### Add New Projects

Edit `projects.html` and add project cards with images/videos in the `images/projects/` folder.

## 📄 License

Copyright © 2026 Ahmed Harbi Elsayed. All rights reserved.
