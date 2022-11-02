set -e

selfdir=$(dirname `realpath $0`)
rootdir=`realpath $selfdir/..`

export CONAN_HOME=$HOME/.local/conan-editable-test

if test -e $rootdir/.venv; then
    source $rootdir/.venv/bin/activate
else
    python -m venv $rootdir/.venv
    source $rootdir/.venv/bin/activate
    pip install --pre --upgrade conan

    conan config install $rootdir/config
    conan profile detect

    mkdir -p $HOME/.local/conan-editable-test
fi

run_conan() {
    echo conan "$@"
    conan "$@"
}
