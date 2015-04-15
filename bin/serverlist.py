# -*- coding: gbk -*-

from gevent.pywsgi import WSGIServer
import urlparse
import time
#import simplejson as json
import json

mpUserName = {
	"gzyejiang" : "Ҷ��",
	"Ҷ��"	    : "Ҷ��",
	"libing"    : "����",
	"����"      : "����",
	"lizhan"    : "��ռ",
	"��ռ"      : "��ռ",
	"normalhy"  : "����",
	"����"      : "����",
	"cairuiyu"  : "�����",
	"�����"    : "�����",
	"light"     : "��ʬ",
	"��ʬ"      : "��ʬ",
	"panweijing" : "����Z",
	"����Z"    : "����Z",
	"richard"   : "����",
	"����"      : "����",
	"xhz"       : "����",
	"����"    : "����",
	"zhangxing" : "����",
	"����"      : "����",
	"gzxiangjianbo" : "�򽨲�",
	"�򽨲�"    : "�򽨲�",
	"gzchenqiu" : "����",
	"����"      : "����",
	"merlinlqy" : "����ӱ",
	"����ӱ"    : "����ӱ",

	"limengying" : "�մ�",
	"�մ�"      : "�մ�",
	"chenjx"    : "ˮ��",
	"ˮ��"      : "ˮ��",
	"huwenlin"  : "����",
	"����"      : "����",
	"mengxing"  : "�Բ�",
	"zhouchengxiang" : "����",
	"����"      : "����",
	"cenjoy"    : "����",
	"����"      : "����",
	"gzchenxiaoran" : "����Ȼ",
	"zhangjian" : "�Ž�",
	"zrj"       : "����",
	"zhulei"    : "����",
	"jiangjun"  : "���",
	"fzp217"    : "��־��",
	"gzhuangzibin" : "���ӱ�",
	"zhangxing" : "����",
	"����" : "����",
	"ף����" : "ף����",
}

mpUserType = {
	"Ҷ��"	    : "�����",
	"����"      : "��Ѱ�",
	"��ռ"      : "��Ѱ�",
	"����"      : "�����",
	"�����"    : "�����",
	"��ʬ"      : "�����",
	"����Z"    : "��Ѱ�",
	"����"      : "�����",
	"����"    : "�����",
	"����"      : "�����",
	"�򽨲�"    : "��Ѱ�",
	"����"      : "��Ѱ�",
	"����ӱ"    : "�����",

	"�մ�"      : "�����",
	"ˮ��"      : "�����",
	"����"      : "�����",
	"�Բ�"      : "��Ѱ�",
	"����"      : "�����",
	"����"      : "�����",
	"�Ž�"      : "�����",
	"����"      : "��Ѱ�",
	"����" 	    : "�����",

	"xy2"	    : "��Ѱ�",
	"tx2"	    : "�����",
	"qa_auto"   : "�����",
	"���"      : "�����",
	"��־��"    : "�����",
	"���ӱ�"    : "��Ѱ�",
	"����"	    : "�󺽺�",
	"ף����"    : "�󺽺�",
}

mpShortName = {
	"�����"    : "cry",
	"����Z"    : "pwj",
	"����"    : "xhz",
	"�򽨲�"    : "xjb",
	"����ӱ"    : "lqy",
	"qa_auto"   : "qa",
	"����Ȼ"    : "cxr",
	"��־��"    : "fzp",
	"���ӱ�"    : "hzb",
}

mpProductID2Name = {
	"xy2"  : "�����",
	"xy2d" : "��Ѱ�",
	"dhh" : "�󺽺�",
	}

def simplify_server_info(server_info):
	new_server_info = { }
	for info, value_list in server_info.items():
		new_server_info[info] = value_list[0]
	return new_server_info

mpAllFeeServer = {}
mpAllFreeServer = {}
mpDahanghaiServer = {}

def get_server_type(server_info):
	#lookup version data
	if "product" in server_info:
		return server_info["product"]

	#find version by username
	if not "username" in server_info:
		return "�����"

	username = server_info["username"]

	if not username in mpUserType:
		return "�����"

	return mpUserType[username]

