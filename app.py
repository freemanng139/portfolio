import ipaddress
import json
import os
import re
import secrets
from datetime import datetime
from pathlib import Path

from flask import Flask, abort, jsonify, render_template, request

from data import PROFILE, PROJECTS, SKILLS, TIMELINE, QUIZ, CERTIFS

BASE = Path(__file__).parent
DATA_DIR = BASE / "data"
MESSAGES_FILE = DATA_DIR / "messages.json"
SUBSCRIBERS_FILE = DATA_DIR / "subscribers.json"
STATS_FILE = DATA_DIR / "stats.json"
EMAIL_RE = re.compile(r"^[^@\s]+@[^@\s]+\.[^@\s]+$")

app = Flask(__name__)
app.secret_key = os.environ.get("SECRET_KEY") or secrets.token_hex(32)
app.config.update(
    MAX_CONTENT_LENGTH=1 * 1024 * 1024,
    SESSION_COOKIE_HTTPONLY=True,
    SESSION_COOKIE_SAMESITE="Lax",
    TEMPLATES_AUTO_RELOAD=True,
    SEND_FILE_MAX_AGE_DEFAULT=0,
)


def _read_json(path, default):
    try:
        return json.loads(path.read_text(encoding="utf-8"))
    except (FileNotFoundError, json.JSONDecodeError):
        return default


def _write_json(path, data):
    DATA_DIR.mkdir(exist_ok=True)
    tmp_path = path.with_suffix(".tmp")
    tmp_path.write_text(json.dumps(data, ensure_ascii=False, indent=2), encoding="utf-8")
    tmp_path.replace(path)


def _is_safe_origin(req):
    origin = req.headers.get("Origin")
    if origin:
        return origin.rstrip("/") == req.host_url.rstrip("/")
    referer = req.headers.get("Referer")
    if referer:
        return referer.startswith(req.host_url)
    return True


@app.context_processor
def inject_globals():
    return {"profile": PROFILE, "year": datetime.now().year}


@app.after_request
def set_security_headers(response):
    response.headers["X-Content-Type-Options"] = "nosniff"
    response.headers["X-Frame-Options"] = "SAMEORIGIN"
    response.headers["Referrer-Policy"] = "strict-origin-when-cross-origin"
    response.headers["Permissions-Policy"] = "geolocation=(), microphone=(), camera=()"
    response.headers["Cross-Origin-Opener-Policy"] = "same-origin"
    response.headers["Content-Security-Policy"] = (
        "default-src 'self'; "
        "script-src 'self' 'unsafe-inline'; "
        "style-src 'self' 'unsafe-inline' https://fonts.googleapis.com; "
        "font-src 'self' https://fonts.gstatic.com; "
        "img-src 'self' data:; "
        "connect-src 'self';"
    )
    return response


@app.route("/")
def index():
    stats = _read_json(STATS_FILE, {"visits": 0})
    stats["visits"] = int(stats.get("visits", 0) or 0) + 1
    _write_json(STATS_FILE, stats)
    return render_template(
        "index.html",
        projects=PROJECTS,
        skills=SKILLS,
        timeline=TIMELINE,
        certifs=CERTIFS,
        visits=stats["visits"],
    )


@app.route("/projets/<slug>")
def project_detail(slug):
    project = next((p for p in PROJECTS if p["slug"] == slug), None)
    if not project:
        abort(404)
    idx = PROJECTS.index(project)
    nxt = PROJECTS[(idx + 1) % len(PROJECTS)]
    p_data = dict(project)
    p_data["num"] = f"{idx + 1:02d}"
    return render_template("project.html", p=p_data, next_project=nxt)


@app.route("/labo")
def lab():
    return render_template("lab.html")


@app.errorhandler(404)
def not_found(_e):
    return render_template("404.html"), 404


@app.post("/api/contact")
def api_contact():
    if not _is_safe_origin(request):
        return jsonify(ok=False, message="Requête non autorisée."), 403
    data = request.get_json(silent=True) or request.form
    name = " ".join((data.get("name") or "").split())
    email = (data.get("email") or "").strip().lower()
    subject = " ".join((data.get("subject") or "").split())[:120]
    message = (data.get("message") or "").strip()

    errors = {}
    if len(name) < 2 or len(name) > 80:
        errors["name"] = "Nom entre 2 et 80 caractères."
    if not EMAIL_RE.match(email) or len(email) > 120:
        errors["email"] = "Adresse e-mail invalide."
    if len(message) < 10 or len(message) > 2000:
        errors["message"] = "Message entre 10 et 2000 caractères."
    if data.get("website"):
        errors["bot"] = "Rejeté."
    if errors:
        return jsonify(ok=False, errors=errors), 400

    messages = _read_json(MESSAGES_FILE, [])
    messages.append({
        "name": name, "email": email, "subject": subject,
        "message": message, "date": datetime.now().isoformat(timespec="seconds"),
    })
    if len(messages) > 1000:
        messages = messages[-1000:]
    _write_json(MESSAGES_FILE, messages)
    return jsonify(ok=True, message=f"Merci {name} ! Votre message a bien été reçu.")


