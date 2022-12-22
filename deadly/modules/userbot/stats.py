
""" stats plugin """

from datetime import datetime

from pyrogram.types import Message
from pyrogram.enums import ChatType

from deadly import app, gen




app.CMD_HELP.update(
    {"stats": (
        "stats",
        {
        "stats" : "Get information about how many groups/channels/users you have in your dialogs."
        }
        )
    }
)



@app.on_message(gen("stats"))
async def stats(client, message):
    """ dialogstats handler for stats plugin """
    try:
        start = datetime.now()
        await app.send_edit("Getting stats . . .", text_type=["mono"])

        bot = 0
        user = 0
        group = 0
        channel = 0
        admin = 0
        supergroup = 0
        stats_format = """
`Your Stats Obtained in {} seconds`\n\n
`You have {} Private Messages.`\n
`You are in {} Groups.`\n
`You are in {} Super Groups.`\n
`You Are in {} Channels.`\n
`You Are Admin in {} Chats.`\n
`Bots = {}`\n\n
Powered by @DeadlyUserbot
"""

        async for dialog in client.get_dialogs():
            if dialog.chat.type == "channel":
                channel += 1
            elif dialog.chat.type == "bot":
                bot += 1
            elif dialog.chat.type == "group":
                group += 1
            elif dialog.chat.type == "supergroup":
                supergroup += 1
                user_s = await dialog.chat.get_member(int(client.me.id))
                if user_s.status in ("creator", "administrator"):
                    admin += 1
            elif dialog.chat.type == "private":
                user += 1
        end = datetime.now()
        ms = (end - start).seconds     
        await app.send_edit(stats_format.format(ms, user, group, supergroup, channel, admin, bot))
    except Exception as e:
        await app.error(e)
