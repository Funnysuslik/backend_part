# Wait until PostgreSQL is ready
until psql "$DATABASE_URL" -c '\q'; do
  >&2 echo "Postgres is unavailable - sleeping"
  sleep 1
done

>&2 echo "Postgres is up - continuing"
exec "$@"