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
            audio_name=item.get('audio', 'unknown'),
            hearts=self.parse_formatted_numeric(item.get('hearts', '0')),
            comments=self.parse_formatted_numeric(item.get('commts', '0')),
            shares=self.parse_formatted_numeric(item.get('shares', '0')),
            user='https://www.tiktok.com/@' + item.get('user', 'unknown'),
        )

class JsonlinesWriterPipeline:
    def open_spider(self, spider):
        self.file = open('../data/tiktoks.jsonlines', 'a')

    def close_spider(self, spider):
        self.file.close()

    def process_item(self, tiktok, spider):
        line = json.dumps(ItemAdapter(tiktok).asdict()) + "\n"
        print(line)
        self.file.write(line)
        return tiktok

