# AOthello

## My Solution

The bot is located in `sdks/python/`. It uses a minimax search algorithm with configurable depth, positional weighting, and mobility scoring to select the best move each turn.

### Acknowledgements

This solution was developed with the assistance of Claude (Anthropic's AI). The AI strategy was inspired by and referenced from [this article on Othello AI with alpha-beta search](https://medium.com/@jackychoi26/how-to-write-an-othello-ai-with-alpha-beta-search-58131ffe67eb).

### Prerequisites

- **Java 17+** — to run the game server (`othello.jar`)
- **Python 3.5+** — to run the bot (no external packages required)

### Running the bot

**Option 1 — Bash script (macOS / Linux / WSL):**

Run the server and client together with a prompt between them:
```
./run_server_and_client.sh
```

Or run them separately in two terminals:
```
./run_server.sh       # Terminal 1: starts the game server
./run_client.sh       # Terminal 2: starts the bot
```

**Option 2 — Manual (any OS):**

In one terminal:
```
java -jar othello.jar --p1-type remote --p2-type random --wait-for-ui
```
In a second terminal:
```
python3 sdks/python/client.py
```

Then open http://localhost:8080 in a browser to watch the game.

### Running the tests

```
python3 -m pytest sdks/python/test.py
```
