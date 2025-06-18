import requests
import time
import math

# --- API and Simulation Configuration ---
CASINO_URL = "http://127.0.0.1:5000"
MAX_BETS_PER_RUN = 2000 # Let's do 200 bets for a live demo
INITIAL_BALANCE = 100.0

# --- "Hybrid Apex" Strategy Parameters ---
# Growth Engine
TRANCHE_1_LIMIT = 20.0
TRANCHE_2_LIMIT = 50.0
TRANCHE_1_PERCENT = 0.10
TRANCHE_2_PERCENT = 0.15
TRANCHE_3_PERCENT = 0.20
MIN_GROWTH_BET = 0.25

# Recovery Engine
MARTINGALE_BASE_BET = 1.00
MAX_MARTINGALE_STREAK = 4

# Master Rule
PROFIT_CHIP_PERCENTAGE = 0.50

# --- Helper Functions for API Interaction ---
def place_bet(bet_amount, choice="heads"):
    """Sends a bet to the casino API."""
    try:
        response = requests.post(f"{CASINO_URL}/flip", json={"bet_amount": bet_amount, "choice": choice})
        response.raise_for_status()
        return response.json()
    except requests.exceptions.RequestException as e:
        print(f"--- FATAL: Could not connect to the casino: {e}")
        return None

def reset_casino():
    """Resets the casino balance for a fresh start."""
    print("--- Resetting casino balance to $100.00 ---")
    requests.post(f"{CASINO_URL}/reset")

# --- The Main Strategy Implementation ---
def run_hybrid_apex_strategy():
    """
    Connects to the casino API and executes the Hybrid Apex strategy.
    """
    print("\n" + "="*50)
    print("      STARTING HYBRID APEX STRATEGY CLIENT")
    print("="*50 + "\n")
    
    # --- Initialize Strategy State Variables ---
    active_balance = INITIAL_BALANCE
    safe_balance = 0.0
    high_water_mark = INITIAL_BALANCE
    
    is_in_martingale_recovery = False
    martingale_bet = 0
    martingale_streak = 0
    
    for bet_num in range(1, MAX_BETS_PER_RUN + 1):
        print(f"\n--- Bet #{bet_num} ---")
        print(f"State: Active=${active_balance:.2f} | Safe=${safe_balance:.2f} | Total=${active_balance + safe_balance:.2f}")

        # --- 1. Strategic Decision Point: Choose Engine ---
        if active_balance < INITIAL_BALANCE or is_in_martingale_recovery:
            # --- RECOVERY ENGINE ---
            if not is_in_martingale_recovery:
                print("Engine: RECOVERY ACTIVATED (Active balance < Initial)")
                is_in_martingale_recovery = True
                martingale_bet = MARTINGALE_BASE_BET
                martingale_streak = 0
            
            current_bet = martingale_bet
            print(f"Engine: Recovery Mode | Streak: {martingale_streak} | Bet: ${current_bet:.2f}")

        else:
            # --- GROWTH ENGINE ---
            risk_capital = active_balance - INITIAL_BALANCE
            if risk_capital <= TRANCHE_1_LIMIT:
                current_bet = risk_capital * TRANCHE_1_PERCENT
                print(f"Engine: Growth Tranche 1 | Risk Capital: ${risk_capital:.2f} | Bet: ${current_bet:.2f}")
            elif risk_capital <= TRANCHE_2_LIMIT:
                current_bet = risk_capital * TRANCHE_2_PERCENT
                print(f"Engine: Growth Tranche 2 | Risk Capital: ${risk_capital:.2f} | Bet: ${current_bet:.2f}")
            else:
                current_bet = risk_capital * TRANCHE_3_PERCENT
                print(f"Engine: Growth Tranche 3 | Risk Capital: ${risk_capital:.2f} | Bet: ${current_bet:.2f}")
            
            current_bet = max(current_bet, MIN_GROWTH_BET)

        # Round the bet to 2 decimal places to avoid API issues with tiny fractions
        current_bet = math.ceil(current_bet * 100) / 100

        # --- 2. Sanity Checks ---
        if active_balance < current_bet:
            print(f"--- STRATEGY HALTED: Cannot afford bet of ${current_bet:.2f} with active balance of ${active_balance:.2f}. ---")
            break

        # --- 3. Execute Bet via API ---
        print(f"Placing bet: ${current_bet:.2f}")
        result = place_bet(current_bet)
        if not result or "error" in result:
            print(f"--- API ERROR: {result.get('error', 'Unknown error')} ---")
            break

        # --- 4. Update State Based on Result ---
        is_win = result["win"]
        
        # The API already handles the win/loss deduction, so we just need to sync our active_balance.
        # This is CRITICAL: our local state must match the server state.
        active_balance = result["new_balance"] - safe_balance

        if is_win:
            print(f"Result: WIN! New Active Balance: ${active_balance:.2f}")
            if is_in_martingale_recovery:
                print("Status: Recovery successful. Switching back to Growth Engine.")
                is_in_martingale_recovery = False
        else: # Loss
            print(f"Result: LOSS! New Active Balance: ${active_balance:.2f}")
            if is_in_martingale_recovery:
                martingale_bet *= 2
                martingale_streak += 1
                if martingale_streak >= MAX_MARTINGALE_STREAK:
                    print(f"Status: Max recovery streak ({MAX_MARTINGALE_STREAK}) reached. Halting recovery to prevent deep losses.")
                    is_in_martingale_recovery = False
        
        # --- 5. Master Rule: Chip Profit ---
        total_balance = active_balance + safe_balance
        if total_balance > high_water_mark:
            new_profit = total_balance - high_water_mark
            chip_amount = new_profit * PROFIT_CHIP_PERCENTAGE
            
            # This is a local book-keeping operation
            active_balance -= chip_amount
            safe_balance += chip_amount
            high_water_mark = total_balance
            print(f"PROFIT CHIPPING: New high-water mark! Moved ${chip_amount:.2f} to Safe Balance.")

        time.sleep(0.5) # Pause to make the simulation readable

    # --- Final Result ---
    print("\n" + "="*50)
    print("         SIMULATION VIA API COMPLETE")
    print("="*50)
    final_total_balance = active_balance + safe_balance
    print(f"Final Active Balance: ${active_balance:.2f}")
    print(f"Final Safe Balance:   ${safe_balance:.2f}")
    print(f"Final Total Balance:  ${final_total_balance:.2f}")
    print(f"Total Profit/Loss:    ${final_total_balance - INITIAL_BALANCE:.2f}")
    print("="*50)


# --- Main Execution Block ---
if __name__ == "__main__":
    # Ensure the casino is in a clean state before starting
    reset_casino()
    # Run the strategy
    run_hybrid_apex_strategy()