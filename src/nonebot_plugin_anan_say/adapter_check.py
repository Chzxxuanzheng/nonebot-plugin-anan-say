from nonebot import require

require("nonebot_plugin_alconna")
import nonebot_plugin_alconna.uniseg.adapters as adapters_pkg
from nonebot_plugin_alconna.uniseg.constraint import SupportAdapterModule
import pkgutil

def read_adapter_exporters() -> dict[str, str]:
	"""
	遍历 nonebot_plugin_alconna.adapters 下的所有子包，
	读取每个子包中的 exporter.py 文件内容为字符串。
	返回映射：{ 子包名: exporter.py 文本内容 }。
	"""
	results: dict[str, str] = {}

	# 遍历 adapters 包下的所有一级子包
	for mod_info in pkgutil.iter_modules(adapters_pkg.__path__):
		name = mod_info.name
		if name.startswith("_"):
			continue  # 跳过私有/内部目录

		package_name = f"{adapters_pkg.__name__}.{name}"
		content = read_exporter_from_package(package_name)

		if content is not None:
			results[name] = content

	return results


def read_exporter_from_package(package_name: str) -> str | None:
	"""
	读取给定子包中的 exporter.py 内容。
	优先使用 importlib.resources.files（兼容 zip 包），
	回退到 pkgutil.get_data。
	"""
	try:
		from importlib import resources
		try:
			base = resources.files(package_name)
			exporter = base.joinpath("exporter.py")
			if exporter.is_file():
				try:
					return exporter.read_text(encoding="utf-8")
				except UnicodeDecodeError:
					# 编码兜底
					return exporter.read_text()
		except ModuleNotFoundError:
			# 子包可能不存在或被可选安装排除
			return None
	except Exception:
		# 任意异常都继续尝试回退方案
		pass


def check_adapter_support(content: str) -> bool:
	"""
	检查给定 Python 源码文本中，是否存在：
	from nonebot_plugin_alconna.uniseg.segment import Image
	或
	from nonebot_plugin_alconna.uniseg.segment import *
	"""
	import ast

	try:
		tree = ast.parse(content)
	except SyntaxError:
		# 解析失败时，不认为支持
		return False

	target_module = "nonebot_plugin_alconna.uniseg.segment"

	for node in ast.walk(tree):
		# 过滤非导入模块
		if not isinstance(node, ast.ImportFrom): continue

		# 过滤非目标模块
		if node.module != target_module: continue

		for alias in node.names:
			# 直接导入 Image，或 *（包含所有导出）
			if alias.name == "Image" or alias.name == "*":
				return True
					
	return False

def get_supported_adapters() -> set[str]:
	"""
	获取支持的适配器
	"""
	re = set()
	adapters = read_adapter_exporters()
	for name in adapters:
		if not hasattr(SupportAdapterModule, name): continue
		if not check_adapter_support(adapters[name]): continue
		re.add(getattr(SupportAdapterModule, name).value)

	return re