from pyrogram.types import InlineKeyboardButton, InlineKeyboardMarkup

from deadly import app, gen

@app.on_message(gen("kboard", allow=["sudo"]))
async def create_keyboard(_, m):
    await m.delete()
    if m.chat.type == "bot":
        return await app.send_edit(
            m, "Sorry you can't use it here", delme=4, text_type=["mono"]
        )

    if not app.user_exists(app.bot.id, m.chat.id):
        return await app.send_edit(
            m, "Your bot is not present in this group.", text_type=["mono"], delme=4
        )

    if app.long(m) >= 3:
        await app.bot.send_message(
            m.chat.id,
            m.text.split(None, 3)[3],
            reply_markup=InlineKeyboardMarkup(
                [
                    [
                        InlineKeyboardButton(m.command[1], url=m.command[2]),
                    ],
                ]
            ),
        )
    else:
        await app.send_edit(
            m, f"`{app.PREFIX}kbd [ Button text ] [ Button url ] [ Text ]`"
        ) 
    except Exception as e:
        await app.error(e)
