from JZBot import dp, GetChatStatus, ReplyVideo, ReplyMsg, TextByLang
from httpx import AsyncClient

def tt_text(text):
    return TextByLang({
        'ru': {
            'text_1': 'Необходимо указать ссылку на видео TikTok',
            'text_2': 'Не удалось загрузить TikTok видео'
        },
        'uk': {
            'text_1': 'Необхідно вказати посилання на відео TikTok',
            'text_2': 'Не вдалося завантажити TikTok відео'
        },
        'en': {
            'text_1': 'TikTok video link required',
            'text_2': 'Failed to download TikTok video'
        }
    }, text)

@dp.message_handler(commands=['tt'])
async def main_tt(msg):
    if await GetChatStatus(msg) is not False:
        if 'https://' in msg.text and 'tiktok.com' in msg.text:
            try:
                async with AsyncClient() as client:
                    tt_get = (await client.get(f'https://api.douyin.wtf/api?url={msg.text.split()[1]}&minimal=true')).json()
                    await ReplyVideo(msg, tt_get['nwm_video_url'], caption=tt_get['desc'])
            except:
                await ReplyMsg(msg, tt_text('text_2'))
        else:
            await ReplyMsg(msg, tt_text('text_1'))
