error=`journalctl | grep "unregistering driver hv_netvsc"`
if [ "$error" ]
then
   echo "$error"
fi

