import telegram

import asyncio

async def main(txt): #실행시킬 함수명 임의지정
    token = '6173895901:AAH54vZaLnXXZq9hngplJNeEJIDEzH2azbc' 
    bot = telegram.Bot(token = token)
    chat_id = '-1001932446119'    
    await bot.send_message(chat_id,txt)
    


asyncio.run(main('func 이거 옴?')) #봇 실행하는 코드