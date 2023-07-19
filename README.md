### Instalation:

```bash
curl -sL https://github.com/jzinferno/JZBot/raw/main/install.sh | bash
```

### Module template

```python
from JZBot import dp, ReplyMsg

@dp.message_handler(commands=['hello'])
async def main_hello(msg):
    await ReplyMsg(msg, 'Hello World!')
```

### config.json

```json
{
  "bot_token": "",
  "openai_key": "",
  "openweather_key": "",
  "iloveimg_key": "",
  "ilovepdf_key": "",
  "lang": "en",
  "chats": [
    -1001609560469
  ]
}
```
