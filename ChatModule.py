# friendly-telegram

from asyncio import sleep
from os import remove
from telethon.tl.functions.channels import LeaveChannelRequest, \
    InviteToChannelRequest
from telethon.errors import UserIdInvalidError, UserNotMutualContactError, \
    UserPrivacyRestrictedError, \
    BotGroupsBlockedError, ChannelPrivateError, YouBlockedUserError, \
    MessageTooLongError, \
    UserBlockedError, ChatAdminRequiredError, UserKickedError, \
    InputUserDeactivatedError, ChatWriteForbiddenError, \
    UserAlreadyParticipantError
from telethon.tl.types import ChannelParticipantCreator, \
    ChannelParticipantsAdmins, PeerChat, ChannelParticipantsBots
from telethon.tl.functions.messages import AddChatUserRequest
from telethon.tl.functions.messages import GetCommonChatsRequest
from telethon.tl.functions.users import GetFullUserRequest
from telethon import functions
import asyncio
from telethon import errors
from .. import loader, utils
import io


@loader.tds
class ChatMod(loader.Module):
    """Чат модуль"""
    strings = {'name': 'Chat Tools'}

    async def client_ready(self, client, db):
        self.db = db

    async def useridcmd(self, message):
        """Команда .userid <@ или реплай> показывает ID выбранного пользователя."""
        args = utils.get_args_raw(message)
        reply = await message.get_reply_message()

        try:
            if args:
                user = await message.client.get_entity(
                    args if not args.isdigit() else int(args))
            else:
                user = await message.client.get_entity(reply.sender_id)
        except ValueError:
            user = await message.client.get_entity(message.sender_id)

        await message.edit(f"<b>Имя:</b> <code>{user.first_name}</code>\n"
                           f"<b>ID:</b> <code>{user.id}</code>")

    async def chatidcmd(self, message):
        """Команда .chatid показывает ID чата."""
        if not message.is_private:
            args = utils.get_args_raw(message)
            to_chat = None

            try:
                if args:
                    to_chat = args if not args.isdigit() else int(args)
                else:
                    to_chat = message.chat_id

            except ValueError:
                to_chat = message.chat_id

            chat = await message.client.get_entity(to_chat)

            await message.edit(f"<b>Название:</b> <code>{chat.title}</code>\n"
                               f"<b>ID</b>: <code>{chat.id}</code>")
        else:
            return await message.edit("<b>Это не чат!</b>")

    async def invitecmd(self, message):
        """Используйте .invite <@ или реплай>, чтобы добавить пользователя в чат."""
        if message.is_private:
            return await message.edit("<b>Это не чат!</b>")

        args = utils.get_args_raw(message)
        reply = await message.get_reply_message()

        if not args and not reply:
            return await message.edit("<b>Нет аргументов или реплая.</b>")

        try:
            if args:
                user = args if not args.isdigit() else int(args)
            else:
                user = reply.sender_id

            user = await message.client.get_entity(user)

            if not message.is_channel and message.is_group:
                await message.client(AddChatUserRequest(chat_id=message.chat_id,
                                                        user_id=user.id,
                                                        fwd_limit=1000000))
            else:
                await message.client(
                    InviteToChannelRequest(channel=message.chat_id,
                                           users=[user.id]))
            return await message.edit("<b>Пользователь приглашён успешно!</b>")

        except ValueError:
            m = "<b>Неверный @ или ID.</b>"
        except UserIdInvalidError:
            m = "<b>Неверный @ или ID.</b>"
        except UserPrivacyRestrictedError:
            m = "<b>Настройки приватности пользователя не позволяют пригласить его.</b>"
        except UserNotMutualContactError:
            m = "<b>Настройки приватности пользователя не позволяют пригласить его.</b>"
        except ChatAdminRequiredError:
            m = "<b>У меня нет прав.</b>"
        except ChatWriteForbiddenError:
            m = "<b>У меня нет прав.</b>"
        except ChannelPrivateError:
            m = "<b>У меня нет прав.</b>"
        except UserKickedError:
            m = "<b>Пользователь кикнут из чата, обратитесь к администраторам.</b>"
        except BotGroupsBlockedError:
            m = "<b>Бот заблокирован в чате, обратитесь к администраторам.</b>"
        except UserBlockedError:
            m = "<b>Пользователь заблокирован в чате, обратитесь к администраторам.</b>"
        except InputUserDeactivatedError:
            m = "<b>Аккаунт пользователя удалён.</b>"
        except UserAlreadyParticipantError:
            m = "<b>Пользователь уже в группе.</b>"
        except YouBlockedUserError:
            m = "<b>Вы заблокировали этого пользователя.</b>"
        return await message.reply(m)

    async def leavecmd(self, message):
        """Используйте команду .leave, чтобы кикнуть себя из чата."""
        args = utils.get_args_raw(message)
        if not message.is_private:
            if args:
                await message.edit(f"<b>До связи.\nПричина: {args}</b>")
            else:
                await message.edit("<b>До связи.</b>")
            await message.client(LeaveChannelRequest(message.chat_id))
        else:
            return await message.edit("<b>Это не чат!</b>")

    async def userscmd(self, message):
        """Команда .users <имя>; ничего выводит список всех пользователей в чате."""
        if not message.is_private:
            await message.edit("<b>Считаем...</b>")
            args = utils.get_args_raw(message)
            info = await message.client.get_entity(message.chat_id)
            title = info.title or "этом чате"

            if not args:
                users = await message.client.get_participants(message.chat_id)
                mentions = f"<b>Пользователей в \"{title}\": {len(users)}</b> \n"
            else:
                users = await message.client.get_participants(message.chat_id,
                                                              search=f"{args}")
                mentions = f'<b>В чате "{title}" найдено {len(users)} пользователей с именем {args}:</b> \n'

            for user in users:
                if not user.deleted:
                    mentions += f"\n• <a href =\"tg://user?id={user.id}\">{user.first_name}</a> | <code>{user.id}</code>"
                else:
                    mentions += f"\n• Удалённый аккаунт <b>|</b> <code>{user.id}</code>"

            try:
                await message.edit(mentions)
            except MessageTooLongError:
                await message.edit(
                    "<b>Черт, слишком большой чат. Загружаю список пользователей в файл...</b>")
                file = open("userslist.md", "w+")
                file.write(mentions)
                file.close()
                await message.client.send_file(message.chat_id,
                                               "userslist.md",
                                               caption="<b>Пользователей в {}:</b>".format(
                                                   title),
                                               reply_to=message.id)
                remove("userslist.md")
                await message.delete()
        else:
            return await message.edit("<b>Это не чат!</b>")

    async def adminscmd(self, message):
        """Команда .admins показывает список всех админов в чате."""
        if not message.is_private:
            await message.edit("<b>Считаем...</b>")
            info = await message.client.get_entity(message.chat_id)
            title = info.title or "this chat"

            admins = await message.client.get_participants(message.chat_id,
                                                           filter=ChannelParticipantsAdmins)
            mentions = f"<b>Админов в \"{title}\": {len(admins)}</b>\n"

            for user in admins:
                admin = admins[admins.index(
                    (await message.client.get_entity(user.id)))].participant
                if not admin:
                    if type(admin) == ChannelParticipantCreator:
                        rank = "creator"
                    else:
                        rank = "admin"
                else:
                    rank = admin.rank or "admin"

                if not user.deleted:
                    mentions += f"\n• <a href=\"tg://user?id={user.id}\">{user.first_name}</a> | {rank} | <code>{user.id}</code>"
                else:
                    mentions += f"\n• Удалённый аккаунт <b>|</b> <code>{user.id}</code>"

            try:
                await message.edit(mentions)
            except MessageTooLongError:
                await message.edit(
                    "Черт, слишком много админов здесь. Загружаю список админов в файл...")
                file = open("adminlist.md", "w+")
                file.write(mentions)
                file.close()
                await message.client.send_file(message.chat_id,
                                               "adminlist.md",
                                               caption="<b>Админов в \"{}\":<b>".format(
                                                   title),
                                               reply_to=message.id)
                remove("adminlist.md")
                await message.delete()
        else:
            return await message.edit("<b>Это не чат!</b>")

    async def botscmd(self, message):
        """Команда .bots показывает список всех ботов в чате."""
        if not message.is_private:
            await message.edit("<b>Считаем...</b>")

            info = await message.client.get_entity(message.chat_id)
            title = info.title if info.title else "this chat"

            bots = await message.client.get_participants(message.to_id,
                                                         filter=ChannelParticipantsBots)
            mentions = f"<b>Ботов в \"{title}\": {len(bots)}</b>\n"

            for user in bots:
                if not user.deleted:
                    mentions += f"\n• <a href=\"tg://user?id={user.id}\">{user.first_name}</a> | <code>{user.id}</code>"
                else:
                    mentions += f"\n• Удалённый бот <b>|</b> <code>{user.id}</code> "

            try:
                await message.edit(mentions, parse_mode="html")
            except MessageTooLongError:
                await message.edit("Черт, слишком много ботов здесь. Загружаю "
                                   "список ботов в файл...")
                file = open("botlist.md", "w+")
                file.write(mentions)
                file.close()
                await message.client.send_file(message.chat_id,
                                               "botlist.md",
                                               caption="<b>Ботов в \"{}\":</b>".format(
                                                   title),
                                               reply_to=message.id)
                remove("botlist.md")
                await message.delete()
        else:
            return await message.edit("<b>Это не чат!</b>")

    async def commoncmd(self, message):
        """Используй .common <@ или реплай>, чтобы узнать общие чаты с
        пользователем. """
        args = utils.get_args_raw(message)
        reply = await message.get_reply_message()
        if not args and not reply:
            return await message.edit('<b>Нет аргументов или реплая.</b>')
        await message.edit('<b>Считаем...</b>')
        try:
            if args:
                if args.isnumeric():
                    user = int(args)
                    user = await message.client.get_entity(user)
                else:
                    user = await message.client.get_entity(args)
            else:
                user = await utils.get_user(reply)
        except ValueError:
            return await message.edit('<b>Не удалось найти пользователя.</b>')
        msg = f'<b>Общие чаты с {user.first_name}:</b>\n'
        user = await message.client(GetFullUserRequest(user.id))
        comm = await message.client(
            GetCommonChatsRequest(user_id=user.user.id, max_id=0, limit=100))
        count = 0
        m = ''
        for chat in comm.chats:
            m += f'\n• <a href="tg://resolve?domain={chat.username}">{chat.title}</a> <b>|</b> <code>{chat.id}</code> '
            count += 1
        msg = f'<b>Общие чаты с {user.user.first_name}: {count}</b>\n'
        await message.edit(f'{msg} {m}')

    async def chatdumpcmd(self, message):
        """.chatdump <n> <m> <s>
            Дамп юзеров чата
            <n> - Получить только пользователей с открытыми номерами
            <m> - Отправить дамп в избранное
            <s> - Тихий дамп
        """
        if not message.chat:
            await message.edit("<b>Это не чат</b>")
            return
        chat = message.chat
        num = False
        silent = False
        tome = False
        if utils.get_args_raw(message):
            a = utils.get_args_raw(message)
            if "n" in a:
                num = True
            if "s" in a:
                silent = True
            if "m" in a:
                tome = True
        if not silent:
            await message.edit("🖤Дампим чат...🖤")
        else:
            await message.delete()
        f = io.BytesIO()
        f.name = f'Dump by {chat.id}.csv'
        f.write("FNAME;LNAME;USER;ID;NUMBER\n".encode())
        me = await message.client.get_me()
        for i in await message.client.get_participants(message.to_id):
            if i.id == me.id: continue
            if num:
                if i.phone:
                    f.write(
                        f"{str(i.first_name)};{str(i.last_name)};{str(i.username)};{str(i.id)};{str(i.phone)}\n".encode())
            else:
                f.write(
                    f"{str(i.first_name)};{str(i.last_name)};{str(i.username)};{str(i.id)};{str(i.phone)}\n".encode())
        f.seek(0)
        if tome:
            await message.client.send_file('me', f,
                                           caption="Дамп чата " + str(chat.id))
        else:
            await message.client.send_file(message.to_id, f, caption="Дамп "
                                                                     "чата "
                                                                     + str(
                chat.id))
        if not silent:
            if tome:
                if num:
                    await message.edit("🖤Дамп юзеров чата сохранён в "
                                       "избранных!🖤")
                else:
                    await message.edit("🖤Дамп юзеров чата с открытыми "
                                       "номерами сохранён в избранных!🖤")
            else:
                await message.delete()
        f.close()

    async def adduserscmd(self, event):
        """Add members"""
        if len(event.text.split()) == 2:
            idschannelgroup = event.text.split(" ", maxsplit=1)[1]
            user = [i async for i in
                    event.client.iter_participants(event.to_id.channel_id)]
            await event.edit(
                f"<b>{len(user)} пользователей будет приглашено из чата {event.to_id.channel_id} в чат/канал {idschannelgroup}</b>")
            for u in user:
                try:
                    try:
                        if u.bot == False:
                            await event.client(
                                functions.channels.InviteToChannelRequest(
                                    idschannelgroup, [u.id]))
                            await asyncio.sleep(1)
                        else:
                            pass
                    except:
                        pass
                except errors.FloodWaitError as e:
                    print('Flood for', e.seconds)
        else:
            await event.edit(f"<b>Куда приглашать будем?</b>")

    async def reportcmd(self, message):
        """Репорт пользователя за спам."""
        args = utils.get_args_raw(message)
        reply = await message.get_reply_message()
        if args:
            user = await message.client.get_entity(
                args if not args.isnumeric() else int(args))
        if reply:
            user = await message.client.get_entity(reply.sender_id)
        else:
            return await message.edit("<b>Кого я должен зарепортить?</b>")

        await message.client(functions.messages.ReportSpamRequest(peer=user.id))
        await message.edit("<b>Ты получил репорт за спам!</b>")
        await sleep(1)
        await message.delete()

    async def echocmd(self, message):
        """Активировать/деактивировать Echo."""
        echos = self.db.get("Echo", "chats", [])
        chatid = str(message.chat_id)

        if chatid not in echos:
            echos.append(chatid)
            self.db.set("Echo", "chats", echos)
            return await message.edit(
                "<b>[Echo Mode]</b> Активирован в этом чате!")

        echos.remove(chatid)
        self.db.set("Echo", "chats", echos)
        return await message.edit(
            "<b>[Echo Mode]</b> Деактивирован в этом чате!")

    async def delmecmd(self, message):
		"""Удаляет все сообщения от тебя"""
		chat = message.chat
		if chat:
			args = utils.get_args_raw(message)
			if args != str(message.chat.id+message.sender_id):
				await message.edit(f"<b>Если ты точно хочешь это сделать, то напиши:</b>\n<code>.delme {message.chat.id+message.sender_id}</code>")
				return
			all = (await self.client.get_messages(chat, from_user="me")).total
			messages = [msg async for msg in self.client.iter_messages(chat, from_user="me")]
			await message.edit(f"<b>{all} сообщений будет удалено!</b>")
			_ = ""
			async for msg in self.client.iter_messages(chat, from_user="me"):
				if _:
					await msg.delete()
				else:
					_ = "_"
			await message.delete()
		else:
			await message.edit("<b>В лс не чищу!</b>")
			
    async def watcher(self, message):
        echos = self.db.get("Echo", "chats", [])
        chatid = str(message.chat_id)

        if chatid not in str(echos): return
        if message.sender_id == (await message.client.get_me()).id: return

        await message.client.send_message(int(chatid), message,
                                          reply_to=await message.get_reply_message() or message)

