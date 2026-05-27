from flask import Flask, render_template, request, redirect, url_for, session

app = Flask(__name__)
app.secret_key = "12345"

DATA_FILE = "data.txt"

def load_data():
    data = {}
    try:
        with open(DATA_FILE, "r") as f:
            for line in f:
                if "=" in line:
                    code, phone = line.strip().split("=")
                    data[code] = phone
    except:
        pass
    return data

def save_data(data):
    with open(DATA_FILE, "w") as f:
        for k, v in data.items():
            f.write(f"{k}={v}\n")

# ================= MAIN SEARCH =================
@app.route("/", methods=["GET", "POST"])
def index():
    data = load_data()
    result = ""

    if request.method == "POST":
        q = request.form.get("query")

        if q in data:
            result = f"{q} → {data[q]}"
        else:
            for k, v in data.items():
                if v == q:
                    result = f"{q} → {k}"
                    break
            if result == "":
                result = "Not Found"

    return render_template("index.html", result=result)

# ================= LOGIN =================
@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        password = request.form.get("password")

        if password == "admin123":
            session["admin"] = True
            return redirect("/admin")
        else:
            return "Wrong Password"

    return '''
    <form method="POST">
        <input name="password" placeholder="Enter password">
        <button>Login</button>
    </form>
    '''

# ================= ADMIN =================
@app.route("/admin", methods=["GET", "POST"])
def admin():
    if not session.get("admin"):
        return redirect("/login")

    data = load_data()
    msg = ""

    if request.method == "POST":
        if "add" in request.form:
            code = request.form.get("code")
            phone = request.form.get("phone")
            data[code] = phone
            save_data(data)
            msg = "Added"

        if "delete" in request.form:
            code = request.form.get("code")
            if code in data:
                del data[code]
                save_data(data)
                msg = "Deleted"

    return render_template("admin.html", data=data, msg=msg)

@app.route("/logout")
def logout():
    session.pop("admin", None)
    return redirect("/")

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
