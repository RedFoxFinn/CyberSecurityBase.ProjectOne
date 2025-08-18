#!/bin/bash

# Usage: ./primer.sh <superuser_email>
if [ "$#" -ne 1 ]; then
	echo "Usage: $0 <superuser_email>"
	exit 1
fi

SUPERUSER_EMAIL="$1"
PROJECT_DIR="csbp1"
MANAGE_PY="$PROJECT_DIR/manage.py"

echo "Applying migrations..."
python3 "$MANAGE_PY" migrate

echo "Creating superuser..."
python3 "$MANAGE_PY" shell <<EOF
from django.contrib.auth import get_user_model
User = get_user_model()
if not User.objects.filter(username='superadmin').exists():
	User.objects.create_superuser('superadmin', '$SUPERUSER_EMAIL', 'adminsuper')
EOF

echo "Initialization complete."
