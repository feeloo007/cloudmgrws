MY_PRINT_DEFAULT_FOR_SECTION_{{mysql.my_print_defaults_for_section}}=$( my_print_defaults -c $MY_CNF {{mysql.my_print_defaults_for_section}} )
if [ -z "$MY_PRINT_DEFAULT_FOR_SECTION_{{mysql.my_print_defaults_for_section}}" ]; then
   echo "{{mysql.my_print_defaults_for_section}} section does'nt exist in $MY_CNF" >&2
   exit 1
fi
