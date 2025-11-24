#!/bin/bash

set -e
echo "CSB Project 1 - Setup Script"
echo "============================"
echo ""

if ! command -v python3 &> /dev/null; then
    echo "Python3 is not installed"
    exit 1
fi

echo "Python3 found: $(python3 --version)"
echo ""

echo "Creating virtual environment..."
python3 -m venv venv
source venv/bin/activate

echo "Upgrading pip..."
pip3 install --upgrade pip3

echo "Installing requirements..."
pip3 install -r requirements.txt

echo "Running migrations..."
python3 manage.py migrate

echo "Creating initial data..."
python3 manage.py create_test_data

echo ""
echo "Setup complete!"
echo ""
echo "Create admin user (optional):"
echo "python3 manage.py createsuperuser"
echo ""
echo "Start the application:"
echo ""
echo "In vulnerable mode (default):"
echo "source venv/bin/activate && python3 manage.py runserver"
echo ""
echo "In secure mode:"
echo "source venv/bin/activate && VULNERABLE=False python3 manage.py runserver"
echo ""
echo "Check vulnerability status:"
echo "python3 manage.py vulnerability_status"
echo ""
echo "Visit: http://localhost:8000/"
echo ""
echo "Close the application and the virtual environment:"
echo "CTRL + C to end the process"
echo "deactivate + ENTER to leave the VENV"
