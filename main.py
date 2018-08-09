import praw
import config
import urllib.request as urllib2
from bs4 import BeautifulSoup
from datetime import datetime


def get_soup(url):
    http_response = urllib2.urlopen(url)
    return BeautifulSoup(http_response, 'html.parser')


def main(bot):
    announcement_list_soup = get_soup('https://www.rayark.com/g/sdorica/en/announcement/')
    announcement_list = announcement_list_soup.find_all('div', class_='list')
    latest_announcement_url = str(announcement_list[0].contents[1]).split('href')[1].split('"')[1]
    with latest_announcement_url.split('/')[len(latest_announcement_url.split('/'))-2] as latest_announcement_date:
        if latest_announcement_date == datetime.now().strftime('%Y-%M-%D'):
            announcement_detail_soup = get_soup('https://www.rayark.com' + latest_announcement_url)
            announcement_detail_title = announcement_detail_soup.find('span', class_='mainTitle').text
            announcement_detail_text = announcement_detail_soup.find('p').text.replace('\n', '\n\n')
            bot.subreddit('reddit_api_test').submit(title=announcement_detail_title,
                                                    selftext=announcement_detail_text +
                                                    '\n\nFor any information about the bot pm /u/Core_Skills.'
                                                    )


if __name__ == '__main__':
    bot = praw.Reddit(user_agent=config.user_agent,
                      client_id=config.client_id,
                      client_secret=config.client_secret,
                      username=config.username,
                      password=config.password)
    # print(bot.user.me())
    main(bot)
