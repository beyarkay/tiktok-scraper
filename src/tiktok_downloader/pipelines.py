from itemadapter import ItemAdapter
from tiktok_downloader.items import TikTokItem
import json

class CookTikTokPipeline:
    def parse_formatted_numeric(self, n: str) -> int:
        if n[-1] == "M":
            return int(float(n[:-1]) * 1_000_000)
        elif n[-1] == "K":
            return int(float(n[:-1]) * 1_000)
        else:
            return int(n)

    def process_item(self, item, spider):
        return TikTokItem(
            scraped_at=item.get('scraped_at', 'NaT').strftime("%Y-%m-%dT%H:%M:%S"),
            url=item.get('url', 'NaT'),
            audio=item.get('audio', '<no audio>'),
            audio_url=item.get('audio_url', '<no audio>'),
            likes=self.parse_formatted_numeric(item.get('likes', '0')),
            comments=self.parse_formatted_numeric(item.get('comments', '0')),
            username='https://www.tiktok.com/@' + item.get('username', '<no_username>'),
            user_followers = self.parse_formatted_numeric(item.get('user_followers', '<no data>')),
            user_likes = self.parse_formatted_numeric(item.get('user_likes', '<no data>')),
        )

class JsonlinesWriterPipeline:
    def open_spider(self, spider):
        self.file = open('../data/tiktoks.jsonlines', 'a')

    def close_spider(self, spider):
        self.file.close()

    def process_item(self, tiktok, spider):
        line = json.dumps(ItemAdapter(tiktok).asdict()) + "\n"
        self.file.write(line)
        return tiktok

