from typing import TypedDict, Literal, Union

class Content(TypedDict):
	type: Literal['content']
	data: str

class Tag(TypedDict):
	type: Literal['mode']
	mode: Literal['bold', 'underline', 'strike', 'color']
	value: Union[bool, str]

class TagMap(TypedDict):
	b: Literal['bold']
	u: Literal['underline']
	s: Literal['strike']

Cmd = Union[Content, Tag]

class LineInfo(TypedDict):
	width: int
	height: int
	content: list[Cmd]