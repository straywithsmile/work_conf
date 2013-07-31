#!/usr/bin/env bash

if [ $# -eq 1 ]
then
	if [ $1 = "all" ]
	then
		killall txos
		killall osd
	else
		port=$1
		findresult=`ps | grep "config.${port}" | grep -v "grep"`
		if [ ! $? -eq 0 ]
		then
			echo "No such server"
			exit 1
		fi
		pid=`echo ${findresult} | awk '{print $1}'`
		osdpid=`expr ${pid} + 1`
		echo "kill ${pid} and ${osdpid}"
		kill -1 ${pid}
		#sleep 4
		#kill ${osdpid}
	fi
else
	echo "error param"
fi
