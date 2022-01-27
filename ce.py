# -- coding: utf-8 --
from flask import Flask, jsonify, request
from bs4 import BeautifulSoup
import re
import requests
import time
import datetime

response = {
	'version' : '2.0'
}

application = Flask(__name__)

@application.route('/ce/notice', methods=['POST'])
def ce_notice():
	p = re.compile('\d{4}[-]\d{2}[-]\d{2}')
	html = requests.get("http://cms.pknu.ac.kr/ced/main.do")
	soup = BeautifulSoup(html.content, 'html.parser')
	total = []

	output = {}
	output['listCard'] = {}
	output['listCard']['header'] = {}
	output['listCard']['header']['title'] = '공지사항'
	output['listCard']['header']['imageUrl'] = ''
	output['listCard']['buttons'] = [{}]
	output['listCard']['buttons'][0]['label'] = '더보기'
	output['listCard']['buttons'][0]['action'] = 'webLink'
	output['listCard']['buttons'][0]['webLinkUrl'] = 'http://cms.pknu.ac.kr/ced/view.do?no=11084'
	output['listCard']['items'] = [{}, {}, {}, {}, {}]

	for li in soup.find('ul', {'class':'board_list'}).find('ul').find_all('li'):
		temp = []
		a = li.find('a')
		temp.append("http://cms.pknu.ac.kr" + a['href'])
		temp.append(a.text.strip())
		span = li.find('span', {'class':'date'})
		if span:
			s = p.search(span.text.strip())
			if s:
				temp.append(s.group())
			else:
				temp.append('')
		total.append(temp)

	for i in range(0, 5):
		output['listCard']['items'][i]['title'] = total[i][1]
		output['listCard']['items'][i]['description'] = total[i][2]
		output['listCard']['items'][i]['link'] = {}
		output['listCard']['items'][i]['link']['web'] = total[i][0]
	
	response['template'] = {}
	response['template']['outputs'] = [output]
	response['template']['quickReplies'] = [{}, {}]
	response['template']['quickReplies'][0]['label'] = '새로고침'
	response['template']['quickReplies'][0]['action'] = 'block'
	response['template']['quickReplies'][0]['blockId'] = '5db416cc8192ac000115fc51'
	response['template']['quickReplies'][1]['label'] = '컴퓨터공학과 메인'
	response['template']['quickReplies'][1]['action'] = 'block'
	response['template']['quickReplies'][1]['blockId'] = '5db53f698192ac000115fec6'

	return jsonify(response)

@application.route('/lib/center', methods=['POST'])
def center_seat():
	url = "https://libweb.pknu.ac.kr/wp-admin/admin-ajax.php"
	data = {
		'action' : 'pknu_get_table_info'
	}
	ajax = requests.post(url=url, data=data).json()

	output = {}
	output['listCard'] = {}
	output['listCard']['header'] = {}
	output['listCard']['header']['title'] = '중앙도서관'
	output['listCard']['header']['imageUrl'] = 'https://libweb.pknu.ac.kr/wp-content/themes/pknu-2016/assets/images/main/main-back-image-02.jpg'
	output['listCard']['buttons'] = [{}]
	output['listCard']['buttons'][0]['label'] = '더보기'
	output['listCard']['buttons'][0]['action'] = 'webLink'
	output['listCard']['buttons'][0]['webLinkUrl'] = 'https://libweb.pknu.ac.kr/service/facilities/seat/'
	output['listCard']['items'] = [{}, {}, {}, {}, {}]
	j = 0

	for i in range(0, 7):
		if i==3 or i==4:continue
		output['listCard']['items'][j]['title'] = ajax['lib'][i][0]
		output['listCard']['items'][j]['description'] = '잔여 좌석 수 : ' + ajax['lib'][i][3]
		output['listCard']['items'][j]['link'] = {}
		output['listCard']['items'][j]['link']['web'] = ajax['lib'][i][4]
		j = j + 1

	response['template'] = {}
	response['template']['outputs'] = [output]
	response['template']['quickReplies'] = [{}, {}]
	response['template']['quickReplies'][0]['label'] = '새로고침'
	response['template']['quickReplies'][0]['action'] = 'block'
	response['template']['quickReplies'][0]['blockId'] = '5db417c092690d0001a4eed6'
	response['template']['quickReplies'][1]['label'] = '학습도서관 좌석 정보'
	response['template']['quickReplies'][1]['action'] = 'block'
	response['template']['quickReplies'][1]['blockId'] = '5db4343492690d0001a4ef07'

	return jsonify(response)

