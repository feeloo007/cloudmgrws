$MYSQL $MY_PRINT_DEFAULT_FOR_SECTION_{{mysql.my_print_defaults_for_section}} $MY_PRINT_DEFAULT_FOR_EXTRA_SECTION $DATABASE_OPTION $DATABASE < $EXECUTABLE_DIR/{{function_params.executable}}
if [ $? -ne 0 ]; then
    echo "error executing $EXECUTABLE_DIR/{{function_params.executable}}" >&2
    exit 1
fi
