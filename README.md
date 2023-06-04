### Instalation:

```bash
git clone --depth=1 https://github.com/jzinferno/JZBot.git && cd JZBot
pip3 install -r requirements.txt --upgrade
python3 ./main.py
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
  "bot_token": "0000000000:XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX",
  "openai_key": "sk-XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX",
  "lang": "en",
  "chats": {
    "0000000000": 1,
    "9999999999": 1
  }
}
```
