
file_name="vProfiler_`hostname`_`date +%d%m%Y-%H%M%S`.tar.gz"
cd ..
sudo tar -czf $file_name logs
user=`whoami`
sudo chown $user $file_name
printf "\nTarball saved at:\n"
realpath $file_name
printf "\nFile Size:\n"
du -h $file_name
