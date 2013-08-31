{% if function_params.database != '*' -%}
$MYSQL $MY_PRINT_DEFAULT_FOR_SECTION_{{mysql.my_print_defaults_for_section}} -e "select * from mysql.db where db = '{{function_params.database}}' ;" > /dev/null 2>&1
if [ $? -ne 0 ]; then
    echo "error accessing databases list" >&2
    exit 1
fi
DATABASE_OPTION="{{function_params.database}}"
DATABASE_SEGMENT_FILENAME="{{function_params.database}}"
{% else %}
DATABASE_OPTION="--all-databases"
DATABASE_SEGMENT_FILENAME="ALL_DATABASES"
{% endif %}
