MY_PRINT_DEFAULT_FOR_EXTRA_SECTION=$( my_print_defaults -c $MY_EXTRA_CNF_FILEPATH -- {{function_params.section}} )
if [ -z "$MY_PRINT_DEFAULT_FOR_EXTRA_SECTION" ]; then
   echo "{{function_params.section}} section doesn't exist in $MY_EXTRA_CNF_FILEPATH" >&2
   exit 1
fi
