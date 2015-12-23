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
	"1" : ["192.168.228.78",  "�ڷ�1", "nf1", "32200", "internal", "richard"],
	"2" : ["192.168.228.75",  "�ڷ�2", "nf2", "32200", "internal", "richard"],
	"3" : ["192.168.229.100", "ģ��1", "mn1", "32200", "internal", "richardcao"],
	"4" : ["192.168.229.101", "ģ��2", "mn2", "32200", "internal", "richardcao"],
	"5" : ["192.168.229.102", "����1", "xr",  "32200", "internal", "richardcao"],
	"6" : ["123.58.170.180",  "ͬ��",  "tb",  "32200", "internal", "richardcao"],
	"7" : ["192.168.228.78",  "�ڷ�21.193", "nf3", "32201", "internal", "richardcao"],
	"8" : ["123.58.169.192",  "mongo", "mongo", "32200", "mongo", "richardcao"],
}
#��http���ӣ��õ�gdsc����
def open_http(product, serverlist_url):
	global server_list
	print '��ʼȡ��gsdc�б���ƷΪ', product

	if product == "mhxy" or product == "dh2":
		try:
			f = urllib2.urlopen(serverlist_url, None, timeout=4)
			print '������ɣ���ʼ��ȡ�б�...'
			server_list = f.readlines()
			tmp_file = open("/tmp/serverlist_cache", "w")
			tmp_file.writelines(server_list)
			tmp_file.close()
		except:
			print '����ʧ�ܣ����Դ��ļ�/tmp/serverlist_cache��ȡ�б�...'
			f = open("/tmp/serverlist_cache", "r")
			server_list = f.readlines()

			f.close()
			if len(server_list) == 0:
				print "û��ȡ��gdsc ���ݣ���ر�Ȼ������"
				return
	elif product == "dh3":
		import urllib
		urllib.urlretrieve("http://mcs.net" + "ease.com/interface/getsynctaginfo/?pid=3", "server_tag.py")
		print '�õ��б���ϣ���ʼ������ʽ...'
	else :
		print "������б�!"
		sys.exit(1)
	
def parse_server_list(product):
	global server_list
	global server_set
	if product == "mhxy" or product == "dh2":
		for cLine in server_list:
			#ÿһ������ 526 60.5.184.87 52688 ������ dm
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
				#��ͼ�Ӻ���ת����Ϊ��2�ֵ�ƴ����д,��Ҫʹ��һ���ⲿƴ���ֵ�
				import ch2py
				py = ch2py.ch2pr(cName)
				py_set = py.split(" ")
				if len(py_set) < 2:
					print "�õ���������д���ִ���,hostnum %d name %s ip %s" %(hostnum, cName, ip)
					continue
				short_name = py_set[0][0] + py_set[1][0]
				server_set[str(hostnum)] = [ip, cName, short_name,svn_tag]
	
	else:
		print "������б�!"
		sys.exit(1)
	print "=============================="
	print "����server %d ��" % len(server_set)
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
				#��ʱӦ���Ѿ�������server set
				#ver:Line[0], group_id:Line[1], x:Line[2], y:Line[3], port:Line[6], server_name:Line[4]
				#hostnum = int(Line[6])/10 hostnum������ôȡ����Ϊ�Ϸ��Ժ�hostnum��һ�������ֹ����λ�ͬ
				#����Ӧ�ø���server nameȥ��һ��
				for k, v in server_set.items():
					if v[1] != Line[4]:
						continue
					server_set[k] += [ group_info[ Line[1] ], Line[2], Line[3], Line[0] ]
				
	elif product == "mhxy":
		#���ֲ��ҷ�ʽ���ܴ�������,��Ҫ�÷��������ֲ���
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
		return format % (100, "�ڲ�����", "192.168.228.78")

	if hostnum in server_set:
		return format % (server_set[hostnum][1], hostnum, server_set[hostnum][0])

	return format % (100, "�ڲ�����", "192.168.228.78")

	
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
	print """q : �˳�
	hostnum : ����hostnum,securecrt��¼
	login hostnum : �޸�xy2.ini�е�default_ip������hostnumĬ��Ϊ500��IPΪ10.172Ϊ�ڷ�����Ϸ·����snet.ini�����ã�����:
		game_paths = D:\\xy2\\
	list : ��securecrt_path������Ŀ¼��Config\\Sessions\\���\\ Ŀ¼�У�����Ŀǰ�������б������з�����������,�б��ַ����:
		serverlist_url = http://dhrsync.x.xxx.com:8660/galaxy/port/get_server/get_server.all
		ע�⣬��һ����������ɾ���������Ŀ¼�µ������ļ�
	"""
	
	print "xx : ƴ��ǰ׺���о�����ƴ��ǰ׺��ͬ�ķ�����"

