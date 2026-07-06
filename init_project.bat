@echo off

# Active the virtual environment
venv\Scripts\activate

# Install backend dependencies
pip install -r requirements.txt

# Install frontend dependencies
cd lms_frontend
npm install