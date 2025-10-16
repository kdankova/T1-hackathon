#!/bin/bash

echo "Запуск интерфейса оператора..."
streamlit run operator_app.py --server.port 8501 --server.address 0.0.0.0

