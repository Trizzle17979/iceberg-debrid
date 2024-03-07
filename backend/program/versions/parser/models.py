import PTN
from typing import List
from pydantic import BaseModel, Field
from .patterns import (
    MULTI_AUDIO_COMPILED,
    MULTI_SUBTITLE_COMPILED,
    COMPLETE_SERIES_COMPILED,
    UNWANTED_QUALITY_COMPILED,
)


class ParsedMediaItem(BaseModel):
    """ParsedMediaItem class containing parsed data from `PTN` library."""

    raw_title: str = Field(...)
    parsed_title: str = Field(default="")
    is_4k: bool = Field(default=False)
    is_multi_audio: bool = Field(default=False)
    is_multi_subtitle: bool = Field(default=False)
    is_complete: bool = Field(default=False)
    is_unwanted_quality: bool = Field(default=False)
    year: List[int] = Field(default=[])
    resolution: List[str] = Field(default=[])
    quality: List[str] = Field(default=[])
    season: List[int] = Field(default=[])
    episodes: List[int] = Field(default=[])
    codec: List[str] = Field(default=[])
    audio: List[str] = Field(default=[])
    hdr: bool = Field(default=False)
    upscaled: bool = Field(default=False)
    remastered: bool = Field(default=False)
    proper: bool = Field(default=False)
    repack: bool = Field(default=False)
    subtitles: bool = Field(default=False)
    language: List[str] = Field(default=[])
    remux: bool = Field(default=False)
    extended: bool = Field(default=False)

    class Config:
        arbitrary_types_allowed = True

    def __init__(self, **data):
        super().__init__(**data)
        self.parse_raw_title()

    def parse_raw_title(self):
        """Parse the raw string using PTN library."""
        parsed: dict = PTN.parse(self.raw_title, coherent_types=True)
        self.parsed_title = parsed.get("title", "")
        self.year = parsed.get("year", [])
        self.resolution = parsed.get("resolution", [])
        self.quality = parsed.get("quality", [])
        self.season = parsed.get("season", [])
        self.episodes = parsed.get("episode") if isinstance(parsed.get("episode"), list) else [parsed.get("episode")] if parsed.get("episode") else []
        self.codec = parsed.get("codec", [])
        self.audio = parsed.get("audio", [])
        self.language = parsed.get("language", [])
        self.is_4k = any(resolution in ["2160p", "4K", "UHD"] for resolution in parsed.get('resolution', []))
        self.hdr = parsed.get("hdr", False)
        self.upscaled = parsed.get("upscaled", False)
        self.remastered = parsed.get("remastered", False)
        self.proper = parsed.get("proper", False)
        self.repack = parsed.get("repack", False)
        self.subtitles = parsed.get("subtitles", False)
        self.remux = parsed.get("remux", False)
        self.extended = parsed.get("extended", False)

        self.is_unwanted_quality = self.check_unwanted_quality(self.raw_title)
        self.is_multi_audio = self.check_multi_audio(self.raw_title)
        self.is_multi_subtitle = self.check_multi_subtitle(self.raw_title)
        self.is_complete = self.check_complete_series(self.raw_title)

    @staticmethod
    def check_multi_audio(string) -> bool:
        """Check if the string contains multi-audio pattern."""
        return any(pattern.search(string) for pattern in MULTI_AUDIO_COMPILED)

    @staticmethod
    def check_multi_subtitle(string) -> bool:
        """Check if the string contains multi-subtitle pattern."""
        return any(pattern.search(string) for pattern in MULTI_SUBTITLE_COMPILED)

    @staticmethod
    def check_complete_series(string) -> bool:
        """Check if the string contains complete series pattern."""
        return any(pattern.search(string) for pattern in COMPLETE_SERIES_COMPILED)

    @staticmethod
    def check_unwanted_quality(string) -> bool:
        """Check if the string contains unwanted quality pattern."""
        return any(pattern.search(string) for pattern in UNWANTED_QUALITY_COMPILED)
