#!/usr/bin/env bash

engine_dir=$PWD/$1
logic_dir=$PWD/$2
port=$3
compile=$4
configname=${engine_dir}config.$port
#shell_port=`expr $3 + 10`
envdir=$PWD/tx2env/

if [ ! -d $logic_dir ]
then
	echo "no Logic dir : $logic_dir"
	exit 1
fi

if [ ! -d $engine_dir ]
then
	echo "no Engine dir: $engine_dir"
	exit 2
fi

if [ ! -f ${engine_dir}txos ]
then
	echo "no Engine engine: ${engine_dir}txos"
	exit 2
fi

if [ -z $port ]
then
	echo "no port"
	exit 3
fi

mkdir -p "${logic_dir}log/{sys,npc,user,god,oslog}"
mkdir -p "${logic_dir}oslog"
mkdir -p "${logic_dir}log"
mkdir -p "${engine_dir}log"

if [ -f ${engine_dir}osd ]
then
	CKSUM=`md5 ${engine_dir}osd | awk '{print $4}'`
	STDSUM=`md5 ${envdir}osd | awk '{print $4}'`

	echo "$CKSUM $STDSUM"
	if [ "$CKSUM" != "$STDSUM" ]
	then
		echo "OSD md5 check error, Overwrite it"
		#cp ${envdir}osd ${engine_dir}osd
	fi
else
	cp ${envdir}osd ${engine_dir}
fi

#if [ ! -f ${engine_dir}osd ]
#then
#	cp ${envdir}osd ${engine_dir}
#fi

if [ ! -f ${engine_dir}osd ]
then
	echo "NO osd, start engine failed"
	exit 4
fi

if [ -f ${engine_dir}tx2.data ]
then
	rm ${engine_dir}tx2.data
fi

if [ ! -x ${logic_dir}db ]
then
	ln -sv /tmp/tx2db ${logic_dir}db
fi

mkdir -p ${logic_dir}dat/
cp ${envdir}host.conf ${logic_dir}dat/

logic_branch=${logic_dir##*logic/}
logic_branch_head=${logic_branch:0:20}
if [ $logic_branch_head = "across_target_server" ]
then
	START_FLAG="-DACROSS_TARGET_SERVER=1"
fi

#echo "use ${engine_dir} compile ${logic_dir} ${START_FLAG}"
#exit 0
TX_HOSTNAME=`hostname`
TX_HOSTIP=`grep $TX_HOSTNAME /etc/hosts|cut -d " " -f 1|head -1`
echo host ip = $TX_HOSTIP

echo "" > $configname
echo "name : 大话西游500" >> $configname
echo "port : $port" >> $configname
echo "" >> $configname
echo "dns ip : localhost" >> $configname
echo "dns port : 8882" >> $configname
echo "" >> $configname
echo "pdc ip : localhost" >> $configname
echo "pdc name : dbTXTxe" >> $configname
echo "pdc user : txe248" >> $configname
echo "log : ${port}_log" >> $configname
echo "" >> $configname
echo "chat server : ${TX_HOSTIP}" >> $configname
echo "chat port : 6667" >> $configname
echo "" >> $configname
echo "txe : ${logic_dir}" >> $configname
echo "tx : ${logic_dir}" >> $configname
echo "block : ${logic_dir}block.dat" >> $configname
echo "" >> $configname
echo "swap : 0" >> $configname
echo "clean up : 180" >> $configname
echo "reset : 900" >> $configname
echo "" >> $configname
echo "cost : 150000000" >> $configname
echo "max_online : 300" >> $configname
echo "" >> $configname

cd ${engine_dir}

if [ ! -z ${compile} ]
then
	#./txos $configname -n -b -DACROSS_TARGET_SERVER=1
	#echo "use ${engine_dir} compile ${logic_dir} -DACROSS_TARGET_SERVER=1"
	./txos $configname -n -b ${START_FLAG}
	echo "use ${engine_dir} compile ${logic_dir} ${START_FLAG}"
	tail ${logic_dir}log/sys/error.dat
	exit 0
fi

#nohup ./txos $configname -DMY_LOGIC=${logic_dir} -DINTERNAL_500=1 -DD1=1 -DD2=2 -DD3=3 -DD4=4 -DD5=5 -DD6=6 -DD7=7 -DD8=8 -DD9=9 -DD10=10 -DD11=\"11\" -DD12="12" -DD13="hello" -DD14="boy" -DD15="joy" -DD16="nono" -DD17=9 -DD18=i -DD19=\"no no 19\" -DD20=j -DD21=\"no no end\" -n -f > ${logic_dir}log/debug.log 2>&1 &
#valgrind --tool=memcheck --leak-check=yes nohup ./txos $configname -n -f ${START_FLAG} -D__RSHELL__ -l"${logic_dir}${port}_oslog/" &
#./txos $configname -n -f ${START_FLAG} -D__RSHELL__ -l"${logic_dir}${port}_oslog/"
#./txos $configname -n -f ${START_FLAG}
#echo "use ${engine_dir} start ${logic_dir} ${START_FLAG}"
#gdb ./txos $configname -n -f
#nohup ./txos $configname -n -f > ${logic_dir}log/debug.log 2>&1 &
#valgrind --leak-check=full --error-limit=no ./txos.bak $configname -n -f > ${logic_dir}log/mem_debug.log
#valgrind --tool=memcheck --leak-check=full ./txos $configname -n -f
#nohup ./txos $configname -DMY_LOGIC=${logic_dir} -DINTERNAL_500=1 -DD1=1 -n -f > ${logic_dir}log/debug.log 2>&1 &
#cp /tmp/tx2db/89/215746989.dat_bak /tmp/tx2db/89/215746989.dat

export HOSTNUM=500

export DBHOST=localhost
export DBDATABASE=TXFEE
export DBUSER=root
#export DBPASSWD=DBtx2

export TBNAME_ACCOUNT=Account
export TBNAME_FEECOUNT=Feecount
export TBNAME_FEE=Fee
export TBNAME_HFEE=HFee
export TBNAME_USERID=Userid
export TBNAME_BALANCE=Balance

TRY=1

while [ $TRY -gt 0 ]
do
	nohup ./osd -s ./ > ${logic_dir}log/osd.err 2>&1 &
	TRY=`expr $TRY - 1`
done

#rm $configname
#tail -f ${logic_dir}log/debug.log
echo "use ${engine_dir} start ${logic_dir} ${START_FLAG}"
#valgrind --tool=memcheck --leak-check=yes --error-limit=no ./txos.bak $configname -n -f ${START_FLAG} -D__RSHELL__ -l"${logic_dir}${port}_oslog/"
#nohup ./txos $configname -n -f ${START_FLAG} -D__RSHELL__ -l"${logic_dir}${port}_oslog/" 2>&1 > "${logic_dir}${port}_oslog/debug.log" &
nohup ./txos $configname -n -f ${START_FLAG} -D__RSHELL__ -D__SELF_TEST__ 2>&1 > "${logic_dir}log/debug.log" &
#./txos $configname -n -f ${START_FLAG} -D__RSHELL__ -D__SELF_TEST__
#./txos $configname -n -f ${START_FLAG} -D__RSHELL__ -l"${logic_dir}${port}_oslog/" 
#./txos $configname -n -f ${START_FLAG} -D__RSHELL__ -l"${logic_dir}${port}_oslog/" 2>&1 > "${logic_dir}${port}_oslog/debug.log"
#./txos $configname -n -f ${START_FLAG} -D__RSHELL__ -l"${logic_dir}${port}_oslog/" &
