import os
import re
import uuid
from functools import wraps
from pathlib import Path
from dotenv import load_dotenv
from flask import Flask, flash, redirect, render_template, request, session, url_for
from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import check_password_hash, generate_password_hash
from werkzeug.utils import secure_filename

load_dotenv()
ROOT = Path(__file__).resolve().parent

# Supabase কনফিগারেশন এবং আপলোড ফাংশন
from supabase import create_client, Client
SUPABASE_URL = os.environ.get("SUPABASE_URL")
SUPABASE_KEY = os.environ.get("SUPABASE_KEY")
SUPABASE_BUCKET = os.environ.get("SUPABASE_BUCKET", "media")
supabase: Client = create_client(SUPABASE_URL, SUPABASE_KEY)
def upload_to_supabase(file):
    if not file or file.filename == '':
        return None
    try:
        file_name = file.filename
        file_bytes = file.read()

        supabase.storage.from_(SUPABASE_BUCKET).upload(
            path=file_name,
            file=file_bytes,
            file_options={"content-type": file.content_type}
        )
        public_url = supabase.storage.from_(SUPABASE_BUCKET).get_public_url(file_name)
        return public_url
    except Exception as e:
        print(e)
        return None
            try:
                file_name = file.filename
                file_bytes = file.read()

                supabase.storage.from_(SUPABASE_BUCKET).upload(
                    path=file_name,
                    file=file_bytes,
                    file_options={"content-type": file.content_type}
                )
                public_url = supabase.storage.from_(SUPABASE_BUCKET).get_public_url(file_name)
                return public_url
            except Exception as e:
                print(e)
                return None

        public_url = supabase.storage.from_(SUPABASE_BUCKET).get_public_url(file_name)
        return public_url
    except Exception as e:
        print(f"Supabase Upload Error: {e}")
        return None

app = Flask(__name__)
app.config["SECRET_KEY"] = os.getenv("SECRET_KEY", "rz-demo-change-this-key")
database_url = os.getenv("DATABASE_URL", "sqlite:///rz_demo.db")
if database_url.startswith("postgres://"):
    database_url = database_url.replace("postgres://", "postgresql+psycopg://", 1)
elif database_url.startswith("postgresql://") and "+psycopg" not in database_url:
    database_url = database_url.replace("postgresql://", "postgresql+psycopg://", 1)
app.config["SQLALCHEMY_DATABASE_URI"] = database_url
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
app.config["UPLOAD_FOLDER"] = ROOT / "static" / "uploads"
app.config["MAX_CONTENT_LENGTH"] = 16 * 1024 * 1024  # সর্বোচ্চ ১৬ এমবি পর্যন্ত ফাইল সাইজ লিমিট

app.config["SESSION_COOKIE_HTTPONLY"] = True
app.config["SESSION_COOKIE_SAMESITE"] = "Lax"
app.config["SESSION_COOKIE_SECURE"] = os.getenv("APP_ENV", "development") == "production"
if database_url.startswith("sqlite"):
    Path(app.instance_path).mkdir(parents=True, exist_ok=True)
db = SQLAlchemy(app)

class Product(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(140), nullable=False)
    category_id = db.Column(db.Integer, db.ForeignKey("category.id"), nullable=False)
    category = db.relationship("Category")
    description = db.Column(db.Text, nullable=False, default="Made to measure, made personal.")
    price = db.Column(db.Numeric(10, 2), nullable=False, default=649)
    color = db.Column(db.String(30), nullable=False, default="#26343b")
    colors = db.Column(db.String(500), nullable=False, default="Cream,Snow Wash,Navy,Grey,Taupe,Brown")
    sizes = db.Column(db.String(250), nullable=False, default="30,32,34,36,38,40")
    image = db.Column(db.String(300), nullable=False, default="")
    featured = db.Column(db.Boolean, default=False)


class Category(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), unique=True, nullable=False)
    slug = db.Column(db.String(90), unique=True, nullable=False)
    color = db.Column(db.String(30), nullable=False, default="#77796d")


