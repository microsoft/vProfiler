echo "vProfiler Summary Report"
date
hostnamectl
lscpu | grep "^CPU(s):"
lscpu | grep "^Thread"

echo

echo "lspci:"
sudo lspci

echo

netstat -i

echo "=========="
