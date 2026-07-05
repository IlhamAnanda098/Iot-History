from flask import Flask, render_template, request, redirect, url_for, session, flash
from werkzeug.security import generate_password_hash, check_password_hash
from models import db, User

app = Flask(__name__)

app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///database.db"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
app.config["SECRET_KEY"] = "iot-secret-key"

import os

BASE_DIR = os.path.abspath(os.path.dirname(__file__))

os.makedirs(os.path.join(BASE_DIR, "instance"), exist_ok=True)

db_path = os.path.join(BASE_DIR, "instance", "database.db")

app.config["SQLALCHEMY_DATABASE_URI"] = f"sqlite:///{db_path}"

db.init_app(app)

with app.app_context():
    db.create_all()

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/home")
def home():

    if "user_id" not in session:
        return redirect(url_for("login"))

    return render_template(
        "home.html",
        name=session["user_name"]
    )

@app.route("/about")
def about():

    if "user_id" not in session:
        return redirect(url_for("login"))

    return render_template("about.html")

@app.route("/list")
def list_history():

    if "user_id" not in session:
        return redirect(url_for("login"))

    return render_template("list.html")

@app.route("/history/<int:year>")
def history_detail(year):

    if "user_id" not in session:
        return redirect(url_for("login"))

    history = {

        1960-1969:{
        "title":"Awal Mula Konsep Jaringan Komputer",
        "image":"Awal Mula Konsep Jaringan Komputer.jpg",
        "location":"Amerika Serikat (UCLA, Stanford Research Institute, UC Santa Barbara, University of Utah)",
        "fact":"ARPANET berhasil menghubungkan empat komputer yang berbeda dan menjadi cikal bakal internet modern.",
        "content":"""
        Pada dekade 1960-an, para peneliti mulai mengembangkan konsep komunikasi data antar komputer. Saat itu komputer masih berukuran sangat besar dan hanya digunakan oleh lembaga pemerintahan maupun universitas.

        Perkembangan terbesar terjadi pada tahun 1969, ketika proyek ARPANET berhasil menghubungkan empat komputer yang berada di lokasi berbeda.

        Tujuan utama ARPANET adalah:

        1. Menghubungkan komputer yang berada di tempat berbeda.
        2. Memungkinkan pertukaran informasi secara cepat.
        3. Menjamin komunikasi tetap berjalan meskipun sebagian jaringan mengalami gangguan.

        Walaupun belum ada konsep Internet of Things, ARPANET menjadi pondasi utama lahirnya internet yang kelak memungkinkan jutaan perangkat saling terhubung.
        """
        },

        1990:{
        "title":"Internet Toaster",
        "image":"toaster_1990.jpg",
        "location":"Interop Conference",
        "fact":"Peralatan rumah pertama yang dikendalikan internet.",
        "content":"""
        John Romkey membuat toaster yang dapat dinyalakan
        melalui internet.

        Demonstrasi ini menunjukkan bahwa benda sehari-hari
        dapat dikendalikan dari jarak jauh menggunakan jaringan.
        """
        },

        1999:{
        "title":"Kevin Ashton",
        "image":"kevin_ashton.jpg",
        "location":"MIT Auto-ID Center",
        "fact":"Lahirnya istilah Internet of Things.",
        "content":"""
        Kevin Ashton memperkenalkan istilah
        Internet of Things ketika menjelaskan penggunaan RFID
        untuk rantai pasok.

        Istilah tersebut kemudian menjadi dasar perkembangan
        teknologi IoT modern.
        """
        },

        2005:{
        "title":"ITU",
        "image":"itu_2005.jpg",
        "location":"International Telecommunication Union",
        "fact":"IoT mulai dikenal dunia.",
        "content":"""
        ITU menerbitkan laporan yang menjelaskan bagaimana
        Internet of Things akan mengubah kehidupan manusia.

        Sejak saat itu perkembangan IoT semakin pesat.
        """
        },

        2015:{
        "title":"Smart Home",
        "image":"smart_home.jpg",
        "location":"Global",
        "fact":"IoT mulai digunakan masyarakat.",
        "content":"""
        Lampu pintar, kamera CCTV,
        smart speaker,
        dan berbagai perangkat rumah mulai
        menggunakan teknologi IoT.
        """
        },

        2020:{
        "title":"Era Industri 4.0",
        "image":"smart_city.jpg",
        "location":"Seluruh Dunia",
        "fact":"IoT berkembang di hampir semua sektor.",
        "content":"""
        IoT digunakan pada

        • Smart City

        • Smart Agriculture

        • Smart Healthcare

        • Smart Transportation

        • Smart Factory

        hingga saat ini.
        """
        }

        }

    data = history.get(year)

    if data is None:
        return "Data tidak ditemukan"

    return render_template(
        "detail.html",
        history=data,
        year=year
    )

@app.route("/register", methods=["GET", "POST"])
def register():

    if request.method == "POST":

        name = request.form["name"]
        email = request.form["email"]
        password = generate_password_hash(request.form["password"])

        existing_user = User.query.filter_by(email=email).first()

        if existing_user:
            flash("Email sudah terdaftar!", "danger")
            return redirect(url_for("register"))

        user = User(
            name=name,
            email=email,
            password=password
        )

        db.session.add(user)
        db.session.commit()
        
        

        flash("Registrasi berhasil! Silakan login.", "success")

        return redirect(url_for("login"))

        return redirect(url_for("index"))

    return render_template("register.html")

@app.route("/login", methods=["GET", "POST"])
def login():

    if request.method == "POST":

        email = request.form["email"]
        password = request.form["password"]

        user = User.query.filter_by(email=email).first()

        if user and check_password_hash(user.password, password):

            session["user_id"] = user.id
            session["user_name"] = user.name

            return redirect(url_for("home"))

        flash("Email atau password salah.", "danger")
        return redirect(url_for("login"))

    return render_template("login.html")

@app.route("/logout")
def logout():

    session.clear()

    return redirect(url_for("login"))

if __name__ == "__main__":
    app.run(debug=True)