class Order(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    customer = db.Column(db.String(140), nullable=False)
    email = db.Column(db.String(180), nullable=False)
    phone = db.Column(db.String(60), nullable=False, default="")
    item = db.Column(db.String(180), nullable=False)
    details = db.Column(db.Text, nullable=False, default="")
    price = db.Column(db.Numeric(10, 2), nullable=False)
    status = db.Column(db.String(30), nullable=False, default="New")
    created = db.Column(db.DateTime, server_default=db.func.now())


class Setting(db.Model):
    key = db.Column(db.String(80), primary_key=True)
    value = db.Column(db.String(300), nullable=False)


class Appointment(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    customer_name = db.Column(db.String(140), nullable=False)
    phone = db.Column(db.String(60), nullable=False)
    email = db.Column(db.String(180), nullable=False)
    preferred_date = db.Column(db.Date, nullable=False)
    service_type = db.Column(db.String(100), nullable=False)
    notes = db.Column(db.Text, nullable=False, default="")
    status = db.Column(db.String(30), nullable=False, default="New")
    created = db.Column(db.DateTime, server_default=db.func.now())


class Inquiry(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    customer_name = db.Column(db.String(140), nullable=False)
    email = db.Column(db.String(180), nullable=False)
    phone = db.Column(db.String(60), nullable=False, default="")
    subject = db.Column(db.String(180), nullable=False, default="General enquiry")
    message = db.Column(db.Text, nullable=False)
    status = db.Column(db.String(30), nullable=False, default="New")
    created = db.Column(db.DateTime, server_default=db.func.now())


class Testimonial(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    customer_name = db.Column(db.String(120), nullable=False)
    location = db.Column(db.String(120), nullable=False, default="")
    review = db.Column(db.Text, nullable=False)
    rating = db.Column(db.Integer, nullable=False, default=5)
    active = db.Column(db.Boolean, nullable=False, default=True)
    created = db.Column(db.DateTime, server_default=db.func.now())


DEFAULT_SETTINGS = {
    "brand": "RZ Custom Tailor & Alteration",
    "admin_username": os.getenv("ADMIN_USERNAME", "admin"), "admin_email": os.getenv("ADMIN_EMAIL", "admin@rzcustomtailor.com"),
    "email": "hello@rzcustomtailor.com", "phone": "+1 (416) 555-0134",
    "address": "Toronto, Ontario · By appointment", "instagram": "https://instagram.com/",
    "facebook": "https://facebook.com/", "tiktok": "https://tiktok.com/",
    "line": "https://line.me/", "linkedin": "https://linkedin.com/",
    "whatsapp": "https://wa.me/14165550134", "currency": "CAD",
}

DEFAULT_CATEGORIES = ["Suits", "Shirts", "Shoes", "Ready to Wear", "Alterations", "Fabrics"]


def admin_required(view):
    @wraps(view)
    def wrapped(*args, **kwargs):
        if not session.get("admin_user"):
            return redirect(url_for("admin_login", next=request.path))
        return view(*args, **kwargs)
    return wrapped


def save_uploaded_image(file_storage):
    if not file_storage or not file_storage.filename:
        return ""
    safe_name = secure_filename(file_storage.filename)
    suffix = Path(safe_name).suffix.lower()
    if suffix not in {".png", ".jpg", ".jpeg", ".webp"}:
        return ""
    app.config["UPLOAD_FOLDER"].mkdir(parents=True, exist_ok=True)
    filename = f"{uuid.uuid4().hex[:12]}{suffix}"
    file_storage.save(app.config["UPLOAD_FOLDER"] / filename)
    return f"uploads/{filename}"


def settings_map():
    data = dict(DEFAULT_SETTINGS)
    data.update({s.key: s.value for s in Setting.query.all()})
    return data


def init_db():
    db.create_all()
    for name in DEFAULT_CATEGORIES:
        slug = re.sub(r"[^a-z0-9]+", "-", name.lower()).strip("-")
        if not Category.query.filter_by(slug=slug).first():
            db.session.add(Category(name=name, slug=slug))
    db.session.flush()
    if Product.query.count() == 0:
        samples = [
            Product(name="Cream Stretch Denim", category=Category.query.filter_by(name="Ready to Wear").first(), description="Comfort-fit stretch denim made with a soft, non-wrinkle fabric. Available in six versatile colours.", price=550, color="#ded8ca", colors="Cream,Snow Wash,Navy,Grey,Taupe,Brown", sizes="30,32,34,36,38,40", featured=True),
            Product(name="The Signature Suit", category=Category.query.filter_by(name="Suits").first(), description="A timeless two-piece, individually cut to your measurements.", price=649, color="#26343b", colors="Midnight,Olive,Charcoal", sizes="Made to measure", featured=True),
            Product(name="The Everyday Blazer", category=Category.query.filter_by(name="Suits").first(), description="Easy refinement in a soft, versatile wool blend.", price=389, color="#77796d", colors="Olive,Navy,Taupe", sizes="Made to measure", featured=True),
            Product(name="The Linen Edit", category=Category.query.filter_by(name="Ready to Wear").first(), description="Lightweight, breathable linen for warmer days.", price=329, color="#dcd4c3", colors="Ivory,Sage,Blue", sizes="S,M,L,XL", featured=True),
            Product(name="The Evening Suit", category=Category.query.filter_by(name="Suits").first(), description="A polished silhouette for the moments that matter.", price=699, color="#72453f", colors="Burgundy,Black,Midnight", sizes="Made to measure", featured=False),
        ]
        db.session.add_all(samples)
    for key, value in DEFAULT_SETTINGS.items():
        if not Setting.query.get(key):
            db.session.add(Setting(key=key, value=value))
    if not Setting.query.get("admin_password_hash"):
        db.session.add(Setting(key="admin_password_hash", value=generate_password_hash(os.getenv("ADMIN_PASSWORD", "ChangeMe123!"))))
    if Testimonial.query.count() == 0:
        db.session.add_all([
            Testimonial(customer_name="Daniel R.", location="Toronto", review="The fitting felt personal from the first conversation. My suit is comfortable and beautifully finished.", rating=5),
            Testimonial(customer_name="Maya L.", location="North York", review="A lovely fabric selection and thoughtful guidance. The final fit was exactly what I hoped for.", rating=5),
            Testimonial(customer_name="Chris P.", location="Etobicoke", review="Easy to work with, clear updates and a jacket that feels made just for me.", rating=5),
        ])
    db.session.commit()


@app.route("/")
def home():
    category = Category.query.filter_by(slug=request.args.get("category", "")).first() if request.args.get("category") else None
    query = Product.query
    if category:
        query = query.filter_by(category_id=category.id)
    products = query.order_by(Product.featured.desc(), Product.id).all()
    categories = Category.query.order_by(Category.name).all()
    testimonials = Testimonial.query.filter_by(active=True).order_by(Testimonial.id.desc()).limit(6).all()
    return render_template("home.html", products=products, categories=categories, testimonials=testimonials, settings=settings_map())


@app.get("/product/<int:product_id>")
def product_detail(product_id):
    product = db.get_or_404(Product, product_id)
    similar = Product.query.filter(Product.id != product.id).limit(3).all()
    return render_template("product.html", product=product, similar=similar, settings=settings_map())


def cart_lines():
    cart = session.get("cart", {})
    products = {p.id: p for p in Product.query.filter(Product.id.in_([int(v["product_id"]) for v in cart.values()])).all()} if cart else {}
    lines = []
    subtotal = 0.0
    for key, item in cart.items():
        product = products.get(int(item["product_id"]))
        if not product:
            continue
        qty = max(1, int(item.get("quantity", 1)))
        line_total = float(product.price) * qty
        subtotal += line_total
        lines.append({"key": key, "product": product, "color": item.get("color", ""), "size": item.get("size", ""), "quantity": qty, "total": line_total})
    return lines, subtotal


@app.route("/cart", methods=["GET", "POST"])
def cart_page():
    if request.method == "POST":
        cart = session.get("cart", {})
        if request.form.get("remove"):
            cart.pop(request.form["remove"], None)
            flash("Item removed from your bag.", "success")
        else:
            for key in list(cart):
                try:
                    cart[key]["quantity"] = max(1, min(20, int(request.form.get(f"qty_{key}", cart[key]["quantity"]))))
                except (TypeError, ValueError):
                    pass
            flash("Your bag has been updated.", "success")
        session["cart"] = cart
        return redirect(url_for("cart_page"))
    lines, subtotal = cart_lines()
    return render_template("cart.html", lines=lines, subtotal=subtotal, settings=settings_map())


@app.post("/cart/add/<int:product_id>")
def add_to_cart(product_id):
    product = db.get_or_404(Product, product_id)
    color = request.form.get("color", "").strip()[:60]
    size = request.form.get("size", "").strip()[:60]
    try:
        quantity = max(1, min(20, int(request.form.get("quantity", "1"))))
    except ValueError:
        quantity = 1
    key = f"{product.id}:{color}:{size}"
    cart = session.get("cart", {})
    if key in cart:
        cart[key]["quantity"] = min(20, int(cart[key]["quantity"]) + quantity)
    else:
        cart[key] = {"product_id": product.id, "color": color, "size": size, "quantity": quantity}
    session["cart"] = cart
    flash(f"{product.name} added to your bag.", "success")
    return redirect(url_for("checkout") if request.form.get("buy_now") else url_for("product_detail", product_id=product.id))


@app.route("/checkout", methods=["GET", "POST"])
def checkout():
    lines, subtotal = cart_lines()
    if not lines:
        flash("Your bag is empty. Choose a piece to get started.", "error")
        return redirect(url_for("home", _anchor="collection"))
    tax_rate = 0.13  # illustrative Ontario HST for demo calculations only
    tax = round(subtotal * tax_rate, 2)
    total = round(subtotal + tax, 2)
    if request.method == "POST":
        customer = request.form.get("customer", "").strip()
        email = request.form.get("email", "").strip()
        if not customer or not email:
            flash("Please enter your name and email to send this demo order.", "error")
            return redirect(url_for("checkout"))
        summary = " | ".join(f"{x['product'].name} / {x['color']} / size {x['size']} × {x['quantity']}" for x in lines)
        address = request.form.get("address", "").strip()
        payment = request.form.get("payment", "Discuss at fitting")
        details = f"{summary}\nDelivery: {address}\nPayment preference: {payment}\nDemo tax estimate (13%): ${tax:.2f}"
        db.session.add(Order(customer=customer, email=email, phone=request.form.get("phone", "")[:60], item=summary[:180], details=details[:2000], price=total))
        db.session.commit()
        session["cart"] = {}
        currency = settings_map()["currency"]
        flash(f"Demo order request received. Estimated total: ${total:.2f} {currency} including sample 13% HST. No payment was collected.", "success")
        return redirect(url_for("home"))
    return render_template("checkout.html", lines=lines, subtotal=subtotal, tax=tax, total=total, settings=settings_map())


@app.post("/appointment")
def book_appointment():
    from datetime import date
    name = request.form.get("customer_name", "").strip()
    phone = request.form.get("phone", "").strip()
    email = request.form.get("email", "").strip()
    service = request.form.get("service_type", "").strip()
    try:
        preferred_date = date.fromisoformat(request.form.get("preferred_date", ""))
    except ValueError:
        preferred_date = None
    if not all([name, phone, email, service, preferred_date]):
        flash("Please complete your name, phone, email, service and preferred date.", "error")
    else:
        db.session.add(Appointment(customer_name=name[:140], phone=phone[:60], email=email[:180], preferred_date=preferred_date, service_type=service[:100], notes=request.form.get("notes", "")[:2000]))
        db.session.commit()
        flash(f"Your fitting request is in. The {settings_map()['brand']} team will contact you to confirm the date.", "success")
    return redirect(url_for("home") + "#appointment")


@app.post("/inquiry")
def send_inquiry():
    name = request.form.get("customer_name", "").strip()
    email = request.form.get("email", "").strip()
    message = request.form.get("message", "").strip()
    if not name or not email or not message:
        flash("Please add your name, email and message.", "error")
    else:
        db.session.add(Inquiry(customer_name=name[:140], email=email[:180], phone=request.form.get("phone", "")[:60], subject=request.form.get("subject", "General enquiry")[:180], message=message[:4000]))
        db.session.commit()
        flash("Thank you. Your message has been sent to the demo inbox.", "success")
    return redirect(url_for("home") + "#contact")


@app.post("/order")
def place_order():
    customer = request.form.get("customer", "").strip()
    email = request.form.get("email", "").strip()
    if not customer or not email:
        flash("Please add your name and email so the atelier can follow up.", "error")
        return redirect(url_for("home") + "#customizer")
    item = request.form.get("item", "The Signature Suit")[:180]
    details = request.form.get("details", "")[:2000]
    try:
        price = float(request.form.get("price", "649"))
    except ValueError:
        price = 649
    db.session.add(Order(customer=customer, email=email, phone=request.form.get("phone", "")[:60], item=item, details=details, price=price))
    db.session.commit()
    flash(f"Design request received. The {settings_map()['brand']} team will be in touch to confirm your fitting.", "success")
    return redirect(url_for("home") + "#customizer")


@app.route("/admin/login", methods=["GET", "POST"])
def admin_login():
    if session.get("admin_user"):
        return redirect(url_for("admin"))
    if request.method == "POST":
        settings = settings_map()
        username = request.form.get("username", "").strip()
        password = request.form.get("password", "")
        password_setting = db.session.get(Setting, "admin_password_hash")
        if username == settings.get("admin_username") and password_setting and check_password_hash(password_setting.value, password):
            session["admin_user"] = username
            target = request.args.get("next", "")
            if target.startswith("/") and not target.startswith("//"):
                return redirect(target)
            return redirect(url_for("admin"))
        flash("That username and password did not match.", "error")
    return render_template("login.html", settings=settings_map())


@app.get("/admin/logout")
def admin_logout():
    session.pop("admin_user", None)
    flash("You have been signed out.", "success")
    return redirect(url_for("admin_login"))


@app.route("/admin", methods=["GET", "POST"])
@admin_required
def admin():
    if request.method == "POST":
        action = request.form.get("action")
        if action == "settings":
            # হিরো ব্যানার আপলোড হ্যান্ডেল করার জন্য
            if 'hero_banner' in request.files:
                file = request.files['hero_banner']
                if file and file.filename != '':
                    filename = secure_filename(file.filename)
                    # ছবিটিকে static ফোল্ডারে সেভ করা
                    file.save(os.path.join('static', filename))
                    # ডেটাবেজে ফাইলের নাম বা পাথ সেভ করা
                    Setting.set_value('hero_banner', filename)
            if required_missing:
                flash("Brand name and public email cannot be empty.", "error")
            else:
                for key in DEFAULT_SETTINGS:
                    setting = db.session.get(Setting, key)
                    if setting and key in request.form:
                        setting.value = request.form.get(key, "").strip()[:300]
                db.session.commit()
                flash("Store website settings saved.", "success")
        elif action == "account":
            settings = settings_map()
            current = request.form.get("current_password", "")
            password_setting = db.session.get(Setting, "admin_password_hash")
            username = request.form.get("admin_username", "").strip()[:80]
            email = request.form.get("admin_email", "").strip()[:180]
            new_password = request.form.get("new_password", "")
            if not password_setting or not check_password_hash(password_setting.value, current):
                flash("Current password was incorrect; account settings were not changed.", "error")
            elif not username or not email:
                flash("Admin username and email are required.", "error")
            elif new_password and len(new_password) < 10:
                flash("New password must be at least 10 characters.", "error")
            else:
                for key, value in (("admin_username", username), ("admin_email", email)):
                    setting = db.session.get(Setting, key)
                    setting.value = value
                if new_password:
                    password_setting.value = generate_password_hash(new_password)
                db.session.commit()
        lif
        action == "product":
        product_id = request.form.get("product_id")
        product = db.session.get(Product, int(product_id)) if product_id else Product()
        product.name = request.form.get("name", "").strip()[:140]

        cat_input = request.form.get("category_id", "").strip()
        category_id = None
        if cat_input:
            if cat_input.isdigit():
                category_id = int(cat_input)
            else:
                cat_obj = Category.query.filter_by(name=cat_input).first()
                if not cat_obj:
                    cat_obj = Category(name=cat_input)
                    db.session.add(cat_obj)
                    db.session.commit()
                category_id = cat_obj.id

        if not category_id:
            first_cat = Category.query.first()
            if first_cat:
                category_id = first_cat.id
            else:
                default_cat = Category(name="General")
                db.session.add(default_cat)
                db.session.commit()
                category_id = default_cat.id

        product.category_id = category_id
        product.price = float(request.form.get("price", "0") or 0)
        product.color = request.form.get("color", "#26343b")[:30]
        product.colors = request.form.get("colors", "")[:500]
        product.sizes = request.form.get("sizes", "")[:250]
        product.featured = request.form.get("featured") == "on"

        uploaded = upload_to_supabase(request.files.get("photo"))
        if uploaded:
            product.image = uploaded

        if not product.name:
            flash(message="Product name is required.", category="error")
        else:
            db.session.add(product)
            db.session.commit()
            flash(message="Product saved to the catalog.", category="success")
        elif action == "category":
            name = request.form.get("name", "").strip()[:80]
            slug = re.sub(r"[^a-z0-9]+", "-", name.lower()).strip("-")
            if name and slug and not Category.query.filter_by(slug=slug).first():
                db.session.add(Category(name=name, slug=slug, color=request.form.get("color", "#77796d")[:30]))
                db.session.commit()
                flash("Product category added.", "success")
            else:
                flash("Enter a category name that is not already in the list.", "error")
        elif action == "delete_category":
            category = db.session.get(Category, int(request.form.get("category_id", "0")))
            if category:
                if Product.query.filter_by(category_id=category.id).count():
                    flash("Move this category’s products to another category before removing it.", "error")
                else:
                    db.session.delete(category)
                    db.session.commit()
                    flash("Category removed.", "success")
        elif action == "testimonial":
            testimonial_id = request.form.get("testimonial_id")
            testimonial = db.session.get(Testimonial, int(testimonial_id)) if testimonial_id else Testimonial()
            testimonial.customer_name = request.form.get("customer_name", "").strip()[:120]
            testimonial.location = request.form.get("location", "").strip()[:120]
            testimonial.review = request.form.get("review", "").strip()[:2000]
            testimonial.rating = max(1, min(5, int(request.form.get("rating", "5"))))
            testimonial.active = request.form.get("active") == "on"
            if not testimonial.customer_name or not testimonial.review:
                flash("Review name and review text are required.", "error")
            else:
                db.session.add(testimonial)
                db.session.commit()
                flash("Review saved.", "success")
        elif action == "delete_testimonial":
            testimonial = db.session.get(Testimonial, int(request.form.get("testimonial_id", "0")))
            if testimonial:
                db.session.delete(testimonial)
                db.session.commit()
                flash("Review removed.", "success")
        elif action == "appointment_status":
            appointment = db.session.get(Appointment, int(request.form.get("appointment_id", "0")))
            if appointment:
                appointment.status = request.form.get("status", "New")[:30]
                db.session.commit()
                flash("Appointment status updated.", "success")
        elif action == "inquiry_status":
            inquiry = db.session.get(Inquiry, int(request.form.get("inquiry_id", "0")))
            if inquiry:
                inquiry.status = request.form.get("status", "New")[:30]
                db.session.commit()
                flash("Inquiry status updated.", "success")
        elif action == "order_status":
            order = db.session.get(Order, int(request.form.get("order_id", "0")))
            if order:
                order.status = request.form.get("status", "New")[:30]
                db.session.commit()
                flash("Order status updated.", "success")
        return redirect(url_for("admin"))
    products = Product.query.order_by(Product.id.desc()).all()
    orders = Order.query.order_by(Order.created.desc()).limit(12).all()
    categories = Category.query.order_by(Category.name).all()
    appointments = Appointment.query.order_by(Appointment.preferred_date).limit(40).all()
    inquiries = Inquiry.query.order_by(Inquiry.created.desc()).limit(40).all()
    testimonials = Testimonial.query.order_by(Testimonial.id.desc()).all()
    counts = {"products": Product.query.count(), "orders": Order.query.count(), "appointments": Appointment.query.count(), "inquiries": Inquiry.query.count()}
    return render_template("admin.html", products=products, orders=orders, categories=categories, appointments=appointments, inquiries=inquiries, testimonials=testimonials, counts=counts, settings=settings_map())


@app.get("/health")
def health():
    return {"status": "ok", "database": "connected"}


with app.app_context():
    init_db()


import os

if _name_ == "_main_":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)
