# Thanks Full To Team Ultroid
# Ported By @skyzu
# from github.com/vckyou/geez-userbot
# Recode Ramadhani892

from telethon.tl.functions.channels import GetFullChannelRequest as getchat
from telethon.tl.functions.phone import CreateGroupCallRequest as startvc
from telethon.tl.functions.phone import DiscardGroupCallRequest as stopvc
from telethon.tl.functions.phone import GetGroupCallRequest as getvc
from telethon.tl.functions.phone import InviteToGroupCallRequest as invitetovc

from userbot import CMD_HELP
from userbot.events import register

NO_ADMIN = "`Maaf Kamu Bukan Admin!"


def vcmention(user):
    full_name = get_display_name(user)
    if not isinstance(user, types.User):
        return full_name
    return f"[{full_name}](tg://user?id={user.id})"


async def get_call(rambot):
    kyura = await rambot.client(getchat(rambot.chat_id))
    hehe = await rambot.client(getvc(kyura.full_chat.call))
    return hehe.call


def user_list(l, n):
    for i in range(0, len(l), n):
        yield l[i : i + n]


@register(outgoing=True, pattern=r"^\.startvc$", groups_only=True)
async def start_voice(kyura):
    chat = await kyura.get_chat()
    admin = chat.admin_rights
    creator = chat.creator

    if not admin and not creator:
        return await kyura.edit(NO_ADMIN)
    try:
        await kyura.client(startvc(kyura.chat_id))
        await kyura.edit("`Voice Chat Started...`")
    except Exception as ex:
        await kyura.edit(f"`{str(ex)}`")


@register(outgoing=True, pattern=r"^\.stopvc$", groups_only=True)
async def stop_voice(hmm):
    chat = await hmm.get_chat()
    admin = chat.admin_rights
    creator = chat.creator

    if not admin and not creator:
        return await hmm.edit(NO_ADMIN)
    try:
        await hmm.client(stopvc(await get_call(hmm)))
        await hmm.edit("`Voice Chat Stopped...`")
    except Exception as ex:
        await hmm.edit(f"`{str(ex)}`")


@register(outgoing=True, pattern=r"^\.vcinvite", groups_only=True)
async def vc_invite(td):
    await td.edit("`Sedang Mengivinte Member...`")
    users = []
    z = 0
    async for x in td.client.iter_participants(td.chat_id):
        if not x.bot:
            users.append(x.id)
    hmm = list(user_list(users, 6))
    for p in hmm:
        try:
            await td.client(invitetovc(call=await get_call(td), users=p))
            z += 6
        except BaseException:
            pass
    await td.edit(f"`Invited {z} users`")


CMD_HELP.update(
    {
        "vcg": "𝘾𝙤𝙢𝙢𝙖𝙣𝙙: `.startvc`\
         \n↳ : Start Group Call in a group.\
         \n𝘾𝙤𝙢𝙢𝙖𝙣𝙙: `.stopvc`\
         \n↳ : `Stop Group Call in a group.`\
         \n𝘾𝙤𝙢𝙢𝙖𝙣𝙙: `.vcinvite`\
         \n↳ : Invite all members of group in Group Call. (You must be joined)."
    }
)
