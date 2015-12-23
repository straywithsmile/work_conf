#!/usr/bin/env python
# -*- coding: gbk -*-
import urllib2
import subprocess
import ConfigParser
import sys
import os

server_list = []

server_set = {}

group_info = {}

internal_server = {
	"1" : ["192.168.228.78",  "内服1", "nf1", "32200", "internal", "richard"],
	"2" : ["192.168.228.75",  "内服2", "nf2", "32200", "internal", "richard"],
	"3" : ["192.168.229.100", "模拟1", "mn1", "32200", "internal", "richardcao"],
	"4" : ["192.168.229.101", "模拟2", "mn2", "32200", "internal", "richardcao"],
	"5" : ["192.168.229.102", "新人1", "xr",  "32200", "internal", "richardcao"],
	"6" : ["123.58.170.180",  "同步",  "tb",  "32200", "internal", "richardcao"],
	"7" : ["192.168.228.78",  "内服21.193", "nf3", "32201", "internal", "richardcao"],
	"8" : ["123.58.169.192",  "mongo", "mongo", "32200", "mongo", "richardcao"],
}
#打开http链接，得到gdsc数据
def open_http(product, serverlist_url):
	global server_list
	print '开始取得gsdc列表，产品为', product

	if product == "mhxy" or product == "dh2":
		try:
			f = urllib2.urlopen(serverlist_url, None, timeout=4)
			print '连接完成，开始获取列表...'
			server_list = f.readlines()
			tmp_file = open("/tmp/serverlist_cache", "w")
			tmp_file.writelines(server_list)
			tmp_file.close()
		except:
			print '连接失败，尝试从文件/tmp/serverlist_cache获取列表...'
			f = open("/tmp/serverlist_cache", "r")
			server_list = f.readlines()

			f.close()
			if len(server_list) == 0:
				print "没有取到gdsc 数据，请关闭然后重试"
				return
	elif product == "dh3":
		import urllib
		urllib.urlretrieve("http://mcs.net" + "ease.com/interface/getsynctaginfo/?pid=3", "server_tag.py")
		print '得到列表完毕，开始分析格式...'
	else :
		print "错误的列表!"
		sys.exit(1)
	
def parse_server_list(product):
	global server_list
	global server_set
	if product == "mhxy" or product == "dh2":
		for cLine in server_list:
			#每一行数据 526 60.5.184.87 52688 大名府 dm
			line_set = cLine.split(" ")
			hostnum = line_set[0]
			ip = line_set[1]
			portnum = line_set[2]
			#cName = line_set[3].decode('gbk').encode('utf-8')
			cName = line_set[3]
			short_name = line_set[4][0:2]
			branch = line_set[5].strip()
			server_set[hostnum] = [ip, cName, short_name, portnum, branch]
	elif product == "dh3":
		from server_tag import synctaginfo
		for svn_tag , server_info_list in synctaginfo.items():
			for server_info in server_info_list:
				hostnum = server_info["serverid"]   #int
				#cName = server_info["name"].decode('gbk').encode('utf-8')
				cName = server_info["name"]
				ip = server_info["ip"]
				#试图从汉字转换成为首2字的拼音缩写,需要使用一个外部拼音字典
				import ch2py
				py = ch2py.ch2pr(cName)
				py_set = py.split(" ")
				if len(py_set) < 2:
					print "得到服务器缩写名字错误,hostnum %d name %s ip %s" %(hostnum, cName, ip)
					continue
				short_name = py_set[0][0] + py_set[1][0]
				server_set[str(hostnum)] = [ip, cName, short_name,svn_tag]
	
	else:
		print "错误的列表!"
		sys.exit(1)
	print "=============================="
	print "共有server %d 组" % len(server_set)
	print "=============================="
	#print server_set

