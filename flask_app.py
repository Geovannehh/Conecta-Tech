"""Aplicação WSGI do Conecta Campus para PythonAnywhere."""

from __future__ import annotations

import os
import secrets
import sqlite3
from functools import wraps
from pathlib import Path
from typing import Any

from flask import Flask, abort, flash, g, jsonify, redirect, render_template, request, session, url_for
from werkzeug.security import check_password_hash

from campus_data import CATEGORIES, HELP_ITEMS, JOURNEYS, SECTORS

BASE_DIR = Path(__file__).resolve().parent
INSTANCE_DIR = BASE_DIR / "instance"
DATABASE_PATH = Path(os.getenv("DATABASE_PATH", INSTANCE_DIR / "conecta_campus.db"))


def _secret_key() -> str:
    configured = os.getenv("SECRET_KEY")
    if configured:
        return configured
    INSTANCE_DIR.mkdir(parents=True, exist_ok=True)
    secret_file = INSTANCE_DIR / ".secret_key"
    if not secret_file.exists():
        secret_file.write_text(secrets.token_hex(32), encoding="utf-8")
    return secret_file.read_text(encoding="utf-8").strip()


app = Flask(__name__, template_folder="templates", static_folder="static")
app.config.update(
    SECRET_KEY=_secret_key(),
    MAX_CONTENT_LENGTH=32 * 1024,
    SESSION_COOKIE_HTTPONLY=True,
    SESSION_COOKIE_SAMESITE="Lax",
    SESSION_COOKIE_SECURE=os.getenv("COOKIE_SECURE", "0") == "1",
)


def get_db() -> sqlite3.Connection:
    if "db" not in g:
        DATABASE_PATH.parent.mkdir(parents=True, exist_ok=True)
        connection = sqlite3.connect(DATABASE_PATH, timeout=15)
        connection.row_factory = sqlite3.Row
        connection.execute("PRAGMA foreign_keys = ON")
        connection.execute("PRAGMA journal_mode = WAL")
        g.db = connection
    return g.db


@app.teardown_appcontext
def close_db(_error: BaseException | None = None) -> None:
    connection = g.pop("db", None)
    if connection is not None:
        connection.close()


def init_db() -> None:
    db = get_db()
    db.executescript(
        """
        CREATE TABLE IF NOT EXISTS interactions (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            type TEXT NOT NULL,
            profile TEXT NOT NULL DEFAULT 'visitante',
            category TEXT NOT NULL DEFAULT 'geral',
            reference TEXT NOT NULL DEFAULT '',
            created_at TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP
        );
        CREATE INDEX IF NOT EXISTS interactions_category_idx ON interactions(category);
        CREATE INDEX IF NOT EXISTS interactions_created_at_idx ON interactions(created_at);

        CREATE TABLE IF NOT EXISTS suggestions (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            profile TEXT NOT NULL,
            category TEXT NOT NULL,
            message TEXT NOT NULL,
            status TEXT NOT NULL DEFAULT 'nova',
            created_at TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP
        );
        CREATE INDEX IF NOT EXISTS suggestions_created_at_idx ON suggestions(created_at);

        CREATE TABLE IF NOT EXISTS ratings (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            sector TEXT NOT NULL,
            score INTEGER NOT NULL CHECK (score BETWEEN 1 AND 5),
            comment TEXT NOT NULL DEFAULT '',
            created_at TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP
        );
        CREATE INDEX IF NOT EXISTS ratings_sector_idx ON ratings(sector);

        CREATE TABLE IF NOT EXISTS admins (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT NOT NULL UNIQUE,
            password_hash TEXT NOT NULL,
            created_at TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP
        );
        """
    )
    db.commit()


with app.app_context():
    init_db()


@app.after_request
def security_headers(response):
    response.headers["X-Content-Type-Options"] = "nosniff"
    response.headers["X-Frame-Options"] = "SAMEORIGIN"
    response.headers["Referrer-Policy"] = "strict-origin-when-cross-origin"
    response.headers["Permissions-Policy"] = "geolocation=(), camera=(), microphone=()"
    return response


@app.get("/")
def home():
    return render_template(
        "index.html",
        help_items=HELP_ITEMS,
        journeys=JOURNEYS,
        categories=CATEGORIES,
        sectors=SECTORS,
    )


@app.get("/health")
def health():
    return jsonify(status="ok", service="conecta-campus")


@app.post("/api/interactions")
def record_interaction():
    payload = _json_body()
    interaction_type = _clean(payload.get("type"), 40)
    profile = _clean(payload.get("profile"), 20) or "visitante"
    category = _clean(payload.get("category"), 60) or "geral"
    reference = _clean(payload.get("reference"), 120)
    if interaction_type not in {"profile_selected", "help_viewed", "journey_viewed", "mission_completed"}:
        return jsonify(error="Interação inválida."), 400
    if profile not in {"calouro", "professor", "visitante"}:
        return jsonify(error="Perfil inválido."), 400
    db = get_db()
    db.execute(
        "INSERT INTO interactions (type, profile, category, reference) VALUES (?, ?, ?, ?)",
        (interaction_type, profile, category, reference),
    )
    db.commit()
    return jsonify(ok=True), 201


