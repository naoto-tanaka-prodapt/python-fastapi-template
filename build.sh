#!/bin/bash
pip install -r requirements.txt
alembic upgrade head
cd frontend
npm install
npm run build
