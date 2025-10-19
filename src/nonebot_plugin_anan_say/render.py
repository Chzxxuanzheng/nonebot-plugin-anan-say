from PIL import Image, ImageDraw, ImageFont
from functools import cache
from typing import Optional
from .typing import Cmd, LineInfo, TagMap
from pathlib import Path

BOOK_LEFT = 320
BOOK_TOP = 875
BOOK_WIDTH = 675
BOOK_HEIGHT = 350
PADDING = 20

ANAN_PATH = Path(__file__).parent / 'anan.png'

def hex_to_rgba(hex_code: str) -> tuple[int, int, int, int]:
	'''
	将十六进制颜色代码转换为 RGBA 元组
	'''
	r = int(hex_code[0:2], 16)
	g = int(hex_code[2:4], 16)
	b = int(hex_code[4:6], 16)
	return (r, g, b, 255)

@cache
def get_char_size(char: str, font_size: int, fontpath: str) -> tuple[int, int]:
	font = ImageFont.truetype(fontpath, font_size)
	tmp = font.getbbox(char)
	return int(tmp[2] - tmp[0]), int(tmp[3] - tmp[1])

def parse_tag(data: str) -> tuple[Cmd, int]:
	'''
	解析单个标签，返回命令和消耗长度
	'''
	NORMAL_TAGS: TagMap = {
		'b': 'bold',
		'u': 'underline',
		's': 'strike',
	}
	# 常规标签检测
	for i in NORMAL_TAGS:
		if data.startswith(f'[{i}]'):
			return {
				'type': 'mode',
				'mode': NORMAL_TAGS[i],
				'value': True
			}, 3
		elif data.startswith(f'[/{i}]'):
			return {
				'type': 'mode',
				'mode': NORMAL_TAGS[i],
				'value': False
			}, 4
	
	# 颜色标签检测
	if data.startswith('[/c]'):
		return {
			'type': 'mode',
			'mode': 'color',
			'value': False
		}, 4
	elif data.startswith('[c '):
		if len(data) < 12:
			return {
				'type': 'content',
				'data': data[0],
			}, 1
		if data[3] != '#' or data[10] != ']':
			return {
				'type': 'content',
				'data': data[0],
			}, 1
		hex_code = data[4:10]
		try:
			assert int(hex_code, 16) < 0x1000000
			return {
				'type': 'mode',
				'mode': 'color',
				'value': str(hex_code),
			}, 11
		except (AssertionError, ValueError):
			return {
				'type': 'content',
				'data': data[0],
			}, 1

	return {
		'type': 'content',
		'data': data[0],
	}, 1

def parse_commands(data: str) -> list[Cmd]:
	'''
	解析输入字符串为命令列表
	'''
	out = []
	now_id = 0
	while True:
		if now_id >= len(data): break
		c = data[now_id:now_id+1]
		if c == '[':
			cmd, length = parse_tag(data[now_id:])
			out.append(cmd)
			now_id += length
			continue

		out.append({
			'type': 'content',
			'data': c,
		})

		now_id += 1

	return out

def calc_range(data: list[Cmd], font_size: int, range: tuple[int, int], fontpath: str) -> Optional[list[LineInfo]]:
	'''
	计算文本在指定范围内的行信息，返回行列表或 None（超出范围）
	'''
	line_infos: list[LineInfo] = []
	current_line = 0
	current_line_data: list[Cmd] = []
	current_pos = 0
	current_width = 0
	current_height = 0
	current_line_height = 0

	def new_line() -> bool:
		nonlocal current_line, current_pos, current_width, current_height, \
				current_line_height, current_line_data
		line_infos.append({
			'width': current_width,
			'height': current_line_height,
			'content': current_line_data,
		})
		current_line += 1
		current_height += current_line_height
		current_line_height = 0
		current_pos = 0
		current_width = 0
		current_line_data = []
		return current_height <= range[1]

	for cmd in data:
		# 处理标签命令
		if cmd['type'] == 'mode':
			current_line_data.append(cmd)
			continue

		# 处理内容命令
		char = cmd['data']
		# 换行特殊处理
		if char == '\n':
			if not new_line(): return None
			continue
		width, height = get_char_size(char, font_size, fontpath)
		# 增加范围
		if current_width + width > range[0]:
			# 超出范围，换行
			if not new_line(): return None
		current_pos += 1
		current_width += width
		if height > current_line_height:
			current_line_height = height
		current_line_data.append(cmd)
	# 保存最后一行
	new_line()

	return line_infos

