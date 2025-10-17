#!/bin/bash

echo "=== Остановка старых процессов ==="
pkill -f "uvicorn app.main:app"
pkill -f "streamlit run operator_app.py"
pkill -f "streamlit run moderator_app.py"
pkill -f "cloudflared tunnel"
sleep 2

echo "=== Запуск Backend API ==="
cd /home/kate/T1-hackathon/backend
nohup python3.13 -m uvicorn app.main:app --host 0.0.0.0 --port 8000 > /tmp/backend.log 2>&1 &
BACKEND_PID=$!
disown $BACKEND_PID
echo "Backend запущен (PID: $BACKEND_PID, лог: /tmp/backend.log)"

sleep 3

echo "=== Запуск Operator UI ==="
cd /home/kate/T1-hackathon/frontend
nohup python3.13 -m streamlit run operator_app.py --server.port=8501 --server.address=0.0.0.0 > /tmp/operator.log 2>&1 &
OPERATOR_PID=$!
disown $OPERATOR_PID
echo "Operator UI запущен (PID: $OPERATOR_PID, лог: /tmp/operator.log)"

sleep 2

echo "=== Запуск Moderator UI ==="
cd /home/kate/T1-hackathon/frontend
nohup python3.13 -m streamlit run moderator_app.py --server.port=8502 --server.address=0.0.0.0 > /tmp/moderator.log 2>&1 &
MODERATOR_PID=$!
disown $MODERATOR_PID
echo "Moderator UI запущен (PID: $MODERATOR_PID, лог: /tmp/moderator.log)"

sleep 2

echo "=== Запуск Cloudflared туннелей ==="
cd /home/kate/T1-hackathon

nohup cloudflared tunnel --url http://localhost:8000 > /tmp/cloudflared_backend.log 2>&1 &
TUNNEL1_PID=$!
disown $TUNNEL1_PID

nohup cloudflared tunnel --url http://localhost:8501 > /tmp/cloudflared_operator.log 2>&1 &
TUNNEL2_PID=$!
disown $TUNNEL2_PID

nohup cloudflared tunnel --url http://localhost:8502 > /tmp/cloudflared_moderator.log 2>&1 &
TUNNEL3_PID=$!
disown $TUNNEL3_PID

sleep 5

echo ""
echo "=== ✅ ВСЁ ЗАПУЩЕНО ==="
echo ""
echo "Backend API:"
grep -o 'https://[^[:space:]]*\.trycloudflare\.com' /tmp/cloudflared_backend.log | head -1
echo ""
echo "Operator UI:"
grep -o 'https://[^[:space:]]*\.trycloudflare\.com' /tmp/cloudflared_operator.log | head -1
echo ""
echo "Moderator UI:"
grep -o 'https://[^[:space:]]*\.trycloudflare\.com' /tmp/cloudflared_moderator.log | head -1
echo ""
echo "Локальные адреса:"
echo "  Backend: http://localhost:8000"
echo "  Operator: http://localhost:8501"
echo "  Moderator: http://localhost:8502"
echo ""
echo "Логи:"
echo "  Backend: tail -f /tmp/backend.log"
echo "  Operator: tail -f /tmp/operator.log"
echo "  Moderator: tail -f /tmp/moderator.log"
echo ""
