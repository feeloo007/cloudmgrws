INSTALLER_DIR=$HOME/installer
if [ ! -d "$INSTALLER_DIR" ]; then
   echo "$INSTALLER_DIR not found" >&2
   exit 1
fi

