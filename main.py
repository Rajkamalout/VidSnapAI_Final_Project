from flask import Flask, render_template, request, redirect, url_for, flash
import uuid
from werkzeug.utils import secure_filename
import os

UPLOAD_FOLDER = 'user_uploads'
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg'}

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.secret_key = "secret123"   # NEW (flash messages ke liye)

@app.route("/")
def home():
    return render_template("index.html")

@app.route("/create", methods=["GET", "POST"])
def create():
    myid = uuid.uuid1()

    if request.method == "POST":
        rec_id = request.form.get("uuid")
        desc = request.form.get("text")
        input_files = []

        for key, value in request.files.items():
            file = request.files[key]
            if file:
                filename = secure_filename(file.filename)

                folder_path = os.path.join(app.config['UPLOAD_FOLDER'], rec_id)
                if not os.path.exists(folder_path):
                    os.mkdir(folder_path)

                file.save(os.path.join(folder_path, filename))
                input_files.append(filename)

        # description file
        with open(os.path.join(app.config['UPLOAD_FOLDER'], rec_id, "desc.txt"), "w") as f:
            f.write(desc)

        # input.txt for ffmpeg
        for fl in input_files:
            with open(os.path.join(app.config['UPLOAD_FOLDER'], rec_id, "input.txt"), "a") as f:
                f.write(f"file '{fl}'\nduration 1\n")

    return render_template("create.html", myid=myid)
@app.route("/home")
def dashboard():
    return render_template("index.html")


@app.route("/gallery")
def gallery():
    reels = os.listdir("static/reels")
    return render_template("gallery.html", reels=reels)

@app.route("/login")
def login():
    return render_template("auth/login.html")

@app.route("/register")
def register():
    return render_template("auth/register.html")

@app.before_request
def check_login():
    allowed = ["/login", "/register", "/"]
    if request.path.startswith("/static"):
        return

    if request.path not in allowed:
        return



# 🔴 NEW ROUTE – DELETE REEL
@app.route("/delete_reel/<reel_name>", methods=["POST"])
def delete_reel(reel_name):
    reel_path = os.path.join("static/reels", reel_name)

    if os.path.exists(reel_path):
        os.remove(reel_path)
        flash("Reel deleted successfully ", "success")
    else:
        flash("Reel not found ", "error")

    return redirect(url_for("gallery"))

app.run(debug=True)
