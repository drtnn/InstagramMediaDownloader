from config import *

class InstagramUser:
	def __init__(self, username):
		self.username = username
		self.is_private = None
		self.profile_pic_url = None
		self.user_id = None
		self.followers = None
		self.followings = None
		self.full_name = None
		self.biography = None
		self.posts_count = None
		self.posts = None
		# self.highlights = None
		self.get_user()

	def get_user(self): #Получить ID пользователя
		result = requests.get(f'https://www.instagram.com/{self.username}/?__a=1', headers=headers)
		try:		
			if not 'graphql' in result.json():
				return
			user = result.json()['graphql']['user']
		except:
			return
		self.biography = user['biography'] if user['biography'] else None
		self.profile_pic_url = user['profile_pic_url_hd'] if user['profile_pic_url_hd'] else None
		self.full_name = user['full_name'] if user['full_name'] else None
		self.posts_count = user['edge_owner_to_timeline_media']['count'] if user['edge_owner_to_timeline_media']['count'] else None
		self.followers = user['edge_followed_by']['count'] if user['edge_followed_by']['count'] else None
		self.followings = user['edge_follow']['count'] if user['edge_follow']['count'] else None
		self.user_id = int(user['id']) if user['id'] else None
		self.is_private = user['is_private'] if user['is_private'] else None

	def get_stories(self): #Получить ссылки на истории пользователя
		if not self.user_id:
			return
		ws_url = f'https://i.instagram.com/api/v1/feed/reels_media/?reel_ids={self.user_id}'
		headers['user-agent'] = headers_agent_list[random.randrange(0,4)]
		links = []
		try:
			responsive = requests.get(ws_url, headers=headers_stories).json()
			if responsive['reels_media']:
				for story in responsive['reels_media'][0]['items']:
					links.append(self.get_story_link(story))
				return links
		except Exception as e:
			return
		
	def get_story_link(self, responsive: dict): #Получить ссылку на фото/видео
		return responsive['video_versions'][0]['url'] if 'video_versions' in responsive else responsive['image_versions2']['candidates'][0]['url']

class InstagramPost:
	def __init__(self, link):
		self.link = link
		self.user = None
		self.caption = None
		self.media = self.get_media()

	def get_media(self): #Получить ссылки фото и видео из поста
		BASE_URL = 'https://www.instagram.com/graphql/query/?'
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
			self.user = InstagramUser(responsive['data']['shortcode_media']['owner']['username'])
			if 'edge_sidecar_to_children' in responsive['data']['shortcode_media']:
				for media in responsive['data']['shortcode_media']['edge_sidecar_to_children']['edges']:
					links.append(self.get_media_link(media['node']))
			else:
				links.append(self.get_media_link(responsive['data']['shortcode_media']))
			if responsive['data']['shortcode_media']['edge_media_to_caption']['edges']:
				self.caption = responsive['data']['shortcode_media']['edge_media_to_caption']['edges'][0]['node']['text']
			return links
		except Exception as e:
			return

	def get_shortcode(self): #Получить ID поста
		link = urllib.parse.urlparse(self.link)[2].split('/')
		if not ('p' in link or 'tv' in link):
			return None
		return link[link.index('p') + 1] if 'p' in link else link[link.index('tv') + 1]

	def get_media_link(self, responsive: dict): #Получить ссылку на фото/видео из JSON
		return responsive['video_url'] if responsive['is_video'] else responsive['display_url']

class InstagramStory:
	def __init__(self, link):
		self.link = link
		self.user = InstagramUser(self.get_username_from_link())
		self.swipe_link = None
		self.story_media = self.get_story()

	def get_story(self): #Получить ссылку на историю
		if not self.user.user_id or not self.link:
			return
		ws_url = f'https://i.instagram.com/api/v1/feed/reels_media/?reel_ids={self.user.user_id}'
		headers['user-agent'] = headers_agent_list[random.randrange(0,4)]
		try:
			responsive = requests.get(ws_url, headers=headers_stories).json()
			if responsive['reels_media']:
				for story in responsive['reels_media'][0]['items']:
					if story['pk'] == self.get_shortcode():
						if 'story_cta' in story:
							try:
								self.swipe_link = story['story_cta'][0]['links'][0]['webUri']
							except:
								pass
						return self.get_story_link(story)
				return None
		except Exception as e:
			return
		
	def get_story_link(self, responsive: dict): #Получить ссылку на фото/видео
		return responsive['video_versions'][0]['url'] if 'video_versions' in responsive else responsive['image_versions2']['candidates'][0]['url']

	def get_shortcode(self): #Получить ID истории
		link = urllib.parse.urlparse(self.link)[2].split('/')
		return link[link.index('stories') + 2] if 'stories' in link else None

	def get_username_from_link(self): #Получить имя пользователя
		link = urllib.parse.urlparse(self.link)[2].split('/')
		return link[link.index('stories') + 1] if 'stories' in link else None

