$MYSQLDUMP $MY_PRINT_DEFAULT_FOR_SECTION_{{mysql.my_print_defaults_for_section}} --opt --skip-extended-insert --hex-blob $DATABASE_OPTION $TABLE_OPTION > $DUMP_DIR/FROM_Z00-${DATABASE_SEGMENT_FILENAME}-${TABLE_SEGMENT_FILENAME}.sql
if [ $? -ne 0 ]; then
    echo "error executing $MYSQLDUMP for database(s) : {{function_params.database}}, table(s) : {{function_params.table}}" >&2
    exit 1
fi
