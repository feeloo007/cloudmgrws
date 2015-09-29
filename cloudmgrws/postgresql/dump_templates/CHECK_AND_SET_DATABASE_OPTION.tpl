{% if function_params.database != '*' -%}
$PSQL --list --tuples-only | cut -d '|' -f 1 | grep -w {{function_params.database}}
if [ $? -ne 0 ]; then
    echo "error accessing databases list" >&2
    exit 1
fi
DATABASE_OPTION="{{function_params.database}}"
DATABASE_SEGMENT_FILENAME="{{function_params.database}}"
{% else %}
PG_DUMP=$PG_DUMP_ALL
DATABASE_OPTION=""
DATABASE_SEGMENT_FILENAME="ALL_DATABASES"
{% endif %}