@app.post("/api/suggestions")
def create_suggestion():
    payload = _json_body()
    profile = _clean(payload.get("profile"), 20)
    category = _clean(payload.get("category"), 40)
    message = _clean(payload.get("message"), 1200)
    if profile not in {"calouro", "professor"}:
        return jsonify(error="Perfil inválido."), 400
    if category not in {"Informação", "Atendimento", "Estrutura", "Acolhimento", "Outro"}:
        return jsonify(error="Categoria inválida."), 400
    if len(message) < 10:
        return jsonify(error="Escreva ao menos 10 caracteres."), 400
    db = get_db()
    db.execute(
        "INSERT INTO suggestions (profile, category, message) VALUES (?, ?, ?)",
        (profile, category, message),
    )
    db.commit()
    return jsonify(ok=True), 201


@app.post("/api/ratings")
def create_rating():
    payload = _json_body()
    sector = _clean(payload.get("sector"), 80)
    comment = _clean(payload.get("comment"), 800)
    try:
        score = int(payload.get("score", 0))
    except (TypeError, ValueError):
        score = 0
    if sector not in SECTORS or score not in range(1, 6):
        return jsonify(error="Selecione um setor e uma nota de 1 a 5."), 400
    db = get_db()
    db.execute(
        "INSERT INTO ratings (sector, score, comment) VALUES (?, ?, ?)",
        (sector, score, comment),
    )
    db.commit()
    return jsonify(ok=True), 201


def admin_required(view):
    @wraps(view)
    def wrapped(*args, **kwargs):
        if not session.get("admin_id"):
            return redirect(url_for("admin_login", next=request.path))
        return view(*args, **kwargs)

    return wrapped


@app.route("/admin/login", methods=["GET", "POST"])
def admin_login():
    token = session.setdefault("csrf_token", secrets.token_urlsafe(24))
    if request.method == "POST":
        if not secrets.compare_digest(request.form.get("csrf_token", ""), token):
            abort(400)
        username = _clean(request.form.get("username"), 80)
        password = request.form.get("password", "")[:256]
        admin = get_db().execute(
            "SELECT id, username, password_hash FROM admins WHERE username = ?",
            (username,),
        ).fetchone()
        if admin and check_password_hash(admin["password_hash"], password):
            session.clear()
            session["admin_id"] = admin["id"]
            session["admin_username"] = admin["username"]
            return redirect(url_for("admin_dashboard"))
        flash("Usuário ou senha inválidos.", "error")
    admin_count = get_db().execute("SELECT COUNT(*) FROM admins").fetchone()[0]
    return render_template("admin_login.html", csrf_token=token, admin_count=admin_count)


@app.post("/admin/logout")
def admin_logout():
    session.clear()
    return redirect(url_for("home"))


@app.get("/admin")
@admin_required
def admin_dashboard():
    db = get_db()
    total_interactions = db.execute("SELECT COUNT(*) FROM interactions").fetchone()[0]
    suggestions_count = db.execute("SELECT COUNT(*) FROM suggestions").fetchone()[0]
    average_rating = db.execute("SELECT ROUND(AVG(score), 1) FROM ratings").fetchone()[0]
    categories = db.execute(
        "SELECT category, COUNT(*) AS count FROM interactions GROUP BY category ORDER BY count DESC, category LIMIT 6"
    ).fetchall()
    sector_ratings = db.execute(
        "SELECT sector, ROUND(AVG(score), 1) AS average, COUNT(*) AS count FROM ratings GROUP BY sector ORDER BY average DESC, count DESC"
    ).fetchall()
    recent_suggestions = db.execute(
        "SELECT id, profile, category, message, status, created_at FROM suggestions ORDER BY created_at DESC, id DESC LIMIT 8"
    ).fetchall()
    return render_template(
        "admin.html",
        total_interactions=total_interactions,
        suggestions_count=suggestions_count,
        average_rating=average_rating,
        categories=categories,
        sector_ratings=sector_ratings,
        recent_suggestions=recent_suggestions,
        top_category=categories[0]["category"] if categories else "Sem dados",
        max_category=max((row["count"] for row in categories), default=1),
        username=session.get("admin_username", "gestor"),
    )


def _json_body() -> dict[str, Any]:
    if not request.is_json:
        abort(415)
    payload = request.get_json(silent=True)
    if not isinstance(payload, dict):
        abort(400)
    return payload


def _clean(value: Any, max_length: int) -> str:
    return value.strip()[:max_length] if isinstance(value, str) else ""


if __name__ == "__main__":
    app.run(host="127.0.0.1", port=5000, debug=True)
