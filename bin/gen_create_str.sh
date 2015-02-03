#!/usr/bin/env bash
date_str=`date "+%Y_%m_%d"`
svn_head="https://svn-dhxy2.gz.netease.com/products/xy2/develop/server/"

create_env="env|release|simulate"
create_branch="branch|release|test|shiwan|other"

help()
{
	echo "./gen_create_str.sh create_env create_branch logic release [date]"
}

#if [ $# -eq 1 ];then
#	date_str=`date "+%Y_%m_%d"`
#	logic_svn_branch=$1
#	engine_svn_branch=$1
#elif [ $# -eq 2 ];then
#	date_str=`date "+%Y_%m_%d"`
#	logic_svn_branch=$1
#	engine_svn_branch=$2
#elif [ $# -eq 3 ];then
#	logic_svn_branch=$1
#	engine_svn_branch=$2
#	date_str=$3
#elif [ $# -eq 4 ];then
#	logic_svn_branch=$1
#	engine_svn_branch=$2
#	date_str=$3
#	create_env=$4
#elif [ $# -eq 5 ];then
#	logic_svn_branch=$1
#	engine_svn_branch=$2
#	date_str=$3
#	create_env=$4
#	create_branch=$5
#else
#	help
#	exit 2
#fi

if [ $# -eq 4 ];then
	create_env=$1
	create_branch=$2
	logic_svn_branch=$3
	engine_svn_branch=$4
elif [ $# -eq 5 ];then
	create_env=$1
	create_branch=$2
	logic_svn_branch=$3
	engine_svn_branch=$4
	date_str=$5
else
	help
	exit 2
fi

#echo $#

echo $logic_svn_branch
if [ $logic_svn_branch = "release" ];then
	logic_dir=${svn_head}logic/release/rel_${date_str}
elif [ ${logic_svn_branch:0:4} = "test" ];then
	logic_dir=${svn_head}logic/test/${logic_svn_branch}_${date_str}
elif [ $logic_svn_branch = "trunk" ];then
	logic_dir=${svn_head}logic/trunk
else
	logic_dir=${svn_head}logic/branch/${logic_svn_branch}_${date_str}
fi
echo $logic_svn_branch

echo $engine_svn_branch
if [ $engine_svn_branch = "release" ];then
	engine_dir=${svn_head}os/release/rel_${date_str}
elif [ ${engine_svn_branch:0:4} = "test" ];then
	engine_dir=${svn_head}os/test/${engine_svn_branch}_${date_str}
elif [ $engine_svn_branch = "trunk" ];then
	engine_dir=${svn_head}os/trunk
else
	engine_dir=${svn_head}os/branch/${engine_svn_branch}_${date_str}
fi
echo $engine_svn_branch

IAM=`whoami`

svn info $logic_dir
if [ $? -ne 0 ];then
	echo LOGIC_PATH ${logic_dir} does NOT_EXIST
fi
logic_dir="svn${logic_dir:5:100}"

svn info $engine_dir
if [ $? -ne 0 ];then
	echo ENGINE_PATH ${engine_dir} does NOT_EXIST
fi
engine_dir="svn${engine_dir:5:100}"

echo ${logic_state} ${engine_state}

#example: ./create_simulate.sh simulate https://svn-dhxy2.gz.netease.com/products/xy2/develop/server/logic/trunk trunk https://svn-dhxy2.gz.netease.com/products/xy2/develop/server/os/trunk ~tx2/osd/release/release/osd
echo "./create_simulate.sh ${create_env} ${logic_dir} ${create_branch} ${engine_dir} ~tx2/osd/release/release/osd"
exit 0
