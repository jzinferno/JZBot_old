### Instalation:

```bash
git clone --depth=1 https://github.com/jzinferno/JZBot.git
cd JZBot
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt
./main.py
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
  "lang": "en",
  "chats": [
    -1001609560469
  ]
}
```
