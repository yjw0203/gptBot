from nonebot import on_command, CommandSession
from nonebot import on_natural_language, NLPSession, IntentCommand

import openai

# Load your API key from an environment variable or secret management service
openai.api_key = "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"#os.getenv("OPENAI_API_KEY")

def chat_gpt(messages):
    # 你的问题
    try:
        # 调用 ChatGPT 接口
        #completion = openai.Completion.create(model="text-davinci-003", prompt=prompt, temperature=0.5, max_tokens=256)
        #response = completion.choices[0].text.strip()
        completion = openai.ChatCompletion.create(
             model="gpt-3.5-turbo", 
             messages=messages,
             timeout = 5000
        )
        response = completion.choices[0].message.content.strip()
    except Exception as err:
        return '服务异常。。。。。。'
    
    return response

@on_command('gpt')
async def gpt(session: CommandSession):
    if session.event.type == 'message' :
        text = session.event.raw_message.strip()
        await session.send(chat_gpt([{"role": "user", "content": text}]))


# on_natural_language 装饰器将函数声明为一个自然语言处理器
# keywords 表示需要响应的关键词，类型为任意可迭代对象，元素类型为 str
# 如果不传入 keywords，则响应所有没有被当作命令处理的消息
@on_natural_language(only_short_message=False)
async def _(session: NLPSession):
    # 返回意图命令，前两个参数必填，分别表示置信度和意图命令名
    return IntentCommand(90.0, 'gpt')


history = {}
message_list = {}

@on_command('system', aliases=('系统', 'sys','s'))
async def system(session: CommandSession):
    if session.event.type == 'message' :
        text = session.current_arg_text.strip()
        uid = getUID(session)
        if message_list.get(uid) == None:
            message_list[uid] = []
            history[uid] = ''
        message_list[uid].append({"role": "system", "content": text})
        response = chat_gpt(message_list[uid])
        history[uid] += "system: " + text + "\n" + "gpt: " + response + "\n"
        await session.send(response)

@on_command('assistant', aliases=('助手', 'ass','a'))
async def assistant(session: CommandSession):
    if session.event.type == 'message' :
        text = session.current_arg_text.strip()
        uid = getUID(session)
        if message_list.get(uid) == None:
            message_list[uid] = []
            history[uid] = ''
        message_list[uid].append({"role": "assistant", "content": text})
        response = chat_gpt(message_list[uid])
        history[uid] += "assistant: " + text + "\n" + "gpt: " + response + "\n"
        await session.send(response)

@on_command('user', aliases=('用户', 'u'))
async def user(session: CommandSession):
    if session.event.type == 'message' :
        text = session.current_arg_text.strip()
        uid = getUID(session)
        if message_list.get(uid) == None:
            message_list[uid] = []
            history[uid] = ''
        message_list[uid].append({"role": "user", "content": text})
        response = chat_gpt(message_list[uid])
        history[uid] += "user: " + text + "\n" + "gpt: " + response + "\n"
        await session.send(response)

@on_command('clear', aliases=('清除', 'clr', 'c'))
async def clear(session: CommandSession):
    if session.event.type == 'message' :
        uid = getUID(session)
        message_list[uid] = []
        history[uid] = ''
        await session.send('已清空历史')

@on_command('list', aliases=('列表', 'l'))
async def list(session: CommandSession):
    if session.event.type == 'message' :
        uid = getUID(session)
        res = ''
        for message in message_list[uid] :
            res += message["role"] + ": " + message["content"] + "\n"
        if res == '':
            res = '历史列表为空'
        await session.send(res)

@on_command('history', aliases=('历史', '历史记录','his','h'))
async def list(session: CommandSession):
    if session.event.type == 'message' :
        uid = getUID(session)
        if history.get(uid) == None :
            history[uid] = ''
        if history[uid] == '':
            await session.send('历史记录为空')
        else :
            await session.send(history[uid])
        

def getUID(session: CommandSession):
    if session.event.type == 'message' :
        if session.event.detail_type == 'group' :
            return session.event.group_id
        if session.event.detail_type == 'private' :
            return session.event.user_id
    return ''    
    