def output_newest():
	all_hostnums = server_set.keys()
	all_int_hostnums = []
	for hostnum in all_hostnums:
		if hostnum in ["1300", "1301", "1302", "1303", "1304"]:
			continue
	all_int_hostnums.append(int(hostnum))
	all_int_hostnums.sort()
	print "������̨����������:"
	for i in range(len(all_int_hostnums) - 5, len(all_int_hostnums)):
		hostnum = str(all_int_hostnums[i])
		server_info = server_set[hostnum]
		print hostnum, server_info[0], server_info[1], server_info[3], server_info[4]
	
	print "�ڷ�����:"
	internal_hostnums = internal_server.keys()
	internal_hostnums.sort()
	for i in internal_hostnums:
		server_info = internal_server[i]
		print i, server_info[0], server_info[1], server_info[3], server_info[4]

exe_command = ""
def process(user_input):
	global server_set
	global exe_command
	#��ȡ�����ļ�
	username = "richardcao"
	port = "32200"
	product = "dh2"
	serverlist_url = "http://dhrsync.x.net" + "ease.com:8660/galaxy/port/get_server_list"
	game_paths = ""
	
	#�õ��б�
	open_http(product, serverlist_url)
	
	#�����б�
	parse_server_list(product)

	server_set.update(internal_server)

	#�����������
	parse_group_info(product)

	#CMD_LINE = '"%s" /N %s /L "%s" /P %s  /AUTH "%s" ' % (securecrt_path, username, port, auth)
	#����ѭ��
	if len(user_input) == 0:
		usage()
	elif user_input == 'n':
		output_newest()
	#������Ϸ�ͻ��������defaut_ip����
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
			print "��������������"
			return
		print server_set[hostnum][0], server_set[hostnum][1], server_set[hostnum][2]
	elif is_number(user_input):
		#Ҫ��ʼ�����Ǹ�������
		if not user_input in server_set:
			print "û�����hostnumŶ"
			return
		if user_input in internal_server:
			username = internal_server[user_input][5]
			port = internal_server[user_input][3]
		#ip = server_set[user_input][0]
		#server_name = user_input + "@" + server_set[user_input][1] +"@" + ip
		print "���Ե�¼", user_input, ":", server_set[user_input][0], server_set[user_input][1], server_set[user_input][3], server_set[user_input][4]
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
				if product == "dh3" and len(v) >= 8: #��3����Ҫ����ʾһ��svn�汾�ţ����ݸ�ʽҲ������ͬ
					output_content = True
					print k, ":", v[0], " ", v[1], " ", v[2], " ", v[4], ",", v[6], "��,", v[6],"��", " ", v[3], " ver:", v[7]
				elif product == "dh2":
					output_content = True
					print k, ":", v[0], " ", v[1], " ", v[3], " ", v[4]
				else:
					output_content = True
					print k, ":", v[0], " ", v[1], " ", v[2]
		if not output_content:
			print "û���ҵ���ط�����"
	else:
		print "�������"

if __name__ == "__main__":
	if len(sys.argv) < 3:
		usage()
		sys.exit(1)
	exe_command = sys.argv[1]
	user_input = " ".join(sys.argv[2:])
	#user_input = sys.argv[1] + sys.argv[2]
	process(user_input)