@application.route('/lib/learning', methods=['POST'])
def learning_seat():
	url = "https://libweb.pknu.ac.kr/wp-admin/admin-ajax.php"
	data = {
		'action' : 'pknu_get_table_info'
	}
	ajax = requests.post(url=url, data=data).json()

	output = {}
	output['listCard'] = {}
	output['listCard']['header'] = {}
	output['listCard']['header']['title'] = '학습도서관'
	output['listCard']['header']['imageUrl'] = 'https://libweb.pknu.ac.kr/wp-content/themes/pknu-2016/assets/images/main/main-back-image-02.jpg'
	output['listCard']['buttons'] = [{}]
	output['listCard']['buttons'][0]['label'] = '더보기'
	output['listCard']['buttons'][0]['action'] = 'webLink'
	output['listCard']['buttons'][0]['webLinkUrl'] = 'https://libweb.pknu.ac.kr/service/facilities/seat/'
	output['listCard']['items'] = [{}, {}, {}, {}, {}]
	j = 0

	for i in range(11, 16):
		output['listCard']['items'][j]['title'] = ajax['lib'][i][0]
		output['listCard']['items'][j]['description'] = '잔여 좌석 수 : ' + ajax['lib'][i][3]
		output['listCard']['items'][j]['link'] = {}
		output['listCard']['items'][j]['link']['web'] = ajax['lib'][i][4]
		j = j + 1

	response['template'] = {}
	response['template']['outputs'] = [output]
	response['template']['quickReplies'] = [{}, {}]
	response['template']['quickReplies'][0]['label'] = '새로고침'
	response['template']['quickReplies'][0]['action'] = 'block'
	response['template']['quickReplies'][0]['blockId'] = '5db4343492690d0001a4ef07'
	response['template']['quickReplies'][1]['label'] = '중앙도서관 좌석 정보'
	response['template']['quickReplies'][1]['action'] = 'block'
	response['template']['quickReplies'][1]['blockId'] = '5db417c092690d0001a4eed6'

	return jsonify(response)

@application.route('/dorm/sejong/notice', methods=['POST'])
def SejongDorm_notice():
	url = 'https://dormitory.pknu.ac.kr/main/main.php'
	html = requests.get(url, verify=False)
	soup = BeautifulSoup(html.content, 'html.parser')

	output = {}
	output['listCard'] = {}
	output['listCard']['header'] = {}
	output['listCard']['header']['title'] = '공지사항'
	output['listCard']['header']['imageUrl'] = ''
	output['listCard']['buttons'] = [{}]
	output['listCard']['buttons'][0]['label'] = '더보기'
	output['listCard']['buttons'][0]['action'] = 'webLink'
	output['listCard']['buttons'][0]['webLinkUrl'] = 'https://dormitory.pknu.ac.kr/03_notice/notice02.php'
	output['listCard']['items'] = [{}, {}, {}, {}, {}]
	i = 0

	for li in soup.find('ul', {'class':'list'}).find_all('li'):
		if i==5:break
		a = li.find('a')
		output['listCard']['items'][i]['title'] = a.text.strip()
		output['listCard']['items'][i]['link'] = {}
		output['listCard']['items'][i]['link']['web'] = 'https://dormitory.pknu.ac.kr' + a['href']
		i = i + 1

	response['template'] = {}
	response['template']['outputs'] = [output]
	response['template']['quickReplies'] = [{}, {}, {}]
	response['template']['quickReplies'][0]['label'] = '새로고침'
	response['template']['quickReplies'][0]['action'] = 'block'
	response['template']['quickReplies'][0]['blockId'] = '5db418a38192ac000115fc5c'
	response['template']['quickReplies'][1]['label'] = '식단표'
	response['template']['quickReplies'][1]['action'] = 'block'
	response['template']['quickReplies'][1]['blockId'] = '5db418928192ac000115fc5a'
	response['template']['quickReplies'][2]['label'] = '다른 날짜 식단'
	response['template']['quickReplies'][2]['action'] = 'block'
	response['template']['quickReplies'][2]['blockId'] = '5db4777bffa7480001db6135'

	return jsonify(response)

