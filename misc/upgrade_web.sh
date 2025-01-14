#!/bin/bash

#set -x  # command tracing
shopt -s nullglob

PATH=/usr/bin:/bin
export PATH


function catch_error() {
    echo
    echo
    echo "The script exited abnormally, please try to run again..."
    echo
    echo
    exit 1
}
trap catch_error ERR

function catch_sigint() {
    echo
    echo
    echo "The setup script was interrupted, please run the script again to finish..."
    echo
    echo
    exit 1
}
trap catch_sigint SIGINT


DISTRO_NAME=$(lsb_release -s -i)
DISTRO_RELEASE=$(lsb_release -s -r)
CPU_ARCH=$(uname -m)
CPU_BITS=$(getconf LONG_BIT)


echo "#################################################"
echo "### Welcome to the indi-allsky upgrade script ###"
echo "#################################################"
echo
echo "This script should be used for situations requiring minimal"
echo "modifications, like a web-only installation"


if systemctl --user -q is-active indi-allsky >/dev/null 2>&1; then
    echo
    echo
    echo "WARNING: indi-allsky is running.  It is recommended to stop the service before running this script."
    echo
    sleep 5
fi


echo
echo
echo "Distribution: $DISTRO_NAME"
echo "Release: $DISTRO_RELEASE"
echo "Arch: $CPU_ARCH"
echo "Bits: $CPU_BITS"
echo


if [[ "$(id -u)" == "0" ]]; then
    echo "Please do not run $(basename "$0") as root"
    echo "Re-run this script as the user which will execute the indi-allsky software"
    echo
    echo
    exit 1
fi

if [[ -n "$VIRTUAL_ENV" ]]; then
    echo "Please do not run $(basename "$0") with a virtualenv active"
    echo "Run \"deactivate\" to exit your current virtualenv"
    echo
    echo
    exit 1
fi

echo "Setup proceeding in 10 seconds... (control-c to cancel)"
echo
sleep 10


# Run sudo to ask for initial password
sudo true


START_TIME=$(date +%s)



echo "**** Installing packages... ****"
if [[ "$DISTRO_NAME" == "Raspbian" && "$DISTRO_RELEASE" == "11" ]]; then
    PYTHON_BIN=python3

    if [ "$CPU_ARCH" == "armv7l" ]; then
        VIRTUALENV_REQ=requirements/requirements_debian11_32.txt
    elif [ "$CPU_ARCH" == "i686" ]; then
        VIRTUALENV_REQ=requirements/requirements_debian11_32.txt
    elif [[ "$CPU_ARCH" == "aarch64" && "$CPU_BITS" == "32" ]]; then
        VIRTUALENV_REQ=requirements/requirements_debian11_32.txt
    elif [[ "$CPU_ARCH" == "x86_64" && "$CPU_BITS" == "32" ]]; then
        VIRTUALENV_REQ=requirements/requirements_debian11_32.txt
    else
        VIRTUALENV_REQ=requirements/requirements_debian11.txt
    fi

elif [[ "$DISTRO_NAME" == "Raspbian" && "$DISTRO_RELEASE" == "10" ]]; then
    PYTHON_BIN=python3

    VIRTUALENV_REQ=requirements/requirements_debian10.txt

elif [[ "$DISTRO_NAME" == "Debian" && "$DISTRO_RELEASE" == "11" ]]; then
    PYTHON_BIN=python3

    if [ "$CPU_ARCH" == "armv7l" ]; then
        VIRTUALENV_REQ=requirements/requirements_debian11_32.txt
    elif [ "$CPU_ARCH" == "i686" ]; then
        VIRTUALENV_REQ=requirements/requirements_debian11_32.txt
    elif [[ "$CPU_ARCH" == "aarch64" && "$CPU_BITS" == "32" ]]; then
        VIRTUALENV_REQ=requirements/requirements_debian11_32.txt
    elif [[ "$CPU_ARCH" == "x86_64" && "$CPU_BITS" == "32" ]]; then
        VIRTUALENV_REQ=requirements/requirements_debian11_32.txt
    else
        VIRTUALENV_REQ=requirements/requirements_debian11.txt
    fi

elif [[ "$DISTRO_NAME" == "Debian" && "$DISTRO_RELEASE" == "10" ]]; then
    PYTHON_BIN=python3

    VIRTUALENV_REQ=requirements/requirements_debian10.txt

