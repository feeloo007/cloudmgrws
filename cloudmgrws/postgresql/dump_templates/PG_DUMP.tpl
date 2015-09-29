$PG_DUMP $TABLE_OPTION --file=$DUMP_DIR/FROM_Z00-${DATABASE_SEGMENT_FILENAME}-${TABLE_SEGMENT_FILENAME}.sql --dbname=$DATABASE_OPTION
if [ $? -ne 0 ]; then
    echo "error executing $PG_DUMP for database(s) : {{function_params.database}}, table(s) : {{function_params.table}}" >&2
    exit 1
fi
