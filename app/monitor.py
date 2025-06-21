import os
import smtplib
import time
from email.mime.text import MIMEText

import feedparser
from bs4 import BeautifulSoup

# --- 환경 변수에서 설정 값 가져오기 ---
RSS_URL = os.getenv('TARGET_URL')
RECIPIENT_EMAIL = os.getenv('RECIPIENT_EMAIL')
SMTP_SERVER = os.getenv('SMTP_SERVER')
SMTP_PORT = int(os.getenv('SMTP_PORT', 587))
SENDER_EMAIL = os.getenv('SENDER_EMAIL')
SENDER_PASSWORD = os.getenv('SENDER_PASSWORD')

# 마지막으로 확인된 게시물의 링크를 저장할 파일
LAST_POST_LINK_FILE = '/app/data/last_post_link.txt'

def get_latest_post(feed_url):
    """RSS 피드를 파싱하여 가장 최신 게시물 정보와 PDF 다운로드 링크를 반환합니다."""
    try:
        feed = feedparser.parse(feed_url)
        if not feed.entries:
            return None

        latest_post = feed.entries[0]
        post_info = {
            'title': latest_post.title,
            'link': latest_post.link,
            'published': latest_post.get('published', 'No date'),
            'download_link': 'Not found'
        }

        if 'content' in latest_post and latest_post.content:
            content_html = latest_post.content[0].value
            soup = BeautifulSoup(content_html, 'html.parser')
            download_tag = soup.select_one('a.wp-block-button__link')
            if download_tag and download_tag.has_attr('href'):
                post_info['download_link'] = download_tag['href']

        return post_info

    except Exception as e:
        print(f"Error fetching or parsing RSS feed: {e}")
        return None

def send_notification_email(post):
    """새 게시물 알림 이메일을 보냅니다."""
    try:
        subject = f"New SMIC Research: {post['title']}"
        body = f"""
        A new research post has been published on SMIC.

        Title: {post['title']}
        
        Website Link: {post['link']}
        Direct PDF Download: {post['download_link']}

        Published: {post['published']}
        """
        
        msg = MIMEText(body, 'plain', 'utf-8')
        msg['Subject'] = subject
        msg['From'] = SENDER_EMAIL
        msg['To'] = RECIPIENT_EMAIL

        with smtplib.SMTP(SMTP_SERVER, SMTP_PORT) as server:
            server.starttls()
            server.login(SENDER_EMAIL, SENDER_PASSWORD)
            server.send_message(msg)
        print("Notification email sent successfully!")
    except Exception as e:
        print(f"Failed to send email: {e}")

def main():
    print(f"[{time.ctime()}] Checking for new post at {RSS_URL}...")

    latest_post = get_latest_post(RSS_URL)
    if not latest_post:
        return

    current_latest_link = latest_post['link']
    last_post_link = ""
    if os.path.exists(LAST_POST_LINK_FILE):
        with open(LAST_POST_LINK_FILE, 'r') as f:
            last_post_link = f.read().strip()

    if current_latest_link != last_post_link:
        print(f"New post found! Title: {latest_post['title']}")
        send_notification_email(latest_post)
        os.makedirs(os.path.dirname(LAST_POST_LINK_FILE), exist_ok=True)
        with open(LAST_POST_LINK_FILE, 'w') as f:
            f.write(current_latest_link)
    else:
        print("No new post found.")

if __name__ == "__main__":
    main()