### Instalation:

```bash
git clone --depth=1 https://github.com/jzinferno/JZBot.git
cd JZBot && ./main.py
```

### Module template

```python
from JZBot import JZBot
from main import dp

@dp.message_handler(commands=['hello'])
async def main_hello(msg):
    await JZBot.ReplyMsg(msg, 'Hello World!')
```

### config.json

```json
{
  "bot_token": "0000000000:XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX",
  "openai_key": "sk-XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX",
  "lang": "en"
}
```
