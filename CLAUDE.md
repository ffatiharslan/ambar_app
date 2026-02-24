# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

**AN-ANT Ambar** is a Django web application for an Ankara–Antalya logistics company. It features a full UI inspired by a React/Tailwind source design, implemented with Django templates, Tailwind CSS CDN, Alpine.js, and AOS animations.

Virtual environment: `.venv/` (repo root) | Django project: `ambar/`

## Setup

```bash
source .venv/bin/activate
cd ambar
python manage.py migrate
python manage.py runserver
```

## Common Commands

All Django commands run from the `ambar/` directory with the virtual environment activated.

```bash
# From ambar/ directory (requires Node.js):
npm run build:css    # Compile Tailwind CSS once
npm run watch:css    # Recompile on template changes (run in a separate terminal)

python manage.py runserver          # Dev server at http://127.0.0.1:8000
python manage.py makemigrations     # Create new migrations
python manage.py migrate            # Apply migrations
python manage.py test ambarapp      # Run app tests
python manage.py createsuperuser    # Create admin user
```

## URL Routes

| URL | View | Template |
|-----|------|----------|
| `/` | `home` | `home.html` |
| `/iletisim/` | `contact` | `contact.html` |
| `/hizmetler/` | `services` | `services.html` |
| `/guzergahlar/` | `routes` | `routes.html` |
| `/hakkimizda/` | `about` | `about.html` |
| `/admin/` | Django admin | — |

## Architecture

Standard Django **MTV** structure:

- **`ambar/ambar/`** — Project config (`settings.py`, `urls.py`, `wsgi.py`, `asgi.py`)
- **`ambar/ambarapp/`** — Main app
  - `views.py` — All page views
  - `forms.py` — `ContactForm` (ad_soyad, email, mesaj)
  - `models.py` — Database models (currently empty)
  - `migrations/` — Schema history
- **`ambar/templates/`** — All HTML templates
  - `base.html` — Base layout: Inter font, Tailwind CDN (with custom config), Alpine.js CDN, AOS CDN, Django message toasts
  - `partials/header.html` — Sticky navbar with Alpine.js dropdowns and mobile hamburger menu
  - `partials/footer.html` — 4-column dark footer
  - `home.html` — Hero, statistics bar, 3-column service cards, "Neden Biz" section, FAQ accordion, CTA
  - `contact.html` — Breadcrumb, contact form with Django form validation display, branch cards, working hours box
  - `about.html`, `services.html`, `routes.html` — Supporting pages

## Frontend Stack

- **Tailwind CSS v3** — built with npm, output served as a Django static file
  - Config: `ambar/tailwind.config.js` (custom primary color `#003366`, Inter font)
  - Input: `ambarapp/static/css/input.css` (Tailwind directives + custom `.section-padding`, `.container-max` components)
  - Output: `ambarapp/static/css/output.css` (compiled, served at `/static/css/output.css`)
  - Build: `npm run build:css` (from `ambar/` directory, requires Node.js)
  - Watch: `npm run watch:css` (for development)
- **Alpine.js v3** (CDN) — dropdown menus, mobile hamburger, FAQ accordion
- **AOS** (CDN) — scroll animations (`data-aos="fade-up"`, `data-aos-delay`)
- `group-hover:` Tailwind classes handle service card hover effects (icon color swap + lift)
- `[x-cloak]` is defined in `input.css` to prevent Alpine.js flash

## Contact Form Flow

POST to `/iletisim/` → validate `ContactForm` → on success, Django message + redirect (PRG pattern) → toast notification auto-hides after 5s via Alpine.js.

## Models

**`Service`** (`ambarapp/models.py`)
- `title`, `description`, `icon` (choices: truck/arrow/building/package), `features` (newline-separated TextField), `order`, `is_active`
- `features_list` property splits the TextField into a Python list for template iteration
- Admin: `ServiceAdmin` with `list_editable` for order/is_active

**`Route`** (`ambarapp/models.py`)
- `origin`, `destination`, `description`, `duration`, `frequency`, `order`, `is_active`
- Admin: `RouteAdmin` with `list_editable` for order/is_active

Initial data is seeded via `ambarapp/migrations/0002_seed_initial_data.py` (3 services, 3 routes).

**Icon rendering**: `templates/partials/service_icon.html` renders the correct SVG based on `icon` value. Used with `{% include 'partials/service_icon.html' with icon=service.icon css_class="w-7 h-7" only %}`.

## Key Dependencies

- Django 5.2.1 (installed, settings.py header says 5.2.1)
- asgiref 3.11.1
- sqlparse 0.5.5

No linting or formatting tools are configured.
