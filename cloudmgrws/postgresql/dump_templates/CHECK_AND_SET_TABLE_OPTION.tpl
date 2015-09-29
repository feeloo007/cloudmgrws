{% if function_params.database != '*' -%}
    {% if function_params.table != '*' -%}
    $PSQL --dbname={{function_params.database}} --tuples-only --quiet --command '\dt {{function_params.table}}' | grep -w table 
    if [ $? -ne 0 ]; then
        echo "error accessing tables list" >&2
        exit 1
    fi
    TABLE_OPTION="--table={{function_params.table}}"
    TABLE_SEGMENT_FILENAME="{{function_params.table}}"
    {% else -%}
    TABLE_OPTION=""
    TABLE_SEGMENT_FILENAME="ALL_TABLES"
    {% endif -%}
{% else -%}
    TABLE_OPTION=""
    TABLE_SEGMENT_FILENAME="ALL_TABLES"
{% endif -%}
