from nonebot.plugin import PluginMetadata

from .config import Config, config

from .adapter_check import get_supported_adapters

__plugin_meta__ = PluginMetadata(
	name="安安说",
	description="一个向安安的素描本上渲染文字并发送出去的插件",
	usage="发送指令`安安说 + 内容`来使用\n",

	type="application",

	homepage="https://github.com/Chzxxuanzheng/nonebot_plugin_anan_say",
	# 发布必填。

	config=Config,
	# 插件配置项类，如无需配置可不填写。

	supported_adapters=get_supported_adapters()
)


# 加载主matcher
if not config.anan_say_library_mode:
	import nonebot_plugin_anan_say.anan_say