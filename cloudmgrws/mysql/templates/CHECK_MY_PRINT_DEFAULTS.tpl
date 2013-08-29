if [ -z $( which my_print_defaults ) ]; then
    echo "my_print_defaults not found" >&2
    exit 1
fi
if [ -z "$MY_CNF" ]; then
    echo "\$MY_CNF not defined" 2>&1
    exit 1
fi
