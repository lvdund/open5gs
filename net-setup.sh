init() {
    sudo ip tuntap add name ogstun mode tun
    sudo ip addr add 10.45.0.1/16 dev ogstun
    sudo ip addr add 2001:db8:cafe::1/48 dev ogstun
    sudo ip link set ogstun up

    sudo sysctl -w net.ipv4.ip_forward=1
    sudo sysctl -w net.ipv6.conf.all.forwarding=1
    sudo iptables -t nat -A POSTROUTING -s 10.45.0.0/16 ! -o ogstun -j MASQUERADE
    sudo ip6tables -t nat -A POSTROUTING -s 2001:db8:cafe::/48 ! -o ogstun -j MASQUERADE
}

remove() {
    sudo ip link del ogstun 2>/dev/null
    sudo sysctl -w net.ipv4.ip_forward=0 2>/dev/null
    sudo sysctl -w net.ipv6.conf.all.forwarding=0 2>/dev/null
    sudo ip -6 route flush table 2>/dev/null
    sudo iptables -t nat -F 2>/dev/null
    sudo iptables -t filter -F 2>/dev/null
    sudo ip6tables -t nat -F 2>/dev/null
    sudo ip6tables -t filter -F 2>/dev/null
}

case "$1" in
    init) init ;;
    remove) remove ;;
    *) echo "Usage: $0 {init|remove}" ;;
esac
