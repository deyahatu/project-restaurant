from flask import Flask, request
import sqlite3

app = Flask(__name__)

@app.route("/", methods=["GET", "POST"])
def home():
    result = ""
    meals = []

    conn = sqlite3.connect("restaurants.db")
    cursor = conn.cursor()

    # get available meals
    cursor.execute("SELECT DISTINCT meal FROM restaurants")
    meals = [row[0] for row in cursor.fetchall()]

    if request.method == "POST":
        typed_meal = request.form.get("typed_meal")
        selected_meal = request.form.get("selected_meal")

        # priority to typed input
        meal = typed_meal if typed_meal else selected_meal

        cursor.execute(
            "SELECT name FROM restaurants WHERE meal = ?",
            (meal,)
        )
        row = cursor.fetchone()

        if row:
            result = f"🍽️ Recommended restaurant: <b>{row[0]}</b>"
        else:
            result = "❌ Sorry, no restaurant found."

    conn.close()

    options = ""
    for m in meals:
        options += f"<option value='{m}'>{m}</option>"

    return f"""
    <!DOCTYPE html>
    <html>
    <head>
        <title>Food Recommendation</title>
        <style>
            body {{
                margin: 0;
                padding: 0;
                font-family: Arial, sans-serif;
                background: linear-gradient(to right, #1e3c72, #2a5298);
                height: 100vh;
                display: flex;
                justify-content: center;
                align-items: center;
            }}

            .card {{
                background: white;
                width: 420px;
                padding: 25px;
                border-radius: 15px;
                box-shadow: 0 15px 30px rgba(0,0,0,0.2);
                text-align: center;
            }}

            img {{
                width: 100%;
                border-radius: 10px;
                margin-bottom: 15px;
            }}

            input, select {{
                width: 80%;
                padding: 10px;
                border-radius: 8px;
                font-size: 16px;
                margin-top: 10px;
            }}

            button {{
                margin-top: 15px;
                padding: 10px 20px;
                border: none;
                border-radius: 8px;
                background-color: #1e90ff;
                color: white;
                font-size: 16px;
                cursor: pointer;
            }}

            .result {{
                margin-top: 20px;
                font-size: 18px;
            }}
        </style>
    </head>

    <body>
        <div class="card">
            <img src="https://images.unsplash.com/photo-1504674900247-0877df9cc836?auto=format&fit=crop&w=800&q=80">
            <h2>Find Your Restaurant</h2>

            <form method="post">
                <input name="typed_meal" placeholder="Type meal (optional)">
                <select name="selected_meal">
                    {options}
                </select>
                <br>
                <button type="submit">Recommend 🍽️</button>
            </form>

            <div class="result">{result}</div>
        </div>
    </body>
    </html>
    """

app.run(host="0.0.0.0", port=5000)

