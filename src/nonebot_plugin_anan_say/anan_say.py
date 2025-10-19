from nonebot import on_command, require
from nonebot.adapters import Message
from nonebot.params import CommandArg
require("nonebot_plugin_alconna")
from nonebot_plugin_alconna.uniseg import UniMessage

from io import BytesIO
from pathlib import Path

from .config import config
from .render import render

DEFAULT_FONT = str(Path(__file__).parent / 'SourceHanSansCN_Regular.otf')

anan_say = on_command("安安说")

@anan_say.handle()
async def main(content: Message = CommandArg()):
	txt = content.extract_plain_text()
	if not txt:
		txt = '你想让吾辈说些什么呢？'

	img = draw(txt)
	if not img:
		img = draw('吾辈写不了这么多字呢')
		if not img:
			await UniMessage.text('渲染失败！请调整最小字号').send()
			return

	buf = BytesIO()
	img.save(buf, format='PNG')

	await UniMessage.image(raw=buf.getvalue()).send()

def draw(data: str):
	return render(
		data,
		config.anan_say_max_font_size,
		config.anan_say_min_font_size,
		config.anan_say_font_path or DEFAULT_FONT,
	)