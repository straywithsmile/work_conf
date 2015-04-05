# -*- coding: gbk -*-

from gevent.pywsgi import WSGIServer
import urlparse
import time
#import simplejson as json
import json

mpUserName = {
	"gzyejiang" : "叶江",
	"叶江"	    : "叶江",
	"libing"    : "厉兵",
	"厉兵"      : "厉兵",
	"lizhan"    : "李占",
	"李占"      : "李占",
	"normalhy"  : "贺彦",
	"贺彦"      : "贺彦",
	"cairuiyu"  : "蔡瑞瑜",
	"蔡瑞瑜"    : "蔡瑞瑜",
	"light"     : "僵尸",
	"僵尸"      : "僵尸",
	"panweijing" : "潘玮璟",
	"潘玮璟"    : "潘玮璟",
	"richard"   : "曹敏",
	"曹敏"      : "曹敏",
	"xhz"       : "许华珍",
	"许华珍"    : "许华珍",
	"zhangxing" : "张星",
	"张星"      : "张星",
	"gzxiangjianbo" : "向建波",
	"向建波"    : "向建波",
	"gzchenqiu" : "陈秋",
	"陈秋"      : "陈秋",
	"merlinlqy" : "林祺颖",
	"林祺颖"    : "林祺颖",

	"limengying" : "苏打",
	"苏打"      : "苏打",
	"chenjx"    : "水手",
	"水手"      : "水手",
	"huwenlin"  : "妹妹",
	"妹妹"      : "妹妹",
	"mengxing"  : "脑残",
	"zhouchengxiang" : "神奇",
	"神奇"      : "神奇",
	"cenjoy"    : "旺仔",
	"旺仔"      : "旺仔",
	"gzchenxiaoran" : "陈潇然",
	"zhangjian" : "张剑",
	"zrj"       : "丸子",
	"zhulei"    : "朱蕾",
	"jiangjun"  : "点点",
	"fzp217"    : "扶志鹏",
	"gzhuangzibin" : "黄子斌",
	"zhangxing" : "张星",
	"张星" : "张星",
	"祝美祺" : "祝美祺",
}

mpUserType = {
	"叶江"	    : "经典版",
	"厉兵"      : "免费版",
	"李占"      : "免费版",
	"贺彦"      : "经典版",
	"蔡瑞瑜"    : "经典版",
	"僵尸"      : "经典版",
	"潘玮璟"    : "免费版",
	"曹敏"      : "经典版",
	"许华珍"    : "经典版",
	"张星"      : "经典版",
	"向建波"    : "免费版",
	"陈秋"      : "免费版",
	"林祺颖"    : "经典版",

	"苏打"      : "经典版",
	"水手"      : "经典版",
	"妹妹"      : "经典版",
	"脑残"      : "免费版",
	"神奇"      : "经典版",
	"旺仔"      : "经典版",
	"张剑"      : "经典版",
	"丸子"      : "免费版",
	"朱蕾" 	    : "经典版",

	"xy2"	    : "免费版",
	"tx2"	    : "经典版",
	"qa_auto"   : "经典版",
	"点点"      : "经典版",
	"扶志鹏"    : "经典版",
	"黄子斌"    : "免费版",
	"张星"	    : "大航海",
	"祝美祺"    : "大航海",
}

mpShortName = {
	"蔡瑞瑜"    : "cry",
	"潘玮璟"    : "pwj",
	"许华珍"    : "xhz",
	"向建波"    : "xjb",
	"林祺颖"    : "lqy",
	"qa_auto"   : "qa",
	"陈潇然"    : "cxr",
	"扶志鹏"    : "fzp",
	"黄子斌"    : "hzb",
}

mpProductID2Name = {
	"xy2"  : "经典版",
	"xy2d" : "免费版",
	"dhh" : "大航海",
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
		return "经典版"

	username = server_info["username"]

	if not username in mpUserType:
		return "经典版"

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
		if get_server_type(info) == "大航海":
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
	if server_type == "经典版":
		mpAllFeeServer[server_key] = server_info
	elif server_type == "免费版":
		mpAllFreeServer[server_key] = server_info
	elif server_type == "大航海":
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
			"name" : u"内服",
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
