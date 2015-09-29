{% if function_params.database != '*' -%}
$PSQL --list --tuples-only | cut -d ' ' -f 1 | grep -w {{function_params.database}} | wc -l
if [ $? -ne 0 ]; then
    echo "error accessing databases list" >&2
    exit 1
fi
DATABASE="{{function_params.database}}"
{% else %}
DATABASE=""
{% endif %}
