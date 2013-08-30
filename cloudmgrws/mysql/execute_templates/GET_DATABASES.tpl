$MYSQL $MY_PRINT_DEFAULT_FOR_SECTION_{{mysql.my_print_defaults_for_section}} -B -L -N -e "show databases;"
if [ $? -ne 0 ]; then
    echo "error accessing databases list" >&2
    exit 1
fi
