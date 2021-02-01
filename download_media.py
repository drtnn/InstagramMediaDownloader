from config import *

headers_agent_list = [
        "Mozilla/5.0 (Windows NT 5.1; rv:41.0) Gecko/20100101"\
        " Firefox/41.0",
        "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_2)"\
        " AppleWebKit/601.3.9 (KHTML, like Gecko) Version/9.0.2"\
        " Safari/601.3.9",
        "Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:15.0)"\
        " Gecko/20100101 Firefox/15.0.1",
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"\
        " (KHTML, like Gecko) Chrome/42.0.2311.135 Safari/537.36"\
        " Edge/12.246",
		"Mozilla/5.0 (Macintosh; Intel Mac OS X 11_1_0) AppleWebKit/537.36"\
		" (KHTML, like Gecko) Chrome/88.0.4324.96 Safari/537.36",
        ]

headers = {
	'authority': 'www.instagram.com',
	'pragma': 'no-cache',
	'cache-control': 'no-cache',
	'sec-ch-ua': '"Chromium";v="88", "Google Chrome";v="88", ";Not A Brand";v="99"',
	'x-ig-www-claim': 'hmac.AR2OIZnV3Xot5AT_boqr-HjjPl9BObBv1RN7LCdlgdQflWvw',
	'sec-ch-ua-mobile': '?0',
	'accept': '*/*',
	'x-requested-with': 'XMLHttpRequest',
	'sec-fetch-site': 'same-origin',
	'sec-fetch-mode': 'cors',
	'sec-fetch-dest': 'empty',
	'accept-language': 'ru-RU,ru;q=0.9,en-US;q=0.8,en;q=0.7',
}

def get_media_json(link: str):
	BASE_URL = 'https://www.instagram.com/graphql/query/?'
	# example = 'query_hash=2c4c2e343a8f64c625ba02b2aa12c7f8&variables=%7B%22shortcode%22%3A%22B1MOgEcisGw%22%2C%22child_comment_count%22%3A3%2C%22fetch_comment_count%22%3A40%2C%22parent_comment_count%22%3A24%2C%22has_threaded_comments%22%3Atrue%7D'
	headers['referer'] = link
	headers['user-agent'] = headers_agent_list[random.randrange(0,4)]
	link = link.split('/')
	shortcode_id = link[-1] if (link[-1] and '?' not in link[-1]) else link[-2]
	variables = f'{{"shortcode":"{shortcode_id}","has_threaded_comments":true}}'
	get_params = {
		'query_hash': '2c4c2e343a8f64c625ba02b2aa12c7f8',
		'variables': variables
	}
	ws_url = BASE_URL + urllib.parse.urlencode(get_params)
	links = []
	try:
		responsive = requests.get(ws_url, headers=headers).json()
		if 'edge_sidecar_to_children' in responsive['data']['shortcode_media']:
			for media in responsive['data']['shortcode_media']['edge_sidecar_to_children']['edges']:
				links.append(get_media_link(media['node']))
		else:
			links.append(get_media_link(responsive['data']['shortcode_media']))
		return links
	except Exception as e:
		return None

def get_media_link(responsive: dict):
	return responsive['video_url'] if responsive['is_video'] else responsive['display_url']
