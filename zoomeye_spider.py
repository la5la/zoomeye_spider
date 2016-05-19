# coding = utf-8
# author: 40huo

import json
import os

import requests

access_token = ''
ip_list = []


def login():
	"""
    输入用户名密码进行登录
    :return: 访问口令 access_token
    """
	user = input('[-] input username: ')
	passwd = input('[-] input password: ')
	data = {
		'username': user,
		'password': passwd
	}
	data_encoded = json.dumps(data)
	# print(data_encoded)
	try:
		r = requests.post(url='http://api.zoomeye.org/user/login', data=data_encoded)
		# print(r.text)
		r_decoded = json.loads(r.text)
		global access_token
		access_token = r_decoded['access_token']
	except Exception as e:
		print('[-] info: username or password is wrong, please try again')
		exit()


def saveStrToFile(file, str):
	"""
    将字符串写入文件
    :param file:
    :param str:
    :return:
    """
	with open(file, 'w') as output:
		output.write(str)


def saveListToFile(file, list):
	"""
    将列表逐行写入文件
    :param file:
    :param list:
    :return:
    """
	s = '\n'.join(list)
	with open(file, 'w') as output:
		output.write(s)


def apiTest():
	"""
    进行api测试
    :return:
    """
	page = 1
	global access_token
	with open('access_token.txt', 'r') as input:
		access_token = input.read()
	headers = {
		'Authorization': 'JMT' + access_token,
	}
	while (True):
		try:
			r = requests.get(url='http://api.zoomeye.org/host/search?query="dedecms"&facet=app,os&page=' + str(page),
							 headers=headers)
			r_decoded = json.loads(r.text)
			for x in r_decoded['matches']:
				print(x['ip'])
				ip_list.append(x['ip'])
			print('[-] info: count' + str(page * 10))
		except Exception as e:
			if str(e) == 'matches':
				print('[-] info: account was broken, exceeding the max limitation')
				break
			else:
				print('[-] info: ' + str(e))
		else:
			if page == 10:
				break
			page += 1


def main():
	if not os.path.isfile('access_token.txt'):
		print('[-] info: access_token file not exists, please login')
		login()
		saveStrToFile('access_token.txt', access_token)

	apiTest()
	saveListToFile('ip_list.txt', ip_list)


if __name__ == '__main__':
	main()
aasss
