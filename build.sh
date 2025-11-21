#!/bin/bash
set -0

# backend
pip install -r requirements.txt
alembic upgrade head

# frontend
cd frontend
npm install
npm run build
