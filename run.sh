#!/bin/bash

# Kill any processes already using the game ports
for PORT in 8080 1337 1338; do
  PID=$(lsof -ti tcp:$PORT 2>/dev/null)
  if [ -n "$PID" ]; then
    echo "Killing existing process on port $PORT (PID $PID)..."
    kill -9 $PID
  fi
done

echo "Starting othello.jar..."
java -jar "$(dirname "$0")/othello.jar" --p1-type remote --p2-type random --wait-for-ui &
JAR_PID=$!

echo "othello.jar is running (PID $JAR_PID)"
echo ""
read -rp "Press Enter to start client.py..."
echo ""
echo ""

python3 "$(dirname "$0")/sdks/python/client.py"

wait $JAR_PID
