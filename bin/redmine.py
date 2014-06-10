#!/usr/bin/env python
# -*- coding: gbk -*-
import sys
import os
import xlrd

type_stat = {}
time_stat = {}

def print_stat_item_info(type_stat, time_stat, item_type):
	print item_type, time_stat[item_type]
	for desc in type_stat[item_type]:
		print desc

def print_left_stat_info(type_stat, time_stat):
	for item_type, desc_list in type_stat.items():
		print item_type, time_stat[item_type]
		for desc in desc_list:
			print desc
		print ""

if __name__ == "__main__":
	if len(sys.argv) == 2:
		filename = sys.argv[1]
	else:
		filename = "timelog.csv"
	time_long_file = open(filename, 'r')
	for line in time_long_file:
		data = line.split(",")
		idx = data[4]
		item_type = data[5]
		item_name = data[6]
		time_len = data[7]
		if not item_type in type_stat:
			type_stat[item_type] = []
			time_stat[item_type] = 0.0
		type_stat[item_type].append("%s %s" % (idx, item_name))
		time_stat[item_type] += float(time_len)
		if len(type_stat[item_type]) >= 30:
			print_stat_item_info(type_stat, time_stat, item_type)
			type_stat[item_type] = []
			time_stat[item_type] = 0.0
			print ""
	
	if len(type_stat) > 0:
		print_left_stat_info(type_stat, time_stat)
