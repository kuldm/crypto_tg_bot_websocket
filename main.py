import asyncio
import json
import time

from aiogram import Bot, Dispatcher
from aiogram.types import Message
from aiogram.filters import CommandStart
import websockets

BOT_TOKEN = "8378015797:AAGEdTn1dadKxBk_HcS-PZ-hcsqFVqPWn68"
user_id = "234565580"
last_sent_time = 0

bot = Bot(
    token=BOT_TOKEN,
)

dp = Dispatcher()


binance_url = "wss://stream.binance.com/ws/btcusdt@aggTrade"


@dp.message(CommandStart())
async def get_start(message: Message):
    user_id = message.from_user.id
    await message.answer(f"{user_id=}")


async def fetch_binance_trades(url: str):
    global last_sent_time
    async with websockets.connect(url) as ws:
        async for msg in ws:
            data = json.loads(msg)
            price = data["p"]
            if time.time() - last_sent_time > 5:
                await send_message_to_tg(
                    msg=f"Последняя цена BTC/USDT: {price}"
                )
                last_sent_time = time.time()


async def send_message_to_tg(msg: str):
    await bot.send_message(chat_id=user_id, text=msg)


async def main():
    async with asyncio.TaskGroup() as task_group:
        task_group.create_task(fetch_binance_trades(binance_url))
        task_group.create_task(dp.start_polling(bot, handle_sigmals=False))


if __name__ == "__main__":
    asyncio.run(main())
