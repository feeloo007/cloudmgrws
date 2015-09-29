$PSQL --dbname={{function_params.database}} --tuples-only --command "SELECT table_schema || '.' || table_name FROM information_schema.tables WHERE table_type = 'BASE TABLE' AND table_schema NOT IN ('pg_catalog', 'information_schema');" | sed "s/^[ ]*//" | sed "/^$/d"
if [ $? -ne 0 ]; then
    echo "error accessing tables list in {{function_params.database}}" >&2
    exit 1
fi