elif [[ "$DISTRO_NAME" == "Ubuntu" && "$DISTRO_RELEASE" == "22.04" ]]; then
    PYTHON_BIN=python3

    if [ "$CPU_ARCH" == "armv7l" ]; then
        VIRTUALENV_REQ=requirements/requirements_debian11_32.txt
    elif [ "$CPU_ARCH" == "i686" ]; then
        VIRTUALENV_REQ=requirements/requirements_debian11_32.txt
    elif [[ "$CPU_ARCH" == "aarch64" && "$CPU_BITS" == "32" ]]; then
        VIRTUALENV_REQ=requirements/requirements_debian11_32.txt
    elif [[ "$CPU_ARCH" == "x86_64" && "$CPU_BITS" == "32" ]]; then
        VIRTUALENV_REQ=requirements/requirements_debian11_32.txt
    else
        VIRTUALENV_REQ=requirements/requirements_debian11.txt
    fi

elif [[ "$DISTRO_NAME" == "Ubuntu" && "$DISTRO_RELEASE" == "20.04" ]]; then
    PYTHON_BIN=python3.9

    if [ "$CPU_ARCH" == "armv7l" ]; then
        VIRTUALENV_REQ=requirements/requirements_debian11_32.txt
    elif [ "$CPU_ARCH" == "i686" ]; then
        VIRTUALENV_REQ=requirements/requirements_debian11_32.txt
    elif [[ "$CPU_ARCH" == "aarch64" && "$CPU_BITS" == "32" ]]; then
        VIRTUALENV_REQ=requirements/requirements_debian11_32.txt
    elif [[ "$CPU_ARCH" == "x86_64" && "$CPU_BITS" == "32" ]]; then
        VIRTUALENV_REQ=requirements/requirements_debian11_32.txt
    else
        VIRTUALENV_REQ=requirements/requirements_debian11.txt
    fi

elif [[ "$DISTRO_NAME" == "Ubuntu" && "$DISTRO_RELEASE" == "18.04" ]]; then
    PYTHON_BIN=python3.8

    if [ "$CPU_ARCH" == "armv7l" ]; then
        VIRTUALENV_REQ=requirements/requirements_debian11_32.txt
    elif [ "$CPU_ARCH" == "i686" ]; then
        VIRTUALENV_REQ=requirements/requirements_debian11_32.txt
    elif [[ "$CPU_ARCH" == "aarch64" && "$CPU_BITS" == "32" ]]; then
        VIRTUALENV_REQ=requirements/requirements_debian11_32.txt
    elif [[ "$CPU_ARCH" == "x86_64" && "$CPU_BITS" == "32" ]]; then
        VIRTUALENV_REQ=requirements/requirements_debian11_32.txt
    else
        VIRTUALENV_REQ=requirements/requirements_debian11.txt
    fi

else
    echo "Unknown distribution $DISTRO_NAME $DISTRO_RELEASE ($CPU_ARCH)"
    exit 1
fi


# find script directory for service setup
SCRIPT_DIR=$(dirname "$0")
cd "$SCRIPT_DIR/.." || catch_error
ALLSKY_DIRECTORY=$PWD
cd "$OLDPWD" || catch_error


echo "**** Python virtualenv setup ****"
[[ ! -d "${ALLSKY_DIRECTORY}/virtualenv" ]] && mkdir "${ALLSKY_DIRECTORY}/virtualenv"
chmod 775 "${ALLSKY_DIRECTORY}/virtualenv"
if [ ! -d "${ALLSKY_DIRECTORY}/virtualenv/indi-allsky" ]; then
    virtualenv -p "${PYTHON_BIN}" "${ALLSKY_DIRECTORY}/virtualenv/indi-allsky"
fi
# shellcheck source=/dev/null
source "${ALLSKY_DIRECTORY}/virtualenv/indi-allsky/bin/activate"
pip3 install --upgrade pip setuptools wheel
pip3 install -r "${ALLSKY_DIRECTORY}/${VIRTUALENV_REQ}"


flask db revision --autogenerate
flask db upgrade head


# dump config for processing
TMP_CONFIG_DUMP=$(mktemp --suffix=.json)
"${ALLSKY_DIRECTORY}/config.py" dump > "$TMP_CONFIG_DUMP"


# load all changes
"${ALLSKY_DIRECTORY}/config.py" load -c "$TMP_CONFIG_DUMP" --force
[[ -f "$TMP_CONFIG_DUMP" ]] && rm -f "$TMP_CONFIG_DUMP"


END_TIME=$(date +%s)

echo
echo
echo "Completed in $((END_TIME - START_TIME))s"
echo

echo
echo "Enjoy!"

