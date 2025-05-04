# Business Requirements Document (BRD)

## 1. Executive Summary
This document outlines the business requirements for Pera Caters, a static, mobile-first food catering web application to be launched in Sri Lanka. The platform will showcase Pera Caters' catering services, menus, and contact information, allowing customers to submit inquiries via a form or contact Pera Caters directly by phone. In addition, Pera Caters will maintain an active Facebook page for posting monthly deals and engaging with customers.

## 2. Target Audience
- Individuals and organizations planning events (weddings, parties, corporate events, etc.)
- Catering service providers (business owners and staff)

## 3. Core Features
- Mobile-first responsive design
- Display of Pera Caters' catering services and offerings
- Menu and package listing with pricing
- Image gallery of past events and dishes
- Simple inquiry form (collect name, contact, event details)
- Prominent display of phone number for direct calls to Pera Caters
- "Latest Deals" or "Promotions" section (synced with Facebook posts or updated manually)
- Facebook page integration (embed posts or link to page)
- Multilingual support (Sinhala, Tamil, English)

## 4. Website & Facebook Integration
- Use the website as the main information hub, always up to date with Pera Caters' offerings and inquiry options.
- Maintain a dedicated section for latest deals/promotions, updated monthly to match Facebook posts.
- Embed or link to the Facebook page and latest posts using Facebook Page Plugin or embedded posts.
- Each Facebook deal post should link back to the website's promotions or inquiry section.
- Add social sharing buttons to encourage visitors to follow Pera Caters' Facebook page.
- (Optional, future) Automate fetching and displaying latest Facebook deals on the website using Facebook Graph API.
- Workflow: Post deal on Facebook, update website deals section, cross-link both platforms.

## 5. Localization
- Support for local languages (Sinhala, Tamil, English)
- Local currency (LKR)
- Compliance with Sri Lankan food safety and data protection regulations

## 6. Technical Specifications & Wireframe

### Recommended Tech Stack
- HTML5, CSS3 (with mobile-first responsive framework such as Bootstrap or Tailwind CSS)
- JavaScript (for form validation and interactivity)
- Static site generator (optional, e.g., Next.js, Hugo, or Jekyll) for easier content updates

### Page Structure / Wireframe
- **Header:**
  - Logo
  - Navigation (Home, Menu, Gallery, Deals, Contact)
- **Hero Section:**
  - Brief intro, call-to-action, phone number
- **Menu/Packages:**
  - List of Pera Caters' offerings with pricing
- **Gallery:**
  - Images of past events/dishes
- **Deals/Promotions:**
  - Monthly deals (manual update or embedded Facebook posts)
  - Button/link to Pera Caters' Facebook page
- **Inquiry Form:**
  - Fields: Name, Contact Number, Email, Event Details/Message
  - Submit button (send to Pera Caters' business email or store in a simple backend/Google Form)
- **Footer:**
  - Address, phone, email, social media links

### Facebook Integration
- Use Facebook Page Plugin or embed specific posts in the Deals section
- Add social sharing buttons (Facebook, WhatsApp, etc.)
- Ensure deals section is easy to update monthly (manual image/text or embed)

### Multilingual Support
- Use language switcher in navigation
- Store content in separate files/sections per language

### Other Notes
- Ensure fast loading and good SEO (meta tags, alt text)
- Test on various mobile devices
- Accessibility: use proper contrast, alt text, and keyboard navigation

## 7. FastAPI Architecture & Implementation Notes

- **Backend Framework:** FastAPI (Python)
- **Frontend:** Server-side rendered HTML using Jinja2 templates (no separate frontend framework)
- **Admin Panel:**
  - Secure admin login (username/password)
  - Admin can add/edit/delete menu items, deals/promotions, gallery images, and content
  - Admin interface is accessible via web browser
- **Public Site:**
  - Displays menus, deals, gallery, inquiry form, contact info, etc.
  - All pages rendered using the same HTML template system as admin
- **Database:** Use SQLite (or PostgreSQL) to store menus, deals, gallery, and admin users
- **Authentication:** Simple session-based authentication for admin (can be upgraded later)
- **Extensibility:**
  - Designed so user management, ordering, and other features can be added in the future
- **Deployment:** Can be hosted on any standard Python web host (e.g., DigitalOcean, Heroku, Render)

---
_Last updated: 2025-05-03_