@application.route('/dorm/sejong/menu', methods=['POST'])
def SejongDorm_menu():
	url = "https://dormitory.pknu.ac.kr/03_notice/req_getSchedule.php"
	data = {'bid': 'foodE'}

	detail_params = request.get_json()['action']['detailParams']
	if detail_params:
		date = detail_params['date']['origin']
		converted_date = datetime.datetime.strptime(date, "%Y-%m-%d")
		week = converted_date.weekday() + 1
		data['vt'] = converted_date.replace(microsecond=0).timestamp()
	else:
		week = datetime.date.today().weekday() + 1
		data['vt'] = time.time()
	if week==7:week=0

	html = requests.post(url=url, data=data, verify=False)
	soup = BeautifulSoup(html.content, 'html.parser')

	menu = {}
	menu['아침'] = []
	menu['점심'] = []
	menu['저녁'] = []
	menu['date'] = []

	for th in soup.find('thead').find_all('th'):
		th = th.text.strip()
		if th=='요일':continue
		menu['date'].append(th)

	for tr in soup.find('tbody').find_all('tr'):
		for td in tr.find_all('td'):
			td = td.text.strip()
			if td=='아침' or td=='점심' or td=='저녁':
				index = td
				continue
			menu[index].append(td.replace('\n', '').replace(' ', '\n'))
	
	response['data'] = {
		'date' : menu['date'][week],
		'breakfast' : menu['아침'][week],
		'lunch' : menu['점심'][week],
		'dinner' : menu['저녁'][week]
	}

	return jsonify(response)

@application.route('/dorm/happy/notice', methods=['POST'])
def HappyDorm_notice():
	url = "https://busan.happydorm.or.kr/busan/bbs/indexBbsNoticeList.kmc"
	data = {
		'bbs_locgbn': 'DD',
		'notice_bbs_id': 'notice',
		'notice_endNum': 5
	}
	kmc = requests.post(url=url, data=data).json()

	output = {}
	output['listCard'] = {}
	output['listCard']['header'] = {}
	output['listCard']['header']['title'] = '공지사항'
	output['listCard']['header']['imageUrl'] = ''
	output['listCard']['buttons'] = [{}]
	output['listCard']['buttons'][0]['label'] = '더보기'
	output['listCard']['buttons'][0]['action'] = 'webLink'
	output['listCard']['buttons'][0]['webLinkUrl'] = 'https://busan.happydorm.or.kr/busan/60/6010.kmc'
	output['listCard']['items'] = [{}, {}, {}, {}, {}]
	i = 0

	for notice in kmc['root'][0]['notice']:
		output['listCard']['items'][i]['title'] = notice['subject']
		output['listCard']['items'][i]['description'] = notice['regdate']
		i = i + 1

	response['template'] = {}
	response['template']['outputs'] = [output]
	response['template']['quickReplies'] = [{}, {}, {}]
	response['template']['quickReplies'][0]['label'] = '새로고침'
	response['template']['quickReplies'][0]['action'] = 'block'
	response['template']['quickReplies'][0]['blockId'] = '5db418d0b617ea00012ba055'
	response['template']['quickReplies'][1]['label'] = '오늘 식단'
	response['template']['quickReplies'][1]['action'] = 'block'
	response['template']['quickReplies'][1]['blockId'] = '5db418c5b617ea00012ba053'
	response['template']['quickReplies'][2]['label'] = '다른 날짜 식단'
	response['template']['quickReplies'][2]['action'] = 'block'
	response['template']['quickReplies'][2]['blockId'] = '5db47784ffa7480001db6137'

	return jsonify(response)

@application.route('/dorm/happy/menu', methods=['POST'])
def HappyDorm_menu():
	data = {}
	data['locgbn'] = 'DD'
	url = "https://busan.happydorm.or.kr/busan/food/getWeeklyMenu.kmc"
	detail_params = request.get_json()['action']['detailParams']

	if detail_params:
		date = detail_params['date']['origin']
		converted_date = date.split('-')
		y = int(converted_date[0])
		m = int(converted_date[1])
		d = int(converted_date[2])
		week = datetime.date(y, m, d).weekday() + 1
		data['sch_date'] = date
	else:
		date = datetime.date.today()
		week = date.weekday() + 1 # (1:월, 2:화, 3:수, 4:목, 5:금, 6:토, 7:일)
		data['sch_date'] = None
		date = date.strftime('%Y-%m-%d')

	kmc = requests.post(url=url, data=data).json()
	try:
		WEEKLYMENU = kmc['root'][0]['WEEKLYMENU'][0]
		breakfast = WEEKLYMENU['fo_menu_mor' + str(week)].replace(', ', '\n')
		lunch = WEEKLYMENU['fo_menu_lun' + str(week)].replace(', ', '\n')
		dinner = WEEKLYMENU['fo_menu_eve' + str(week)].replace(', ', '\n')
	except IndexError:
		breakfast = ''
		lunch = ''
		dinner = ''

	response['data'] = {
		'date' : date,
		'breakfast' : breakfast,
		'lunch' : lunch,
		'dinner' : dinner
	}

	return jsonify(response)

if __name__ == '__main__':
	application.run(host = '0.0.0.0', threaded = True)