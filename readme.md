# 黑盒语音 骰子机器人 
基于 [黑盒语音 - 机器人 DEMO](https://github.com/QingFengOpen/HeychatDoc/tree/main) 工程

## 介绍
实现黑盒语音骰子机器人, 用于  TRPG 文字跑团

## 依赖
- Python3
    - websockets
    - pydantic
    - requests

## 部署
### 1. Set `bot_token`
At config file `\conf\config.py`
```py
HeyChatAPPToken = "YourToken"
```
### 2. Run 
```
py main.py
```