def get_server_list(mpAllServer):
	now = int(time.time())
	send_data = ""
	for server_key, info in mpAllServer.items():
		diff = now - info["update_time"]
		if 35 < diff:
			continue
		if not "use" in info:
			info["use"] = "unknown"
		if not "desc" in info:
			info["desc"] = "unknown"
		if not "logic_dir" in info:
			info["logic_dir"] = "unknown"

		username = info["username"]
		if get_server_type(info) == "�󺽺�":
			username = username.decode("gbk").encode("utf-8")

		data = [info["ip"], info["port"], username, info["use"], info["desc"], info["logic_dir"], "\n"]
		send_data = send_data + "|".join(data)
	return send_data

def update_server_info(ip, query_string):
	global mpUserName
	server_info = urlparse.parse_qs(query_string)
	now = int(time.time())

	server_info = simplify_server_info(server_info)

	if not "logic_dir" in server_info:
		return ""

	if "time" in server_info:
		server_now = int(server_info["time"])
		time_diff = server_now - now
		if time_diff < -30 or 30 < time_diff:
			server_info["logic_dir"] = server_info["logic_dir"] + ("#rError Time : %d sec" % time_diff)

	if "port" in server_info:
		server_key = ":".join([ip, server_info["port"]])
	else:
		print "error.......", server_info
		server_key = ip

	tmp_data = server_info["logic_dir"].split("/")
	username = tmp_data[2]

	if username in mpUserName:
		server_info["username"] = mpUserName[username]
	else:
		server_info["username"] = username
	
	server_info["update_time"] = int(time.time())
	server_info["ip"] = ip 

	if "product_id" in server_info:
		server_info["product"] = mpProductID2Name[server_info["product_id"]]

	server_type = get_server_type(server_info)
	if server_type == "�����":
		mpAllFeeServer[server_key] = server_info
	elif server_type == "��Ѱ�":
		mpAllFreeServer[server_key] = server_info
	elif server_type == "�󺽺�":
		mpDahanghaiServer[server_key] = server_info
	else:
		mpAllFeeServer[server_key] = server_info

	return "register succ\n%s\n%s" % (server_key, time.ctime(now))

def parse_xy(idx):
	return ((idx / 6) % 5) + 1, (idx % 6) + 1

def get_ngp_serverlist(mpAllServer):
	now = int(time.time())
	all_servers = []
	idx = 0
	developer2server = {}
	for server_key, info in mpAllServer.items():
		diff = now - info["update_time"]
		if 35 < diff:
			continue
		if not "use" in info:
			info["use"] = "unknown"
		if not "desc" in info:
			info["desc"] = "unknown"
		if not "logic_dir" in info:
			info["logic_dir"] = "unknown"
			
		developer = info["username"]
		if not developer in developer2server:
			developer2server[developer] = []

		server_info = {
				"name" : ("%s:%s" % (unicode(developer, 'gbk'), info["port"])),
				"active" : 1,
				"port" : info["port"],
				"ip" : info["ip"],
		}

		if developer in mpShortName:
			server_info["name"] = "%s:%s" % (mpShortName[developer], info["port"])

		server_info["x"], server_info["y"] = parse_xy(idx)
		idx += 1
		developer2server[developer].append(server_info)

	for developer in sorted(developer2server.keys()):
		all_servers.extend(developer2server[developer])

	group_info = {
		202 : {
			"name" : u"�ڷ�",
			"servers" : all_servers,
		}
	}

	return json.dumps(group_info)

def serve_request(environ, start_response):
	status = '200 OK'
	body = ""

	headers = [
		('Content-Type', 'text/plain')
	]

	if environ["PATH_INFO"] == "/get_server_list":
		body = get_server_list(mpAllFeeServer)
	elif environ["PATH_INFO"] == "/get_server_list_free":
		body = get_server_list(mpAllFreeServer)
	elif environ["PATH_INFO"] == "/register_server":
		body = update_server_info(environ["REMOTE_ADDR"], environ["QUERY_STRING"])
	elif environ["PATH_INFO"] == "/get_ngp_server_list":
		body = get_ngp_serverlist(mpAllFeeServer)
	elif environ["PATH_INFO"] == "/get_ngp_server_list_free":
		body = get_ngp_serverlist(mpAllFreeServer)
	elif environ["PATH_INFO"] == "/get_dhh_server_list":
		body = get_server_list(mpDahanghaiServer)

	start_response(status, headers)
	return [body]

if __name__ == "__main__":
	WSGIServer(('192.168.228.78',8090), serve_request).serve_forever()
