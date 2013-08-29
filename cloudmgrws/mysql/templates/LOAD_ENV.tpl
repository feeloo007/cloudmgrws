# Cleaning env
env -i

if [ -f $HOME/.bash_profile ]; then

    # Sourcing env
    source $HOME/.bash_profile
    if [ $? -ne 0 ]; then
         echo "error sourcing $HOME/.bash_profile" >&2
    fi

else

    echo "$HOME/.bash_profile does'nt exist" >&2
    exit 1

fi
