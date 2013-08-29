$MYSQL $MY_PRINT_DEFAULT_FOR_SECTION_{{mysql.my_print_defaults_for_section}} --force $DATABASE < $HOME/executables/{{function_params.executable}}
if [ $? -ne 0 ]; then
    echo "error executing $HOME/executables/{{function_params.executable}}" >&2
    exit 1
fi
