if [[ -z "${IS_LUDENSPROD}" ]]; then
    exit 0
fi

IPADDR=$(grep 'db' /etc/hosts | awk '{print $1}' | head -1)
awk -v ip="$IPADDR " '{print ip $0}' docker/django/ludensprod-dns.txt >> /etc/hosts