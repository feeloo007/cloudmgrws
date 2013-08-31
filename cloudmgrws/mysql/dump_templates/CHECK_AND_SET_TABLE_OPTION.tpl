{% if function_params.database != '*' -%}
    {% if function_params.table != '*' -%}
    $MYSQL $MY_PRINT_DEFAULT_FOR_SECTION_{{mysql.my_print_defaults_for_section}} {{function_params.database}} -e "show create table {{function_params.table}};" > /dev/null 2>&1
    if [ $? -ne 0 ]; then
        echo "error accessing databases list" >&2
        exit 1
    fi
    TABLE_OPTION="{{function_params.table}}"
    TABLE_SEGMENT_FILENAME="{{function_params.table}}"
    {% else -%}
    TABLE_OPTION=""
    TABLE_SEGMENT_FILENAME="ALL_TABLES"
    {% endif -%}
{% else -%}
    TABLE_OPTION=""
    TABLE_SEGMENT_FILENAME="ALL_TABLES"
{% endif -%}