def parse_group_info(product):
	global group_info
	global server_set
	if product == "dh3":
		for x in urllib2.urlopen("http://update.xy3.163.com/xy3server10.txt").readlines():
			Line = x.split()
			if x.startswith("ServerGroup"):
				group_info[ Line[1] ] = Line[4]
			elif len(Line) == 16:
				#此时应该已经分析完server set
				#ver:Line[0], group_id:Line[1], x:Line[2], y:Line[3], port:Line[6], server_name:Line[4]
				#hostnum = int(Line[6])/10 hostnum不能这么取，因为合服以后hostnum不一定是这种规则，梦幻同
				#还是应该根据server name去找一下
				for k, v in server_set.items():
					if v[1] != Line[4]:
						continue
					server_set[k] += [ group_info[ Line[1] ], Line[2], Line[3], Line[0] ]
				
	elif product == "mhxy":
		#这种查找方式可能存在问题,需要用服务器名字查找
		for x in urllib2.urlopen("http://update.xyq.163.com/v1_xyqserver.txt?").readlines():
			Line = x.split()
			if x.startswith("-") and len(Line) == 4:
				Line = x[1:].split()
				group_info[ Line[0] ] = Line[3]
				#print x, Line
			elif len(Line) == 15:
				#group_id:Line[0] x:Line[2], y:Line[1],port:Line[5],server_name:Line[3]
				#hostnum = int(Line[5])/100
				for k, v in server_set.items():
					if v[1] != Line[3]:
						continue
					server_set[k] += [ group_info[ Line[0] ], Line[1], Line[2]  ]
	else:
		pass

def is_number(number):
		#if number is a number,return 1,other than return 0.a
		number_type = type(number)
		if  number_type == int:
				return 1
		elif number_type == str:
				if number.isdigit() == True:
						return 1
				else:
						return 0
		else:
				return 0

def gen_server_config(hostnum):
	format = "#%s %s\ndefault_ip=%s\ninternal_server_list=192.168.228.78:8090/get_server_list\n"

	if hostnum == 500:
		return format % (100, "内部测试", "192.168.228.78")

	if hostnum in server_set:
		return format % (server_set[hostnum][1], hostnum, server_set[hostnum][0])

	return format % (100, "内部测试", "192.168.228.78")

	
def update_config_file(game_paths, hostnum):
	result = ""
	append_content = gen_server_config(hostnum)
	for path in game_paths:
		try:
			tmp_file = open(path + "xy2.ini", "r")
		except:
			print path + "xy2.ini", "can't open"
			continue
	
		for line in tmp_file:
			result += line
			if line.find("[net]") >= 0:
				break
		tmp_file.close()
	result += append_content
	tmp_file = open(path + "xy2.ini", "w")
	tmp_file.write(result)
	tmp_file.close()
	print path, "\n", append_content, "READY"

def usage():
	print """q : 退出
	hostnum : 输入hostnum,securecrt登录
	login hostnum : 修改xy2.ini中的default_ip，不填hostnum默认为500，IP为10.172为内服，游戏路径在snet.ini中配置，如下:
		game_paths = D:\\xy2\\
	list : 在securecrt_path的配置目录下Config\\Sessions\\外服\\ 目录中，生成目前服务器列表中所有服务器的配置,列表地址如下:
		serverlist_url = http://dhrsync.x.xxx.com:8660/galaxy/port/get_server/get_server.all
		注意，这一操作，将会删除所有外服目录下的所有文件
	"""
	
	print "xx : 拼音前缀，列举所有拼音前缀相同的服务器"

def output_newest():
	all_hostnums = server_set.keys()
	all_int_hostnums = []
	for hostnum in all_hostnums:
		if hostnum in ["1300", "1301", "1302", "1303", "1304"]:
			continue
	all_int_hostnums.append(int(hostnum))
	all_int_hostnums.sort()
	print "最新五台服务器如下:"
	for i in range(len(all_int_hostnums) - 5, len(all_int_hostnums)):
		hostnum = str(all_int_hostnums[i])
		server_info = server_set[hostnum]
		print hostnum, server_info[0], server_info[1], server_info[3], server_info[4]
	
	print "内服如下:"
	internal_hostnums = internal_server.keys()
	internal_hostnums.sort()
	for i in internal_hostnums:
		server_info = internal_server[i]
		print i, server_info[0], server_info[1], server_info[3], server_info[4]

