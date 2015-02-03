#!/usr/bin/env bash
part=$1
branch=$2

if [ ${branch:0:4} = "rel_" ];then
	branch_name="release/${branch}"
elif [ ${branch:0:4} = "test" ];then
	branch_name="test/${branch}"
elif [ ${branch:0:7} = "shiwan_" ];then
	branch_name="branch/${branch}"
else
	branch_name="branch/${branch}"
fi

svn_path=svn://svn-dhxy2.gz.netease.com/products/xy2/develop/server/${part}/${branch_name}
svn info ${svn_path}
if [ $? -ne 0 ];then
	echo "svn path ${svn_path} does NOT exist"
	exit 1
fi

IAM=`whoami`
svn_tmp_file="svn_tmp_file_${IAM}"
svn log --stop-on-copy $svn_path -q|grep -o -E "r[0-9]+" > ${svn_tmp_file}
end_version=`head -n 1 ${svn_tmp_file}`
start_version=`tail -n 1 ${svn_tmp_file}`
if [ ${end_version} = ${start_version} ];then
	echo "svn path has ONLY one version ${end_version}"
	exit 1
fi
echo "svn merge -r${start_version:1}:${end_version:1} $svn_path --ignore-ancestry"
rm ${svn_tmp_file}
