from nonebot.plugin import PluginMetadata, inherit_supported_adapters

from nonebot import require
require('nonebot_plugin_alconna')

from .config import Config, config

__plugin_meta__ = PluginMetadata(
	name="安安说",
	description="一个向安安的素描本上渲染文字并发送出去的插件",
	usage="发送指令`安安说 + 内容`来使用\n",

	type="application",

	homepage="https://github.com/Chzxxuanzheng/nonebot_plugin_anan_say",
	# 发布必填。

	config=Config,

	supported_adapters=inherit_supported_adapters('nonebot_plugin_alconna')
)


# 加载主matcher
if not config.anan_say_library_mode:
	import nonebot_plugin_anan_say.anan_say