# friendly-telegram

import requests 
from .. import loader, utils 
 
 
def register(cb): 
    cb(WeatherMod()) 
     
class WeatherMod(loader.Module): 
    """Погода с сайта wttr.in""" 
    strings = {'name': 'Weather'} 
     
    async def pwcmd(self, message): 
        """"Кидает погоду картинкой.\nИспользование: .pw <город>; ничего.""" 
        args = utils.get_args_raw(message).replace(' ', '+')
        city = requests.get(f"https://wttr.in/{args if args != None else ''}.png").content 
        await message.client.send_file(reply_to.message_id, city)
 
 
    async def awcmd(self, message): 
        """Кидает погоду ascii-артом.\nИспользование: .aw <город>; ничего.""" 
        city = utils.get_args_raw(message)
        r = requests.get(f"https://wttr.in/{city if city != None else ''}?0?q?T&lang=ru") 
        await message.reply(f"<code>Город: {r.text}</code>")
