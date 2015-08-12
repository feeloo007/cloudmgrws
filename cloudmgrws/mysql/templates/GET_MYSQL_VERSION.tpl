$MYSQL $MY_PRINT_DEFAULT_FOR_SECTION_{{mysql.my_print_defaults_for_section}} -B -L -N -e "SHOW VARIABLES LIKE 'version';" | sed -E -e 's#^.*version\t([^\.]*?)\.([^\.]*?)\..*$#\"\1\.\2"#g'
