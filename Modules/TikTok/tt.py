from JZBot import dp, GetChatStatus, ReplyVideo, ReplyMsg, TextByLang
from httpx import AsyncClient

def tt_text(number):
    return TextByLang({
        'ru': [
            'Необходимо указать ссылку на видео TikTok',
            'Не удалось загрузить TikTok видео'
        ],
        'uk': [
            'Необхідно вказати посилання на відео TikTok',
            'Не вдалося завантажити TikTok відео'
        ],
        'en': [
            'TikTok video link required',
            'Failed to download TikTok video'
        ]
    }, number)

@dp.message_handler(commands=['tt'])
async def main_tt(msg):
    if await GetChatStatus(msg) is not False:
        if 'https://' in msg.text and 'tiktok.com' in msg.text:
            try:
                async with AsyncClient() as client:
                    tt_get = (await client.get(f'https://api.douyin.wtf/api?url={msg.text.split()[1]}&minimal=true')).json()
                    await ReplyVideo(msg, tt_get['nwm_video_url'], caption=tt_get['desc'])
            except:
                await ReplyMsg(msg, tt_text(1))
        else:
            await ReplyMsg(msg, tt_text(0))
