# Catering App

A web-based catering management application built with FastAPI, Jinja2, and SQLite. This app allows you to manage menus, deals, and a gallery for a catering business, with an admin dashboard for secure management.

## Features
- Public homepage displaying menus, deals, and gallery
- Sinhala and English menu descriptions
- Customisable Menu with included and optional items
- Admin login and dashboard for managing content
- Image gallery with automatic thumbnail generation
- Session-based authentication for admin
- Hero section with horizontal action buttons (Call, Request a Call, Inquire, Facebook, Google)
- Menu detail popup with action icons and smooth navigation
- "Latest Deals" section encourages users to check Facebook for promotions
- Modern, responsive UI with code and style cleanup

## Tech Stack
- **Backend:** FastAPI
- **Frontend:** Jinja2 Templates
- **Database:** SQLite
- **Static Files:** Managed under `app/static` (including gallery images)

## Getting Started

### Prerequisites
- Python 3.8+
- [pip](https://pip.pypa.io/en/stable/)

### Installation
1. Clone the repository:
   ```bash
   git clone <your-repo-url>
   cd catering_app
   ```
2. (Recommended) Create and activate a virtual environment:
   ```bash
   python -m venv venv
   source venv/bin/activate
   ```
3. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```
4. Ensure the database file `app/caterers.db` exists and is initialized with the required schema.

### Running the Application
```bash
uvicorn app.main:app --reload
```
Visit [http://127.0.0.1:8000](http://127.0.0.1:8000) in your browser.

### Directory Structure
```
catering_app/
├── app/
│   ├── main.py
│   ├── __init__.py
│   ├── templates/
│   ├── static/
│   │   └── gallery/
│   │       ├── originals/
│   │       └── thumbs/
│   └── caterers.db
├── requirements.txt
└── README.md
```

## Usage Notes
- Click on any menu card to view details in a popup modal. Action icons at the bottom allow users to call, request a call, or inquire, and will close the modal before navigating.
- The hero section's action buttons are always horizontal and centered.
- The "Latest Deals" section contains a Sinhala message encouraging users to visit Facebook for current promotions and savings.

## Notes
- Admin credentials are stored in the `admins` table in the database.
- The application will create necessary static/gallery directories if they do not exist.
- Make sure to set a secure `SECRET_KEY` via environment variables for production use.

## License
MIT License
