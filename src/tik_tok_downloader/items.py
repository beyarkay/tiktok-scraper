from scrapy.item import Item, Field

class RawTikTokItem(Item):
    """A single TikTok before the data has been processed.
    All fields are simple strings, and may or may not be valid"""
    scraped_at = Field()
    audio_name = Field()
    hearts = Field()
    comments = Field()
    shares = Field()
    user = Field()

class TikTokItem(Item):
    """A single TikTok with all fields verified and processed into appropriate
    datatypes."""
    scraped_at = Field()
    audio_name = Field()
    hearts = Field()
    comments = Field()
    shares = Field()
    user = Field()
