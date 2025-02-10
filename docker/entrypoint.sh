#!/bin/bash

# Create and populate the database
if [[ ! -s "${DB_URL#sqlite:///}" ]]
then
    python app/database/quieries/db_populate.py
fi

# Run the application
exec "$@"