exe_command = ""
def process(user_input):
	global server_set
	global exe_command
	#读取配置文件
	username = "richardcao"
	port = "32200"
	product = "dh2"
	serverlist_url = "http://dhrsync.x.net" + "ease.com:8660/galaxy/port/get_server_list"
	game_paths = ""
	
	#得到列表
	open_http(product, serverlist_url)
	
	#处理列表
	parse_server_list(product)

	server_set.update(internal_server)

	#处理服务器组
	parse_group_info(product)

	#CMD_LINE = '"%s" /N %s /L "%s" /P %s  /AUTH "%s" ' % (securecrt_path, username, port, auth)
	#输入循环
	if len(user_input) == 0:
		usage()
	elif user_input == 'n':
		output_newest()
	#更新游戏客户端里面的defaut_ip配置
	elif user_input.find("login") >= 0:
		try:
			hostnum = user_input.split(" ")[1]
		except:
			hostnum = 500
		update_config_file(game_paths, hostnum)
	elif user_input.find("info") >= 0:
		try:
			hostnum = user_input.split(" ")[1]
		except:
			print "请输入服务器编号"
			return
		print server_set[hostnum][0], server_set[hostnum][1], server_set[hostnum][2]
	elif is_number(user_input):
		#要开始连接那个服务器
		if not user_input in server_set:
			print "没有这个hostnum哦"
			return
		if user_input in internal_server:
			username = internal_server[user_input][5]
			port = internal_server[user_input][3]
		#ip = server_set[user_input][0]
		#server_name = user_input + "@" + server_set[user_input][1] +"@" + ip
		print "尝试登录", user_input, ":", server_set[user_input][0], server_set[user_input][1], server_set[user_input][3], server_set[user_input][4]
		#print newtab, type(newtab)
		if exe_command == "ssh":
			#cmd = "ssh -F /opt/local/etc/ssh/ssh_config %s@%s -p %s" % (username, server_set[user_input][0], port)
			cmd = "ssh %s@%s -p %s" % (username, server_set[user_input][0], port)
		elif exe_command == "sftp":
			#sftp -F /opt/local/etc/ssh/ssh_config -P 32200 192.168.228.78
			cmd = "sftp -P %s %s@%s" % (port, username, server_set[user_input][0])
		else:
			print "can't execute %s, enable is ssh|sftp" % exe_command
			return

		print "EXE : %s" % cmd
		cmd = 'echo "%s" > /tmp/richard_macsnet.cmd' % cmd
		os.system(cmd)
	elif len(user_input) == 2:
		output_content = False
		for k, v in server_set.items():
			if v[2] == user_input:
				#hostnum, ip, name, short_name
				if product == "dh3" and len(v) >= 8: #大话3会需要多显示一个svn版本号，数据格式也有所不同
					output_content = True
					print k, ":", v[0], " ", v[1], " ", v[2], " ", v[4], ",", v[6], "行,", v[6],"列", " ", v[3], " ver:", v[7]
				elif product == "dh2":
					output_content = True
					print k, ":", v[0], " ", v[1], " ", v[3], " ", v[4]
				else:
					output_content = True
					print k, ":", v[0], " ", v[1], " ", v[2]
		if not output_content:
			print "没有找到相关服务器"
	else:
		print "输入错误"

if __name__ == "__main__":
	if len(sys.argv) < 3:
		usage()
		sys.exit(1)
	exe_command = sys.argv[1]
	user_input = " ".join(sys.argv[2:])
	#user_input = sys.argv[1] + sys.argv[2]
	process(user_input)
