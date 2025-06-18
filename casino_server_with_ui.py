from flask import Flask, request, jsonify, render_template
import random

# --- Basic Setup ---
app = Flask(__name__)

# --- Casino State ---
# This is the "upgraded" part: history is a regular list, so it has no size limit.
# This allows for the full balance graph.
player_state = {
    "balance": 100.00,
    "history": [] 
}

# --- Game Logic ---
def flip_coin():
    """Simulates a fair coin flip."""
    return random.choice(["heads", "tails"])

# --- UI Route ---
@app.route("/")
def home():
    """Serves the main HTML page that acts as the UI."""
    return render_template(
        "index.html", 
        current_balance=player_state['balance'],
        history=player_state['history']
    )

# --- API Endpoints ---

@app.route("/status", methods=["GET"])
def get_status():
    """API endpoint to check current status."""
    return jsonify({
        "balance": player_state["balance"],
        "history": player_state["history"]
    })

@app.route("/reset", methods=["POST"])
def reset_game():
    """API endpoint to reset the game to its initial state."""
    player_state["balance"] = 100.00
    player_state["history"].clear()
    return jsonify({
        "message": "Player balance has been reset.",
        "new_balance": player_state["balance"],
        "history": player_state["history"]
    })

@app.route("/flip", methods=["POST"])
def play_flip():
    """The main game API endpoint, used by both the UI and your scripts."""
    try:
        data = request.get_json()
        bet_amount = float(data["bet_amount"])
        player_choice = data["choice"].lower()
    except Exception as e:
        return jsonify({"error": f"Invalid request. Details: {e}"}), 400

    if bet_amount > player_state["balance"]:
        return jsonify({"error": "Insufficient funds.", "your_balance": player_state['balance']}), 400
    if bet_amount <= 0:
        return jsonify({"error": "Bet amount must be positive."}), 400

    outcome = flip_coin()
    win = (player_choice == outcome)
    
    # Using the 2% house edge version.
    if win:
        winnings = bet_amount * 0.98 
        player_state["balance"] += winnings
        result_message = f"Win (+${winnings:.2f})"
        message_for_ui = f"You won ${winnings:.2f}! (2% house edge)"
    else:
        player_state["balance"] -= bet_amount
        result_message = f"Loss (-${bet_amount:.2f})"
        message_for_ui = f"You lost ${bet_amount:.2f}."

    # Create a log entry for the history
    log_entry = {
        "choice": player_choice.capitalize(),
        "outcome": outcome.capitalize(),
        "result": result_message,
        "balance_after": round(player_state["balance"], 2)
    }
    # Add the new log to the beginning of the history list
    player_state["history"].insert(0, log_entry)

    # Return the complete state to the client
    return jsonify({
        "player_choice": player_choice,
        "outcome": outcome,
        "win": win,
        "bet_amount": bet_amount,
        "message": message_for_ui,
        "new_balance": round(player_state["balance"], 2),
        "history": player_state["history"]
    })

# --- Run the Server ---
if __name__ == "__main__":
    app.run(debug=True, port=5000)