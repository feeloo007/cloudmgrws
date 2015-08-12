(
if [ -d $MY_EXTRA_CNF_DIR ]; then
    cd $MY_EXTRA_CNF_DIR
    find . -type f -maxdepth 1 -mindepth 1
fi
)
