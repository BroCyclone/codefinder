from flask import Flask, render_template, request, redirect, session

app = Flask(__name__)
app.secret_key = "codepayoo"


# ================= LOAD DATA =================
def load_data():

    data = {}

    try:

        with open("data.txt", "r", encoding="utf-8") as f:

            for line in f:

                line = line.strip()

                if not line:
                    continue

                parts = line.split()

                if len(parts) >= 2:

                    phone = parts[0].strip()
                    code = parts[1].strip()

                    data[code] = phone

    except:
        pass

    return data


# ================= SAVE DATA =================
def save_data(data):

    with open("data.txt", "w", encoding="utf-8") as f:

        for code, phone in data.items():

            f.write(f"{phone} {code}\n")


# ================= HOME =================
@app.route("/", methods=["GET", "POST"])
def index():

    data = load_data()

    result = ""

    if request.method == "POST":

        q = request.form.get("query", "").strip()

        # CODE → PHONE
        if q in data:

            result = f"{q} = {data[q]}"

        else:

            # PHONE → CODE
            for code, phone in data.items():

                if q == phone:

                    result = f"{phone} = {code}"
                    break

            if result == "":

                result = "NOT FOUND"

    return render_template(
        "index.html",
        result=result
    )


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
    <html>

    <head>

        <title>Admin Login</title>

        <style>

            body{
                background:#020617;
                color:white;
                font-family:Arial;
                display:flex;
                justify-content:center;
                align-items:center;
                height:100vh;
            }

            form{
                background:#111827;
                padding:30px;
                border-radius:20px;
                width:300px;
            }

            input{
                width:100%;
                padding:14px;
                border:none;
                border-radius:12px;
                margin-top:10px;
            }

            button{
                width:100%;
                padding:14px;
                border:none;
                border-radius:12px;
                margin-top:15px;
                background:#00ffcc;
                font-weight:bold;
            }

        </style>

    </head>

    <body>

        <form method="POST">

            <h2>Admin Login</h2>

            <input
                type="password"
                name="password"
                placeholder="Password"
                required
            >

            <button type="submit">
                LOGIN
            </button>

        </form>

    </body>
    </html>
    '''


# ================= ADMIN =================
@app.route("/admin", methods=["GET", "POST"])
def admin():

    if not session.get("admin"):

        return redirect("/login")

    data = load_data()

    if request.method == "POST":

        phone = request.form.get("phone", "").strip()
        code = request.form.get("code", "").strip()

        if phone and code:

            data[code] = phone

            save_data(data)

    return render_template(
        "admin.html",
        data=data
    )


# ================= DELETE =================
@app.route("/delete/<code>")
def delete(code):

    if not session.get("admin"):

        return redirect("/login")

    data = load_data()

    if code in data:

        del data[code]

        save_data(data)

    return redirect("/admin")


# ================= LOGOUT =================
@app.route("/logout")
def logout():

    session.clear()

    return redirect("/")


# ================= RUN =================
if __name__ == "__main__":

    app.run(
        host="0.0.0.0",
        port=5000,
        debug=True
    )
