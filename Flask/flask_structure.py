from flask import Flask, request, jsonify

app = Flask(__name__)

@app.route("/")
def home():
    return "Welcome to Math API! Use /add, /subtract, /multiply, /divide"

@app.route("/add", methods=["GET"])
def add():
    try:
        a = float(request.args.get("a"))
        b = float(request.args.get("b"))
        return jsonify({"operation": "addition", "a": a, "b": b, "result": a + b})
    except Exception as e:
        return jsonify({"error": str(e)}), 400

@app.route("/subtract", methods=["GET"])
def subtract():
    try:
        a = float(request.args.get("a"))
        b = float(request.args.get("b"))
        return jsonify({"operation": "subtraction", "a": a, "b": b, "result": a - b})
    except Exception as e:
        return jsonify({"error": str(e)}), 400

@app.route("/multiply", methods=["GET"])
def multiply():
    try:
        a = float(request.args.get("a"))
        b = float(request.args.get("b"))
        return jsonify({"operation": "multiplication", "a": a, "b": b, "result": a * b})
    except Exception as e:
        return jsonify({"error": str(e)}), 400

@app.route("/divide", methods=["GET"])
def divide():
    try:
        a = float(request.args.get("a"))
        b = float(request.args.get("b"))
        if b == 0:
            return jsonify({"error": "Division by zero is not allowed"}), 400
        return jsonify({"operation": "division", "a": a, "b": b, "result": a / b})
    except Exception as e:
        return jsonify({"error": str(e)}), 400


if __name__ == "__main__":
    app.run(debug=True)