@app.post("/api/subscribe")
def api_subscribe():
    if not _is_safe_origin(request):
        return jsonify(ok=False, message="Requête non autorisée."), 403
    data = request.get_json(silent=True) or request.form
    email = (data.get("email") or "").strip().lower()
    if not EMAIL_RE.match(email) or len(email) > 120:
        return jsonify(ok=False, message="Veuillez entrer une adresse e-mail valide."), 400

    now = datetime.now().isoformat(timespec="seconds")
    subscribers = _read_json(SUBSCRIBERS_FILE, [])
    if not any(s.get("email") == email for s in subscribers):
        subscribers.append({"email": email, "date": now})
        if len(subscribers) > 1000:
            subscribers = subscribers[-1000:]
        _write_json(SUBSCRIBERS_FILE, subscribers)

    messages = _read_json(MESSAGES_FILE, [])
    messages.append({
        "name": "Contact direct (Email)",
        "email": email,
        "subject": "Nouvelle prise de contact rapide",
        "message": f"Prise de contact rapide via formulaire email : {email}",
        "date": now,
    })
    if len(messages) > 1000:
        messages = messages[-1000:]
    _write_json(MESSAGES_FILE, messages)

    return jsonify(ok=True, message="Merci ! Votre e-mail a bien été envoyé.")


@app.get("/api/subnet")
def api_subnet():
    raw = request.args.get("cidr", "").strip()
    if not raw or len(raw) > 50:
        return jsonify(ok=False, error="Format attendu : 192.168.1.10/24"), 400
    try:
        iface = ipaddress.ip_interface(raw)
        if iface.version != 4:
            raise ValueError
    except ValueError:
        return jsonify(ok=False, error="Format attendu : 192.168.1.10/24"), 400
    net = iface.network
    hosts = net.num_addresses - 2 if net.prefixlen < 31 else net.num_addresses
    first = net.network_address + 1 if net.prefixlen < 31 else net.network_address
    last = net.broadcast_address - 1 if net.prefixlen < 31 else net.broadcast_address
    first_octet = int(str(iface.ip).split(".")[0])
    cls = "A" if first_octet < 128 else "B" if first_octet < 192 else "C" if first_octet < 224 else "D/E"
    return jsonify(
        ok=True,
        ip=str(iface.ip),
        network=str(net.network_address),
        broadcast=str(net.broadcast_address),
        netmask=str(net.netmask),
        wildcard=str(net.hostmask),
        prefix=net.prefixlen,
        hosts=hosts,
        range=f"{first} – {last}",
        ip_class=cls,
        private=iface.ip.is_private,
        binary_mask=".".join(f"{int(o):08b}" for o in str(net.netmask).split(".")),
    )


@app.get("/api/quiz")
def api_quiz():
    return jsonify([{"q": q["q"], "choices": q["choices"]} for q in QUIZ])


@app.post("/api/quiz")
def api_quiz_check():
    answers = (request.get_json(silent=True) or {}).get("answers", [])
    if not isinstance(answers, list):
        return jsonify(ok=False, error="Format invalide"), 400
    results = []
    for i, q in enumerate(QUIZ):
        given = answers[i] if i < len(answers) else None
        results.append({"correct": given == q["answer"], "answer": q["answer"], "explain": q["explain"]})
    score = sum(r["correct"] for r in results)
    return jsonify(score=score, total=len(QUIZ), results=results)


@app.get("/api/stats")
def api_stats():
    return jsonify(
        visits=_read_json(STATS_FILE, {"visits": 0})["visits"],
        messages=len(_read_json(MESSAGES_FILE, [])),
        projects=len(PROJECTS),
    )


@app.errorhandler(413)
def request_entity_too_large(_e):
    return jsonify(ok=False, message="Données trop volumineuses."), 413


if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    debug = os.environ.get("FLASK_DEBUG", "False").lower() in ("true", "1", "yes")
    app.run(host="0.0.0.0", port=port, debug=debug)
