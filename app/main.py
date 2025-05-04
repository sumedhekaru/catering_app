from fastapi import FastAPI, Request, Form, Depends, status
from fastapi.responses import RedirectResponse, HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from starlette.middleware.sessions import SessionMiddleware
import sqlite3
from passlib.context import CryptContext
import os
from PIL import Image

def get_db():
    BASE_DIR = os.path.dirname(os.path.abspath(__file__))
    db_path = os.path.join(BASE_DIR, 'caterers.db')
    if not os.path.exists(db_path):
        raise RuntimeError("Database file 'caterers.db' does not exist. Please create it and run the SQL schema script before starting the app.")
    conn = sqlite3.connect(db_path)
    conn.row_factory = sqlite3.Row
    try:
        yield conn
    finally:
        conn.close()

app = FastAPI()
app.add_middleware(SessionMiddleware, secret_key=os.environ.get('SECRET_KEY', 'changeme'))

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
PROJECT_ROOT = os.path.dirname(BASE_DIR)
STATIC_DIR = os.path.join(PROJECT_ROOT, "app", "static")
GALLERY_DIR = os.path.join(STATIC_DIR, "gallery")
GALLERY_ORIGINALS = os.path.join(GALLERY_DIR, "originals")
GALLERY_THUMBS = os.path.join(GALLERY_DIR, "thumbs")
THUMB_SIZE = (400, 300)  # width, height
print(f"[DEBUG] Mounting static directory at: {STATIC_DIR}")

# Ensure gallery folders exist
os.makedirs(GALLERY_ORIGINALS, exist_ok=True)
os.makedirs(GALLERY_THUMBS, exist_ok=True)

def resize_gallery_images():
    for filename in os.listdir(GALLERY_ORIGINALS):
        if filename.lower().endswith((".jpg", ".jpeg", ".png", ".webp")):
            orig_path = os.path.join(GALLERY_ORIGINALS, filename)
            thumb_path = os.path.join(GALLERY_THUMBS, filename)
            if not os.path.exists(thumb_path):
                try:
                    img = Image.open(orig_path)
                    img.thumbnail(THUMB_SIZE)
                    img.save(thumb_path)
                    print(f"[GALLERY] Resized and saved: {thumb_path}")
                except Exception as e:
                    print(f"[GALLERY] Error resizing {filename}: {e}")

resize_gallery_images()

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

templates = Jinja2Templates(directory=os.path.join(BASE_DIR, "templates"))
app.mount("/static", StaticFiles(directory=STATIC_DIR), name="static")

def crop_center(img, crop_width, crop_height):
    img_width, img_height = img.size
    left = (img_width - crop_width) // 2
    top = (img_height - crop_height) // 2
    right = left + crop_width
    bottom = top + crop_height
    return img.crop((left, top, right, bottom))

