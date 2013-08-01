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
