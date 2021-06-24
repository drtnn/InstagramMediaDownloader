import headers
import random
import requests
import urllib


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

	def get_user(self):  # Получить ID пользователя
		result = requests.get(
			f'https://www.instagram.com/{self.username}/?__a=1', headers=headers.headers)
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

	def get_stories(self):  # Получить ссылки на истории пользователя
		if not self.user_id:
			return
		ws_url = f'https://i.instagram.com/api/v1/feed/reels_media/?reel_ids={self.user_id}'
		headers.headers['user-agent'] = headers.headers_agent_list[random.randrange(
			0, 4)]
		stories = []
		try:
			responsive = requests.get(
				ws_url, headers=headers.headers_stories).json()
			if responsive['reels_media']:
				for story_responsive in responsive['reels_media'][0]['items']:
					story = InstagramStory(user=self, story_media=self.__get_story_link(
						story_responsive), preview=story_responsive['image_versions2']['candidates'][0]['url'])
					if 'story_cta' in story_responsive:
						try:
							story.swipe_link = story_responsive['story_cta'][0]['links'][0]['webUri']
						except:
							pass
					stories.append(story)
				return stories
		except:
			return

	def __get_story_link(self, responsive: dict):  # Получить ссылку на фото/видео
		return responsive['video_versions'][0]['url'] if 'video_versions' in responsive else responsive['image_versions2']['candidates'][0]['url']


class InstagramPost:
	def __init__(self, link):
		self.link = link
		self.user = None
		self.caption = None
		self.preview = None
		self.media = self.get_media()

	def get_media(self):  # Получить ссылки фото и видео из поста
		BASE_URL = 'https://www.instagram.com/graphql/query/?'
		headers.headers['referer'] = self.link
		headers.headers['user-agent'] = headers.headers_agent_list[random.randrange(
			0, 4)]
		shortcode_id = self.__get_shortcode()
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
			responsive = requests.get(ws_url, headers=headers.headers).json()
			self.user = InstagramUser(
				responsive['data']['shortcode_media']['owner']['username'])
			self.preview = []
			if 'edge_sidecar_to_children' in responsive['data']['shortcode_media']:
				for media in responsive['data']['shortcode_media']['edge_sidecar_to_children']['edges']:
					self.preview.append(media['node']['display_url'])
					links.append(self.__get_media_link(media['node']))
			else:
				self.preview.append(
					responsive['data']['shortcode_media']['display_url'])
				links.append(self.__get_media_link(
					responsive['data']['shortcode_media']))
			if responsive['data']['shortcode_media']['edge_media_to_caption']['edges']:
				self.caption = responsive['data']['shortcode_media']['edge_media_to_caption']['edges'][0]['node']['text']
			return links
		except:
			return

	def __get_shortcode(self):  # Получить ID поста
		link = urllib.parse.urlparse(self.link)[2].split('/')
		if 'p' in link:
			return link[link.index('p') + 1]
		elif 'tv' in link:
			return link[link.index('tv') + 1]
		elif 'reel' in link:
			return link[link.index('reel') + 1]
		else:
			return

	# Получить ссылку на фото/видео из JSON
	def __get_media_link(self, responsive: dict):
		return responsive['video_url'] if responsive['is_video'] else responsive['display_url']


class InstagramStory:
	def __init__(self, link=None, user=None, swipe_link=None, story_media=None, preview=None):
		if link:
			self.link = link
			self.user = InstagramUser(self.__get_username_from_link())
			self.swipe_link = None
			self.preview = None
			self.story_media = self.get_story()
		else:
			self.link = link
			self.user = user
			self.swipe_link = swipe_link
			self.story_media = story_media
			self.preview = preview

	def get_story(self):  # Получить ссылку на историю
		if not self.user.user_id or not self.link:
			return
		ws_url = f'https://i.instagram.com/api/v1/feed/reels_media/?reel_ids={self.user.user_id}'
		headers.headers_stories['user-agent'] = headers.headers_agent_list[random.randrange(
			0, 4)]
		try:
			responsive = requests.get(
				ws_url, headers=headers.headers_stories).json()
			if responsive['reels_media']:
				for story in responsive['reels_media'][0]['items']:
					if story['pk'] == self.__get_shortcode():
						if 'story_cta' in story:
							try:
								self.swipe_link = story['story_cta'][0]['links'][0]['webUri']
							except:
								pass
						self.preview = story['image_versions2']['candidates'][0]['url']
						return self.__get_story_link(story)
				return None
		except:
			return

	def __get_story_link(self, responsive: dict):  # Получить ссылку на фото/видео
		return responsive['video_versions'][0]['url'] if 'video_versions' in responsive else responsive['image_versions2']['candidates'][0]['url']

	def __get_shortcode(self):  # Получить ID истории
		link = urllib.parse.urlparse(self.link)[2].split('/')
		return link[link.index('stories') + 2] if 'stories' in link else None

	def __get_username_from_link(self):  # Получить имя пользователя
		link = urllib.parse.urlparse(self.link)[2].split('/')
		return link[link.index('stories') + 1] if 'stories' in link else None

	def __str__(self):
		return f'link – {self.link}, user – {self.user}, swipe_link – {self.swipe_link}, story_media – {self.story_media}'

class InstagramHighlight:
	def __init__(self, link):
		self.link = link
		self.user = None
		self.highlight_id = self.__parse_highlight_id(self.link) if link and 'instagram.com/stories/highlights/' in link else self.__get_highlight_id()
		self.story_media_id = urllib.parse.urlparse(self.link).query.split('&')[0].replace('story_media_id=', '') if '?story_media_id=' in self.link else None
		self.highlight_media = self.get_highlight_media()

	def get_highlight_media(self): #Получить ссылку на историю
		if self.highlight_id:
			ws_url = f'https://i.instagram.com/api/v1/feed/reels_media/?reel_ids=highlight%3A{self.highlight_id}'
			headers.headers_stories['user-agent'] = headers.headers_agent_list[random.randrange(0,4)]
			try:
				responsive = requests.get(ws_url, headers=headers.headers_stories).json()
				if 'reels_media' in responsive and responsive['reels_media']:
					self.user = InstagramUser(
						responsive['reels_media'][0]['user']['username'])
					highlights = []
					for story_responsive in responsive['reels_media'][0]['items']:
						story = InstagramStory(user=self, story_media=self.__get_highlight_link(
							story_responsive), preview=story_responsive['image_versions2']['candidates'][0]['url'])
						if 'story_cta' in story_responsive:
							try:
								story.swipe_link = story_responsive['story_cta'][0]['links'][0]['webUri']
							except:
								pass
						if self.story_media_id and story_responsive['pk'] == self.story_media_id:
							return [story]
						elif not self.story_media_id:
							highlights.append(story)
					return highlights
			except:
				return

	def __get_highlight_link(self, responsive: dict):  # Получить ссылку на фото/видео
		return responsive['video_versions'][0]['url'] if 'video_versions' in responsive else responsive['image_versions2']['candidates'][0]['url']

	def __parse_highlight_id(self, link):
		link = urllib.parse.urlparse(link)[2].split('/')
		return link[link.index('highlights') + 1] if 'highlights' in link else None

	def __get_highlight_id(self):
		headers.headers_stories['user-agent'] = headers.headers_agent_list[random.randrange(0,4)]
		try:
			r = requests.get(url=self.link, headers=headers.headers_stories)
			for responsive in r.history:
				if responsive.next and responsive.is_redirect:
					return self.__parse_highlight_id(responsive.next.url)
		except:
			return