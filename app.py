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

@app.route("/history/<year>")
def history_detail(year):

    if "user_id" not in session:
        return redirect(url_for("login"))

    history = {

        "1960-1969": {
        "title":"Awal Mula Konsep Jaringan Komputer",
        "image":"Awal Mula Konsep Jaringan Komputer.jpg",
        "location":"Amerika Serikat (UCLA, Stanford Research Institute, UC Santa Barbara, University of Utah)",
        "fact":"ARPANET berhasil menghubungkan empat komputer yang berbeda dan menjadi cikal bakal internet modern.",
        "content":"""
        Pada dekade 1960-an, para peneliti mulai mengembangkan konsep komunikasi data antar komputer. Saat itu komputer masih berukuran sangat besar dan hanya digunakan oleh lembaga pemerintahan maupun universitas. Perkembangan terbesar terjadi pada tahun 1969, ketika proyek ARPANET berhasil menghubungkan empat komputer yang berada di lokasi berbeda.

        Tujuan utama ARPANET adalah:

        1. Menghubungkan komputer yang berada di tempat berbeda.
        2. Memungkinkan pertukaran informasi secara cepat.
        3. Menjamin komunikasi tetap berjalan meskipun sebagian jaringan mengalami gangguan.

        Walaupun belum ada konsep Internet of Things, ARPANET menjadi pondasi utama lahirnya internet yang kelak memungkinkan jutaan perangkat saling terhubung.
        """
        },

       "1982": {
        "title":"Mesin Coca-Cola Menjadi Perangkat IoT Pertama",
        "image":"Mesin Coca-Cola Menjadi Perangkat IoT Pertama.jpg",
        "location":"Carnegie Mellon University, Pittsburgh, Pennsylvania, Amerika Serikat",
        "fact":"Mesin ini dapat memberi tahu apakah minuman masih tersedia dan sudah dingin sebelum seseorang berjalan menuju mesin. Banyak yang menganggapnya sebagai perangkat IoT pertama di dunia..",
        "content":"""
        Tahun 1982 menjadi salah satu tonggak sejarah paling penting dalam perkembangan IoT. Sekelompok mahasiswa di Carnegie Mellon University memodifikasi mesin penjual minuman Coca-Cola agar dapat terhubung ke internet.

        Mesin tersebut mampu memberikan informasi secara real-time mengenai:

        1. Jumlah minuman yang masih tersedia.
        2. Posisi setiap botol.
        3. Apakah minuman sudah dingin atau belum.

        Informasi tersebut dapat diakses dari komputer melalui jaringan.
        """
        },

        "1990":{
        "title":"Internet Toaster",
        "image":"Internet_Toaster.jpg",
        "location":"Ajang Interop, Amerika Serikat",
        "fact":"John Romkey berhasil menghubungkan pemanggang roti ke internet menggunakan TCP/IP. Perangkat ini dapat dinyalakan dari jarak jauh, menjadi contoh awal smart home.",
        "content":"""
        Pada tahun 1990, John Romkey memperkenalkan Internet Toaster, yaitu pemanggang roti yang dapat dikendalikan melalui internet. Awalnya toaster hanya dapat dinyalakan dari jarak jauh. Kemudian sistem dikembangkan sehingga lengan robot dapat memasukkan roti secara otomatis.

        Dampak demonstrasi ini menunjukkan bahwa:

        1. Peralatan rumah tangga dapat dikontrol melalui internet.
        2. Internet tidak hanya digunakan oleh komputer, tetapi juga benda sehari-hari.

        Konsep Smart Home mulai mendapat perhatian para peneliti.
        """
        },

        "1991-1998":{
        "title":"Embedded System dan Wireless Sensor",
        "image":"Embedded System dan Wireless Sensor.jpg",
        "location":"Xerox PARC, California, Amerika Serikat",
        "fact":"Mark Weiser memperkenalkan konsep bahwa komputer akan menghilang ke dalam kehidupan sehari-hari. Gagasan ini menjadi landasan filosofis IoT modern.",
        "content":"""
        Pada periode ini perkembangan perangkat keras meningkat sangat pesat. Teknologi yang berkembang meliputi:

        1. Mikrokontroler.
        2. Sensor digital.
        3. RFID.
        4. Bluetooth.
        5. Wireless Sensor Network (WSN).

        Harga komponen elektronik mulai turun sehingga banyak penelitian dilakukan mengenai otomatisasi industri. Perangkat mampu:

        1. Mengukur suhu.
        2. Mengukur kelembapan.
        3. Mengukur tekanan.
        4. Mengukur getaran.
        5. Mengirim data secara otomatis.

        Inilah awal berkembangnya sistem monitoring modern.
        """
        },

        "1999":{
        "title":"Lahirnya Istilah Internet of Things (IoT)",
        "image":"Lahirnya Istilah Internet of Things (IoT).jpg",
        "location":"Procter & Gamble, Amerika Serikat",
        "fact":"Kevin Ashton menggunakan istilah Internet of Things saat mempresentasikan penggunaan RFID dalam manajemen rantai pasok.",
        "content":"""
        Tahun 1999, istilah Internet of Things (IoT) pertama kali diperkenalkan oleh Kevin Ashton saat bekerja di Procter & Gamble. Saat itu ia sedang mengembangkan sistem pelacakan produk menggunakan teknologi RFID.

        Kevin Ashton berpendapat bahwa:

        "Komputer akan menjadi jauh lebih pintar apabila dapat mengumpulkan data secara otomatis dari benda-benda di dunia nyata."

        Ia memperkenalkan konsep bahwa setiap benda dapat memiliki identitas digital dan berkomunikasi melalui internet tanpa campur tangan manusia.

        Dampak:
        1. Istilah Internet of Things mulai dikenal dunia.
        2. RFID mulai digunakan secara luas.
        3. Penelitian mengenai IoT semakin berkembang.
        """
        },

        "2010-2013": {
        "title":"Era Smartphone dan Cloud Computing",
        "image":"Era Smartphone dan Cloud Computing.jpg",
        "location":"Global",
        "fact":"Smartphone menjadi pusat kendali perangkat pintar seperti lampu, kamera, TV, dan thermostat melalui aplikasi seluler.",
        "content":"""
        Kemunculan smartphone mengubah perkembangan IoT secara drastis. Smartphone menjadi pusat pengendali berbagai perangkat.

        Pada periode ini berkembang:

        1. Android
        2. iOS
        3. Cloud Computing
        4. Wi-Fi murah
        5. Mobile Internet

        Muncul berbagai perangkat Smart Home seperti:

        1. Lampu pintar
        2. Kamera CCTV online
        3. Smart Plug
        4. Smart TV
        5. Smart Lock
        6. Smart Thermostat

        Pengguna dapat mengontrol rumah hanya menggunakan smartphone.
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