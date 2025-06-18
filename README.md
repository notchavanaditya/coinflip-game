# Coin Flip Casino Game with Hybrid Apex Strategy

Created by: Aditya Raosaheb Chavan

A web-based casino game with a sophisticated betting strategy implementation. The project consists of two main components:

1. `casino_server_with_ui.py` - A Flask-based web server with a beautiful UI
2. `hybrid_apex.py` - A sophisticated betting strategy implementation

## Features

### Casino Game (Web UI)
- Real-time balance tracking with visual chart
- Interactive coin flip betting interface
- 2% house edge on bets
- Detailed game history with win/loss tracking
- Responsive design for all devices

### Hybrid Apex Strategy
- Dual-engine betting system:
  - Growth Engine: Uses tranches to manage risk
  - Recovery Engine: Uses Martingale system for losses
- Profit chipping mechanism
- Real-time API integration
- Configurable parameters for different risk profiles

## Setup

### Prerequisites
- Python 3.7+
- Flask
- Requests library

### Installation
1. Clone the repository:
```bash
git clone https://github.com/notchavanaditya/coinflip-game.git
cd coinflip-game
```

2. Install dependencies:
```bash
pip install flask requests
```

## Running the Casino Server

Start the casino server:
```bash
python casino_server_with_ui.py
```

The server will run on `http://localhost:5000`. Open this URL in your web browser to play the game.

## Running the Hybrid Apex Strategy

In a separate terminal, run:
```bash
python hybrid_apex.py
```

The strategy will automatically connect to the casino server and start executing bets according to its rules.

## Strategy Parameters

The Hybrid Apex strategy uses several configurable parameters:

### Growth Engine
- `TRANCHE_1_LIMIT`: $20.00
- `TRANCHE_2_LIMIT`: $50.00
- `TRANCHE_1_PERCENT`: 10%
- `TRANCHE_2_PERCENT`: 15%
- `TRANCHE_3_PERCENT`: 20%
- `MIN_GROWTH_BET`: $0.25

### Recovery Engine
- `MARTINGALE_BASE_BET`: $1.00
- `MAX_MARTINGALE_STREAK`: 4

### Master Rule
- `PROFIT_CHIP_PERCENTAGE`: 50%

## How It Works

1. The casino server provides a web interface where players can:
   - Set bet amounts
   - Choose heads or tails
   - View their balance history
   - See detailed game results

2. The Hybrid Apex strategy operates on two engines:
   - **Growth Engine**: Uses different betting percentages based on current balance
   - **Recovery Engine**: Uses Martingale system when balance falls below initial

3. The strategy includes a profit chipping mechanism that moves profits to a safe balance when new highs are reached.

## Technical Details

### Casino Server
- Built with Flask
- Uses a 2% house edge (98% payout)
- Maintains player state in memory
- Provides RESTful API endpoints:
  - `/flip`: Place a bet
  - `/status`: Get current status
  - `/reset`: Reset game state

### Strategy Implementation
- Uses requests library for API communication
- Implements sophisticated betting logic
- Includes error handling and state management
- Configurable parameters for different risk profiles

## Contributing

Feel free to submit issues and enhancement requests!

## License

This project is licensed under the MIT License - see the LICENSE file for details.
