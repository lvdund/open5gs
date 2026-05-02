INSTALL_DIR="/home/vd/github/open5gs/install"
LIB_PATH="/home/vd/github/open5gs/install/lib"

export LD_LIBRARY_PATH="$LIB_PATH:$LD_LIBRARY_PATH"

NFS=(
    "bin/open5gs-nrfd"
    "bin/open5gs-amfd"
    "bin/open5gs-smfd"
    "bin/open5gs-upfd"
    "bin/open5gs-ausfd"
    "bin/open5gs-udmd"
    "bin/open5gs-pcfd"
    "bin/open5gs-nssfd"
    "bin/open5gs-bsfd"
    "bin/open5gs-udrd"
)

start() {
    for nf in "${NFS[@]}"; do
        "$INSTALL_DIR/$nf" &
    done
    echo "All Open5GS NFs started in background"
}

stop() {
    pkill -f "open5gs-"
    echo "All Open5GS processes stopped"
}

case "$1" in
    start)
        start
        ;;
    stop)
        stop
        ;;
    restart)
        stop
        sleep 1
        start
        ;;
    *)
        echo "Usage: $0 {start|stop|restart}"
        exit 1
        ;;
esac