def find_font_size(data: list[Cmd], start: int, end: int, range: tuple[int, int], fontpath: str) -> tuple[int, Optional[list[LineInfo]]]:
	'''
	在指定范围内寻找合适的字体大小，返回字号和行信息列表
	'''
	last_size = start
	last_line_info = calc_range(data, last_size, range, fontpath)
	current_size = start
	current_line_info = last_line_info
	while True:
		if last_line_info is not None:
			# 尝试增大字号
			next_size = int(current_size + abs(current_size - last_size) / 2)
		else:
			# 尝试减小字号
			next_size = int(current_size - abs(current_size - end) / 2)
		# 字号无变化为最优解
		if next_size == last_size: break
		if next_size < end: break
		next_line_info = calc_range(data, next_size, range, fontpath)
		
		# 更新状态
		last_size, last_line_info = current_size, current_line_info
		current_size, current_line_info = next_size, next_line_info

	return current_size, current_line_info

def render_rich_text_to_image(
		line_infos: list[LineInfo],
		font_size: int,
		range: tuple[int, int],
		fontpath: str
	) -> Image.Image:
	'''
	渲染富文本函数
	'''
	img = Image.new("RGBA", range, (255, 255, 255, 0))
	all_height = sum([line['height'] for line in line_infos])
	current_y = (range[1] - all_height) // 2 - line_infos[0]['height'] // 2

	default_color = (0, 0, 0, 255)

	bold: bool = False
	underline: bool = False
	strike: bool = False
	color = default_color
	font = ImageFont.truetype(fontpath, font_size)
	for line in line_infos:
		current_x = (range[0] - line['width']) // 2
		for cmd in line['content']:
			# 处理标签命令
			if cmd['type'] == 'mode':
				if cmd['mode'] == 'bold':
					bold = cmd['value']  # type: ignore
				elif cmd['mode'] == 'underline':
					underline = cmd['value']  # type: ignore
				elif cmd['mode'] == 'strike':
					strike = cmd['value']  # type: ignore
				elif cmd['mode'] == 'color':
					if cmd['value'] is False:
						color = default_color
					else:
						color = hex_to_rgba(cmd['value'])  # type: ignore
				continue

			# 处理内容命令
			char = cmd['data']
			draw = ImageDraw.Draw(img)
			draw.text((current_x, current_y), char, font=font, fill=color)
			char_size = get_char_size(char, font_size, fontpath)
			if bold:
				draw.text((current_x + 1, current_y), char, font=font, fill=color)
				draw.text((current_x - 1, current_y), char, font=font, fill=color)
				draw.text((current_x, current_y + 1), char, font=font, fill=color)
				draw.text((current_x, current_y - 1), char, font=font, fill=color)
			if underline:
				ascent, descent = font.getmetrics()
				baseline = current_y + ascent
				thickness = max(1, font_size // 15)
				uy = baseline + max(1, descent // 2)
				draw.line((current_x, uy, current_x + char_size[0], uy), fill=color, width=thickness)
			if strike:
				ascent, descent = font.getmetrics()
				baseline = current_y + ascent
				thickness = max(1, font_size // 15)
				sy = baseline - max(1, ascent // 3)
				draw.line((current_x, sy, current_x + char_size[0], sy), fill=color, width=thickness)
			current_x += char_size[0]

		current_y += line['height']

	return img

def render(txt: str, max_font_size: int, min_font_size: int, fontpath: str) -> Optional[Image.Image]:
	'''
	渲染函数
	空间不足返回 None
	'''
	# 解析命令
	cmds = parse_commands(txt)

	# 寻找合适字号
	font_size, line_infos = find_font_size(
		cmds,
		max_font_size,
		min_font_size,
		(BOOK_WIDTH - PADDING * 2, BOOK_HEIGHT - PADDING * 2),
		fontpath
	)
	if not line_infos: return None
	img = render_rich_text_to_image(
		line_infos,
		font_size,
		(BOOK_WIDTH, BOOK_HEIGHT),
		fontpath
	)
	bg = Image.open(ANAN_PATH)
	bg.paste(img, (BOOK_LEFT, BOOK_TOP), img)
	return bg