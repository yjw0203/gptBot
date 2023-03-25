# gptBot
## 描述
集成了chatGPT接口的QQ机器人。
## 环境搭建
### 解释器
Python 3.10.7
### 库依赖
#### openai
```
pip install openai -i https://pypi.tuna.tsinghua.edu.cn/simple/
```
#### nonebot
```
pip install nonebot
```
### 配置
config.yml
``` yml
account: # 账号相关
  uin: 1000000000 # QQ账号
  password: '111111111' # 密码为空时使用扫码登录
 
 ...
 
servers:
  - ws-reverse:
      universal: ws://127.0.0.1:8080/ws/ #填入自己的ip地址
```
config.py
``` py
from nonebot.default_config import *

SUPERUSERS = {12345678}

HOST = '127.0.0.1' # 填入自己的ip地址，与config.yml中的对应
PORT = 8080 # 填入端口号，与config.yml中的对应
```
openai.api_key
``` py
# openai密钥，在上传git后会失效，需要自己手动搞一个
openai.api_key = "***"
```
### 启动
启动launcher.bat，第一次启动可能要做QQ验证，注意看log。
### 开发
添加插件，见https://docs.nonebot.dev/guide/installation.html
