from config import *

class InstagramUser:
	def __init__(self, username):
		self.username = username
		self.user_id = self.get_user_id()

	def get_user_id(self):
		result = requests.get(f'https://www.instagram.com/{self.username}/?__a=1', headers=headers).json()
		self.is_private = result['graphql']['user']['is_private'] if 'graphql' in result else None
		return int(result['graphql']['user']['id']) if 'graphql' in result else None

	def get_stories(self):
		if not self.user_id:
			return
		ws_url = f'https://i.instagram.com/api/v1/feed/reels_media/?reel_ids={self.user_id}'
		# example =  'https://i.instagram.com/api/v1/feed/reels_media/?reel_ids=111111111'
		headers['user-agent'] = headers_agent_list[random.randrange(0,4)]
		links = []
		try:
			responsive = requests.get(ws_url, headers=headers_stories).json()
			if responsive['reels_media']:
				for story in responsive['reels_media'][0]['items']:
					links.append(self.get_story_link(story))
				print(links)
				return links
		except Exception as e:
			return
		
	def get_story_link(self, responsive: dict):
		return responsive['video_versions'][0]['url'] if 'video_versions' in responsive else responsive['image_versions2']['candidates'][0]['url']

class InstagramPost:
	def __init__(self, link):
		self.link = link

	def get_media(self): #Получить список ссылок фото и видео из поста
		BASE_URL = 'https://www.instagram.com/graphql/query/?'
		# example = 'query_hash=2c4c2e343a8f64c625ba02b2aa12c7f8&variables=%7B%22shortcode%22%3A%22B1MOgEcisGw%22%2C%22child_comment_count%22%3A3%2C%22fetch_comment_count%22%3A40%2C%22parent_comment_count%22%3A24%2C%22has_threaded_comments%22%3Atrue%7D'
		headers['referer'] = self.link
		headers['user-agent'] = headers_agent_list[random.randrange(0,4)]
		link = urllib.parse.urlparse(self.link)[2].split('/')
		shortcode_id = self.get_shortcode()
		if not shortcode_id:
			return
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
					links.append(self.get_media_link(media['node']))
			else:
				links.append(self.get_media_link(responsive['data']['shortcode_media']))
			print(links)
			return links
		except Exception as e:
			return

	def get_shortcode(self):
		link = urllib.parse.urlparse(self.link)[2].split('/')
		if not ('p' in link or 'tv' in link):
			return None
		return link[link.index('p') + 1] if 'p' in link else link[link.index('tv') + 1]

	def get_media_link(self, responsive: dict): #Получить ссылку на фото/видео из JSON
		return responsive['video_url'] if responsive['is_video'] else responsive['display_url']

# class InstagramStory:
# 	def __init__(self, link):
# 		self.link = link