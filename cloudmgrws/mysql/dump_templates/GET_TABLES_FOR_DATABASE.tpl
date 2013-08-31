$MYSQL $MY_PRINT_DEFAULT_FOR_SECTION_{{mysql.my_print_defaults_for_section}} -B -L -N {{function_params.database}} -e "show tables;"
if [ $? -ne 0 ]; then
    echo "error accessing tables list in {{function_params.database}}" >&2
    exit 1
fi
