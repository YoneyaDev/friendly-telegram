# friendly-telegram

from .. import loader, utils  # pylint: disable=relative-beyond-top-level
import io
from PIL import Image, ImageOps
from telethon.tl.types import DocumentAttributeFilename
import logging
import random

logger = logging.getLogger(__name__)

def register(cb):
	cb(Ебал_я_в_рот_ваш_пеп_8_Mod())


@loader.tds
class Ебал_я_в_рот_ваш_пеп_8_Mod(loader.Module):
	"""Гавно залупное"""
	strings = {
		"name": "Хуификатор"
	}

	async def client_ready(self, client, db):
		self.client = client
	
	
	@loader.sudo
	async def хуйcmd(self, message):
		text = utils.get_args(message)
		if not text:
			reply = await message.get_reply_message()
			if not reply:
				await message.delete()
				return
			text = reply.raw_text.split()
		async def huify(word):
			word = word.lower().strip()
			vowels = 'аеёиоуыэюя'
			rules = {
				'а': 'я',
				'о': 'ё',
				'у': 'ю',
				'ы': 'и',
				'э': 'е',
			}
			for letter in word:
				if letter in vowels:
					if letter in rules:
						word = rules[letter] + word[1:]
					break
				else:
					word = word[1:]
			return 'Ху' + word if word else 'Хуй'
		
		out = []
		for word in text:
			хуй = await huify(word)
			out.append(хуй)
		await message.reply(" ".join(out))
		
	async def хуйняcmd(self, message):
		text = utils.get_args(message)
		if not text:
			reply = await message.get_reply_message()
			if not reply:
				await message.delete()
				return
			text = reply.raw_text.split()
		async def huify(word):
			word = word.lower().strip()
			vowels = 'аеёиоуыэюя'
			rules = {
				'а': 'я',
				'о': 'ё',
				'у': 'ю',
				'ы': 'и',
				'э': 'е',
			}
			for letter in word:
				if letter in vowels:
					if letter in rules:
						word = rules[letter] + word[1:]
					break
				else:
					word = word[1:]
			return 'Ху' + word if word else 'Хуй'
		
		out = []
		for word in text:
			хуй = await huify(word)
			out.append(f"{word}-{хуй}")
		await message.reply(" ".join(out))
