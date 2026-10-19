# RZ Custom Tailor & Alteration — Portfolio Demo

A portfolio-ready Flask tailoring and clothing shop demo. It includes a customer storefront, animated featured-product carousel, category catalogue, product detail pages, bag and demo checkout, appointment booking, contact inquiries, testimonials, and a protected admin area.

The app uses SQLAlchemy models and creates its tables on first startup. Its tables cover `Category`, `Product`, `Order`, `Appointment`, `Inquiry`, `Testimonial` and key/value `Setting`. SQLite is the local default; PostgreSQL is supported with `DATABASE_URL`.

## Run locally on Windows

1. Install Python 3.10 or newer.
2. Extract this ZIP into a new folder.
3. Double-click `run_windows.bat`. It creates a virtual environment, installs the packages and starts Flask.
4. Open `http://127.0.0.1:5000` in a browser.
5. Admin sign-in: `http://127.0.0.1:5000/admin/login`.

Starter admin credentials are `admin` / `ChangeMe123!`. Sign in and change them under **Admin account** before you share a hosted demo. The database seeds sample products, reviews, categories, and placeholder business details on first run. Change these to client-approved details in the admin panel. Review names and quotes are demo content; replace them with approved reviews.

## PostgreSQL

Create an empty PostgreSQL database, then copy `.env.example` to `.env` and set `DATABASE_URL`, for example:

```text
DATABASE_URL=postgresql+psycopg://postgres:YOUR_PASSWORD@localhost:5432/rz_tailor
```

The app creates its tables when it starts. Do not share `.env` or commit real database passwords.

## Portfolio link / hosting

The ZIP runs on your laptop at the local URL above. To show it to other customers from your portfolio, deploy it to a Python web host with PostgreSQL and add that host's public URL to your portfolio. Set `SECRET_KEY`, `ADMIN_USERNAME`, `ADMIN_EMAIL`, `ADMIN_PASSWORD`, and `DATABASE_URL` as private host environment variables. Use a persistent upload disk or object storage for product photos; temporary host storage may be cleared during redeploys. The included `Procfile` starts the app with Gunicorn on a compatible host.

## What the demo includes

- Responsive tailor storefront and automatically advancing featured-product carousel.
- Shop categories: Suits, Shirts, Shoes, Ready to Wear, Alterations, Fabrics; the admin can add categories.
- Editable product catalog: title, description, price, category, image upload, colour choices, sizes and featured status.
- Product pages with gallery-style imagery, price, tax/shipping notes, colour and size selection, quantity, Add to Bag and Buy Now.
- Shopping bag with quantity updates and remove action; demo checkout displays a sample Ontario 13% HST estimate and stores order requests. It never collects or charges a card.
- Custom design / measurement request form.
- Appointment booking requests with customer name, phone, email, requested date, service, notes and admin status.
- Contact inquiry form with an admin inbox and status.
- Testimonial and review management.
- Admin-editable business name, public email, phone/SMS, WhatsApp, address, currency, and Facebook, Instagram, TikTok, LINE and LinkedIn links.
- Admin login with salted password hashing and editable username/email/password.

## Before going live

This is a customer presentation demo, not a production commerce launch. Payment processing, tax rules by shipping address, inventory control, shipping integrations, verified reviews, CSRF protection, login rate limiting, email notifications, privacy/consent policy and database migrations need production review and setup. The sample 13% HST is illustrative only; confirm actual tax, currency, prices, shipping, returns and all business details with the client. The built-in review text is sample content and must be replaced with real approved testimonials before publication.
