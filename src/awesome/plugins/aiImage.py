
import openai
from nonebot import on_command, CommandSession

def get_image(decriptor):
    try:
        response = openai.Image.create(
            prompt=decriptor,
            n=1,
            size="1024x1024"
        )
        image_url = response['data'][0]['url']
    except Exception as err:
        return 'None'
    return image_url

# on_command 装饰器将函数声明为一个命令处理器
@on_command('image', aliases=('图片', 'im'))
async def AIImage(session: CommandSession):
    decriptor = session.current_arg_text.strip()
    await session.send(f"[CQ:image,file={get_image(decriptor)}]")
