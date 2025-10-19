<div align="center">
  <a href="https://v2.nonebot.dev/store"><img src="https://github.com/A-kirami/nonebot-plugin-template/blob/resources/nbp_logo.png" width="180" height="180" alt="NoneBotPluginLogo"></a>
  <br>
  <p><img src="https://github.com/A-kirami/nonebot-plugin-template/blob/resources/NoneBotPlugin.svg" width="240" alt="NoneBotPluginText"></p>
</div>

<div align="center">

# nonebot-plugin-anan-say

_✨ 安安的素描本上都写了什么呢？ ✨_


<a href="./LICENSE">
    <img src="https://img.shields.io/github/license/Chzxxuanzheng/nonebot_plugin_anan_say.svg" alt="license">
</a>
<a href="https://pypi.python.org/pypi/nonebot-plugin-anan-say">
    <img src="https://img.shields.io/pypi/v/nonebot_plugin_anan_say.svg" alt="pypi">
</a>
<img src="https://img.shields.io/badge/python-3.9+-blue.svg" alt="python">

<b>本插件仅供学习交流使用，请勿用于其他用途
版权争议请提出 issue 协商</b>

</div>

一个向安安的素描本上渲染文字并发送出去的插件

## 📖 介绍

一个向安安的素描本上渲染文字并发送出去的插件。支持富文本渲染。

## 💿 安装

<details open>
<summary>使用 nb-cli 安装</summary>
在 nonebot2 项目的根目录下打开命令行, 输入以下指令即可安装

    nb plugin install nonebot-plugin-anan-say

</details>

<details>
<summary>使用包管理器安装</summary>
在 nonebot2 项目的插件目录下, 打开命令行, 根据你使用的包管理器, 输入相应的安装命令

<details>
<summary>pip</summary>

    pip install nonebot-plugin-anan-say
</details>
<details>
<summary>pdm</summary>

    pdm add nonebot-plugin-anan-say
</details>
<details>
<summary>poetry</summary>

    poetry add nonebot-plugin-anan-say
</details>
<details>
<summary>conda</summary>

    conda install nonebot-plugin-anan-say
</details>

打开 nonebot2 项目根目录下的 `pyproject.toml` 文件, 在 `[tool.nonebot]` 部分追加写入

    plugins = ["nonebot_plugin_template"]

</details>

## ⚙️ 配置

在 nonebot2 项目的`.env`文件中添加下表中的必填配置

| 配置项 | 必填 | 默认值 | 说明 |
|:-----:|:----:|:----:|:----:|
| anan_say_max_font_size | 否 | 200 | 最大字号 |
| anan_say_min_font_size | 否 | 40 | 最小字号 |
| anan_say_font_path | 否 | 无 | 自定义字体路径(默认思源黑体) |
| anan_say_library_mode | 否 | False | 库模式 |

<details>
<summary>库模式</summary>
请您在对nonebot插件开发有一定了解后再看。

不同人的bot有自己不同的插件管理方式，或者指令格式规范。单纯写死on_command无法满足不同bot的客制化需求。
如果您也有这种客制化需求，请将`anan_say_library_mode`设置为`True`。然后在您的插件里引入一下代码来进行渲染。

```python
require('nonebot_plugin_anan_say')
from nonebot_plugin_anan_say.render import render
```
render函数用法:

|参数|类型|作用|
|:--:|:-:|:--:|
|txt|str|要渲染的文本|
|max_font_size|int|最大字号|
|min_font_size|int|最小字号|
|fontpath|str|字体路径|

返回值为`PIL.Image.Image`对象

~~真会有人用这东西吗？用得上的大佬基本上都自己写插件，不会考虑引入第三方的吧...~~
</details>

## 🎉 使用
### 指令表
| 指令 | 权限 | 需要@ | 范围 | 说明 |
|:-----:|:----:|:----:|:----:|:----:|
| 安安说 + 命令 | 无 | 否 | 群聊 | 指令说明 |
### 效果图
![效果图](./docs/effect_img.png)
