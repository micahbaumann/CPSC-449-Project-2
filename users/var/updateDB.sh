# Use this file to remove the current catalog.db file and populate it with the newest version found in catalog.sql

echo "Updating database file"
rm users.db
sqlite3 users.db -init users.sql
echo "users Database file updated :)"
