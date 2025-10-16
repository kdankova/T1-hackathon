#!/bin/bash

echo "Запуск интерфейса модератора..."
streamlit run moderator_app.py --server.port 8502 --server.address 0.0.0.0

