# friendly-telegram

import asyncio
import logging
import io
from .. import loader, utils

logger = logging.getLogger(__name__)


@loader.tds
class SavedMod(loader.Module):
	"""Созранятель в избранное"""
	strings = {"name": "Сохранение"}

	
	@loader.unrestricted
	async def mecmd(self, message):
		""".me реплай на медиа"""
		await message.delete()
		reply = await message.get_reply_message()
		if not reply or not reply.file:
			return
		file = io.BytesIO()
		file.name = reply.file.name or f"{reply.file.id}{reply.file.ext}"
		await message.client.download_file(reply, file)
		file.seek(0)
		await message.client.send_file("me", file, force_document=True)
