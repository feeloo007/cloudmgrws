if [ ! -f $MY_EXTRA_CNF_DIR/{{function_params.my_extra_cnf}} ]; then
    echo "$MY_EXTRA_CNF_DIR/{{function_params.my_extra_cnf}} does'nt exist" >&2
    exit 1
fi
MY_EXTRA_CNF_FILEPATH=$MY_EXTRA_CNF_DIR/{{function_params.my_extra_cnf}}
