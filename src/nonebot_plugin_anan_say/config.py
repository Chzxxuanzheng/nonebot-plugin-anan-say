from typing import Optional
from pydantic import BaseModel
from nonebot import get_plugin_config

class Config(BaseModel):
	"""Plugin Config Here"""
	anan_say_max_font_size: int = 200
	''' 最大字体大小 '''
	anan_say_min_font_size: int = 40
	''' 最小字体大小 '''
	anan_say_font_path: Optional[str] = None
	''' 字体文件路径，留空则使用默认字体 '''

	anan_say_library_mode: bool = False
	''' 库模式 '''

config: Config = get_plugin_config(Config)