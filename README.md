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

## 🎉 使用
### 指令表
| 指令 | 权限 | 需要@ | 范围 | 说明 |
|:-----:|:----:|:----:|:----:|:----:|
| 安安说 + 命令 | 无 | 否 | 群聊 | 指令说明 |
### 效果图
![效果图](./docs/effect_img.png)