def get_gallery_images():
    """
    Ensure all originals have a resized, portrait-cropped thumb and large image, and return up to 9 latest gallery images for template rendering.
    """
    THUMB_SIZE = (400, 500)  # 4:5 aspect ratio
    LARGE_SIZE = (800, 1000) # 4:5 aspect ratio
    GALLERY_LARGE = os.path.join(GALLERY_DIR, "large")
    os.makedirs(GALLERY_LARGE, exist_ok=True)
    files = []
    for filename in os.listdir(GALLERY_ORIGINALS):
        if filename.lower().endswith((".jpg", ".jpeg", ".png", ".webp")):
            orig_path = os.path.join(GALLERY_ORIGINALS, filename)
            thumb_path = os.path.join(GALLERY_THUMBS, filename)
            large_path = os.path.join(GALLERY_LARGE, filename)
            try:
                img = Image.open(orig_path)
                img = img.convert("RGB")
                w, h = img.size
                target_ratio = 4 / 5
                img_ratio = w / h
                # Always crop to center 4:5 portrait
                if img_ratio > target_ratio:
                    new_w = int(h * target_ratio)
                    new_h = h
                else:
                    new_w = w
                    new_h = int(w / target_ratio)
                crop_img = crop_center(img, new_w, new_h)
                # Save thumb
                thumb_img = crop_img.resize(THUMB_SIZE, Image.LANCZOS)
                thumb_img.save(thumb_path)
                # Save large
                large_img = crop_img.resize(LARGE_SIZE, Image.LANCZOS)
                large_img.save(large_path, quality=80, optimize=True)
            except Exception as e:
                print(f"[GALLERY] Error resizing/cropping {filename}: {e}")
            # Add file info for sorting
            files.append({
                "filename": filename,
                "mtime": os.path.getmtime(orig_path)
            })
    # Sort by modification time descending and take up to 9
    files = sorted(files, key=lambda x: x["mtime"], reverse=True)[:9]
    import random
    sinhala_lines = [
        "ආහාරයෙන් ආදරය පිරේ",
        "රසවත් රසකැවිලි ඔබ වෙනුවෙන්",
        "ගෙදර රසයි, හදවතින්ම",
        "කෑමට ආදරෙයි",
        "අපේ කෑම, ඔබේ සිනහව",
        "ආදරයෙන් පිසූ රසය",
        "කෑමෙන් සතුටට",
        "හොඳම රසය, හොඳම මතකය",
        "කෑමට සුවඳයි, රසයි",
        "කෑමෙන් යහපත් සම්බන්ධතා",
        "ඔබට උදුනූ රසය",
        "ආදරේ රසය කෑමෙන්",
        "පවුලේ රසය මේ කෑමෙන්",
        "කෑමෙන් සිනාසෙමු",
        "හදවතින් පිසූ රසය",
        "ඔබටම හදපු රසය"
    ]
    images = [
        {
            "image_url": f"gallery/thumbs/{f['filename']}",
            "large_url": f"gallery/large/{f['filename']}",
            "caption": random.choice(sinhala_lines)
        }
        for f in files
    ]
    return images

def verify_admin(request: Request):
    return request.session.get("admin_logged_in")

@app.get("/", response_class=HTMLResponse)
def home(request: Request, db=Depends(get_db)):
    menus = db.execute("SELECT * FROM menus").fetchall()
    deals = db.execute("SELECT * FROM deals").fetchall()
    gallery = get_gallery_images()  # Use the new gallery logic
    return templates.TemplateResponse("home.html", {"request": request, "menus": menus, "deals": deals, "gallery": gallery})

@app.get("/admin/login", response_class=HTMLResponse)
def admin_login_get(request: Request):
    return templates.TemplateResponse("admin_login.html", {"request": request})

@app.post("/admin/login")
def admin_login_post(request: Request, username: str = Form(...), password: str = Form(...), db=Depends(get_db)):
    admin = db.execute("SELECT * FROM admins WHERE username = ?", (username,)).fetchone()
    if admin and pwd_context.verify(password, admin["password_hash"]):
        request.session["admin_logged_in"] = True
        return RedirectResponse("/admin", status_code=status.HTTP_302_FOUND)
    return templates.TemplateResponse("admin_login.html", {"request": request, "error": "Invalid credentials"})

@app.get("/admin", response_class=HTMLResponse)
def admin_dashboard(request: Request, db=Depends(get_db)):
    if not verify_admin(request):
        return RedirectResponse("/admin/login", status_code=status.HTTP_302_FOUND)
    menus = db.execute("SELECT * FROM menus").fetchall()
    deals = db.execute("SELECT * FROM deals").fetchall()
    gallery = db.execute("SELECT * FROM gallery").fetchall()
    return templates.TemplateResponse("admin_dashboard.html", {"request": request, "menus": menus, "deals": deals, "gallery": gallery})

@app.get("/logout")
def logout(request: Request):
    request.session.clear()
    return RedirectResponse("/", status_code=status.HTTP_302_FOUND)
