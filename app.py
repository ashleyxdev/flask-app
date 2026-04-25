from flask import Flask, request, render_template, redirect, session, jsonify
import json
import secrets
import os

app = Flask(__name__)
app.secret_key = "dev_secret_key"

authors_db = "data/authors.json"
blogs_db = "data/blogs.json"
os.makedirs('data', exist_ok=True)

def save(db, data):
    with open(db, "w") as f:
        json.dump(data, f)


def load(db):
    try:
        with open(db, "r") as f:
            return json.load(f)
    except:
        return []


authors = load(authors_db)
blogs = load(blogs_db)


def get_current_user():
    return session.get("user", {"is_logged_in": False, "name": ""})


@app.route("/", methods=["GET"])
def index():
    return render_template("index.html", blogs=blogs, author=get_current_user())


@app.route("/register", methods=["GET"])
def register():
    return render_template("registration.html")


@app.route("/login", methods=["GET"])
def login():
    return render_template("login.html")


@app.route("/write-blog", methods=["GET"])
def blog():
    if not session.get("user"):
        return redirect("/login")
    return render_template("write-blog.html")


@app.context_processor
def inject_user():
    return {
        "author": session.get("user", {"is_logged_in": False, "name": ""})
    }
    
@app.route("/health", methods=["GET"])
def health():
    return jsonify({"status": "ok", "uptime": "running"})


@app.route("/register", methods=["POST"])
def handle_registration():
    name = request.form.get("name")
    email = request.form.get("email")
    password = request.form.get("password")

    if not name or not email or not password:
        return render_template("registration.html", message="All fields required")

    for a in authors:
        if a["email"] == email:
            return render_template(
                "registration.html", message="Email already exists!"
            )

    authors.append(
        {
            "id": secrets.token_hex(8),
            "name": name,
            "email": email,
            "password": password,
        }
    )
    save(authors_db, authors)

    return render_template("registration.html", message="Registered successfully")


@app.route("/login", methods=["POST"])
def handle_login():
    email = request.form.get("email")
    password = request.form.get("password")

    for a in authors:
        if a["email"] == email and a["password"] == password:
            session["user"] = {
                "name": a["name"],
                "is_logged_in": True,
            }
            return redirect("/")

    return render_template("login.html", message="Invalid email or password")


@app.route("/logout")
def logout():
    session.pop("user", None)
    return redirect("/")


@app.route("/write-blog", methods=["POST"])
def write_blog():
    user = session.get("user")
    if not user:
        return redirect("/login")

    title = request.form.get("title")
    content = request.form.get("content")

    if not title or not content:
        return "Title and content required"

    blogs.append(
        {
            "id": secrets.token_hex(8),
            "title": title,
            "content": content,
            "author": user["name"],
        }
    )

    save(blogs_db, blogs)
    return redirect("/")


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)