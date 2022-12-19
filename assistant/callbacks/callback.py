"""
This file is for inline help menu.
"""

import struct
import base64

from pyrogram import filters
from pyrogram.errors import PeerIdInvalid

from pyrogram.types import (
    InputMediaPhoto,
    InlineKeyboardButton,
    InlineKeyboardMarkup,
    CallbackQuery
)

from deadly.client import app

# anime-quote
@app.bot.on_callback_query(filters.regex("animequote-tab"))
async def _anime_quotes(_, cb: CallbackQuery):
    await cb.edit_message_text(
        app.quote(),
        reply_markup=InlineKeyboardMarkup(
            [
                [
                    InlineKeyboardButton(
                        text="More",
                        callback_data="animequote-tab",
                    )
                ]
            ]
        ),
    )


# assistant 
@app.bot.on_callback_query(filters.regex("assistant-tab"))
@app.alert_user
async def _assistant(_, cb: CallbackQuery):
    await cb.edit_message_media(
        media=InputMediaPhoto(
            media="assets/images/Laky.jpg", 
            caption=app.assistant_tab_string()
        ),
        reply_markup=InlineKeyboardMarkup(
            [
                app.bot.BuildKeyboard(
                    (
                        ["Home", "close-tab"],
                        ["Back", "home-tab"]
                    )
                )
            ]
        )
    )


# close 
@app.bot.on_callback_query(filters.regex("close-tab"))
@app.alert_user
async def _close(_, cb: CallbackQuery):
    await cb.edit_message_media(
        media=InputMediaPhoto(
            media="assets/images/DeadlyUserbot.jpg", 
            caption=app.close_tab_string()
        ),
        reply_markup=InlineKeyboardMarkup(
            [
                [
                    InlineKeyboardButton(
                        text="Open",
                        callback_data="home-tab"
                    )
                ],
                [
                    InlineKeyboardButton(
                        text="Delete",
                        callback_data="delete-tab"
                    )
                ]
            ]
        )
    )


# delete 
@app.bot.on_callback_query(filters.regex("delete-tab"))
@app.alert_user
async def delete_helpdex(_, cb: CallbackQuery):
    """ delete helpdex handler for help plugin """

    try:
        if cb.inline_message_id:
            dc_id, message_id, chat_id, query_id = struct.unpack(
                "<iiiq",
                base64.urlsafe_b64decode(
                    cb.inline_message_id + '=' * (len(cb.inline_message_id) % 4)
                )
            )

            await app.delete_messages(
                chat_id=int(str(-100) + str(chat_id)[1:]),
                message_ids=message_id
            )
        elif not cb.inline_message_id:
            if cb.message:
                await cb.message.delete()
        else:
            await cb.answer(
                "Message Expired !",
                show_alert=True
            )

    except (PeerIdInvalid, KeyError, ValueError):
        await app.delete_messages(
            chat_id=chat_id,
            message_ids=message_id
        )
        print(chat_id, message_id)
    except Exception as e:
        await app.error(e)

# extra

@app.bot.on_callback_query(filters.regex("extra-tab"))
@app.alert_user
async def _extra(_, cb: CallbackQuery):
    await cb.edit_message_text(
        text=app.extra_tab_string(),
        reply_markup=InlineKeyboardMarkup(
            [
                [
                    InlineKeyboardButton(
                        text="• Public commands •",
                        callback_data="ubpublic-commands-tab"
                    )
                ],
                [
                    InlineKeyboardButton(
                        text="Home",
                        callback_data="close-tab"
                    ),
                    InlineKeyboardButton(
                        text="Back",
                        callback_data="home-tab"
                    )
                ]
            ]
        )
    )
    print(cb)


# home
@app.bot.on_callback_query(filters.regex("home-tab"))
@app.alert_user
async def _start(_, cb: CallbackQuery):
    await cb.edit_message_media(
        media=InputMediaPhoto(media=app.BotPic(), caption=app.home_tab_string()),
        reply_markup=InlineKeyboardMarkup([
                app.BuildKeyboard(
                    (
                        ["๏ Settings ๏", "settings-tab"],
                        ["๏ Plugins ๏", "plugins-tab"]
                    )
                ),
                app.BuildKeyboard(
                    (
                        ["๏ Extra ๏", "extra-tab"],
                        ["๏ Stats ๏", "stats-tab"]
                    )
                ),
                app.BuildKeyboard(([["About", "about-tab"]])),
                app.BuildKeyboard(([["Close", "close-tab"]]))
        ]
        ),
    )


# plugin-page
@app.bot.on_callback_query(filters.regex("plugins-tab"))
@app.alert_user
async def plugins_page(_, cb: CallbackQuery):
    btn = app.HelpDex(0, app.CMD_HELP, "navigate")
    await cb.edit_message_text(
        text=app.plugin_tab_string(),
        reply_markup=InlineKeyboardMarkup(btn)
    )


# next page
@app.bot.on_callback_query(filters.regex(pattern="navigate-next\((.+?)\)"))
@app.alert_user
async def give_next_page(_, cb: CallbackQuery):
    current_page_number = int(cb.matches[0].group(1))
    btn = app.HelpDex(current_page_number + 1, app.CMD_HELP, "navigate")
    print(cb.matches[0])
    print(dir(cb.matches[0]))
    await cb.edit_message_reply_markup(reply_markup=InlineKeyboardMarkup(btn))


# previous page
@app.bot.on_callback_query(filters.regex(pattern="navigate-prev\((.+?)\)"))
@app.alert_user
async def give_old_page(_, cb: CallbackQuery):
    current_page_number = int(cb.matches[0].group(1))
    btn = app.HelpDex(current_page_number - 1, app.CMD_HELP, "navigate")
    await cb.edit_message_reply_markup(reply_markup=InlineKeyboardMarkup(btn))


# back from plugin dex to home
@app.bot.on_callback_query(filters.regex(pattern="back-to-plugins-page-(.*)"))
@app.alert_user
async def get_back(_, cb: CallbackQuery):
    page_number = int(cb.matches[0].group(1))
    btn = app.HelpDex(page_number, app.CMD_HELP, "navigate")
    await cb.edit_message_text(text=app.plugin_tab_string(), reply_markup=InlineKeyboardMarkup(btn))


# plugin page information
@app.bot.on_callback_query(filters.regex(pattern="pluginlist-(.*)"))
@app.alert_user
async def give_plugin_cmds(_, cb: CallbackQuery):
    plugin_name, page_number = cb.matches[0].group(1).split("|", 1)
    plugs = await app.PluginData(plugin_name)
    cmd_string = f"**PLUGIN:** {plugin_name}\n\n" + "".join(plugs)
    await cb.edit_message_text(
        cmd_string,
        reply_markup=InlineKeyboardMarkup(
            [
                [
                    InlineKeyboardButton(
                        text="Back",
                        callback_data=f"back-to-plugins-page-{page_number}",
                    )
                ]
            ]
        ),
        )


# public-page
@app.bot.on_callback_query(filters.regex("ubpublic-commands-tab"))
@app.alert_user
async def _public_commands(_, cb: CallbackQuery):
    await cb.edit_message_text(
        text=app.public_tab_string(),
        reply_markup=InlineKeyboardMarkup(
            [
                [
                    InlineKeyboardButton(
                        text="Back",
                        callback_data="extra-tab"
                    )
                ]
            ]
        )
    )





@app.bot.on_callback_query(filters.regex("public-commands-tab"))
async def _global_commands(_, cb):
    await cb.edit_message_text(
        text=app.public_tab_string(),
        reply_markup=InlineKeyboardMarkup(
            [
                [
                    InlineKeyboardButton(
                        text="Back",
                        callback_data="back-to-public"
                    )
                ]
            ]
        )
    )


@app.bot.on_callback_query(filters.regex("back-to-public"))
async def _back_to_info(_, cb):
    await cb.edit_message_text(
        text="You can use these public commands, check below.",
        reply_markup=InlineKeyboardMarkup(
            [
                [
                    InlineKeyboardButton(
                        text="• View commands •",
                        callback_data="public-commands-tab"
                    )
                ]
            ]
        )
    )

# restart-page
@app.bot.on_callback_query(filters.regex("restart-tab"))
@app.alert_user
async def _restart_userbot(_, cb: CallbackQuery):
    await cb.edit_message_text(
        text=app.restart_tab_string("`Press confirm to restart.`"),
        reply_markup=InlineKeyboardMarkup(
            [
                [
                    InlineKeyboardButton(
                        text="Confirm",
                        callback_data="confirm-restart-tab"
                    )
                ],
                [
                    InlineKeyboardButton(
                        text="Home",
                        callback_data="close-tab"
                    ),
                    InlineKeyboardButton(
                        text="Back",
                        callback_data="settings-tab"
                    )
                ]
            ]
        ),
    )


@app.bot.on_callback_query(filters.regex("confirm-restart-tab"))
@app.alert_user
async def _confirm_restart(_, cb: CallbackQuery):
    try:
        back_button = InlineKeyboardMarkup(
            [
                [
                    InlineKeyboardButton(
                        text="Back",
                        callback_data="settings-tab"
                    )
                ]
            ]
        )

        await cb.edit_message_text(
            text=app.restart_tab_string("`Trying to restart DeadlyUserbot . . .`"),
            reply_markup=back_button
        )
        if not app.heroku_app():
            await cb.edit_message_text(
                text=app.restart_tab_string("`Heroku requirements missing (heroku - key, app name), restart manually . . .`"),
                reply_markup=back_button
            )
        else:
            res = app.heroku_app().restart()
            text = "`Please wait 2-3 minutes to restart userbot . . .`"
            final_text = text if res else "`Failed to restart userbot, do it manually . . .`"
            await cb.edit_message_text(
                text=app.restart_tab_string(final_text),
                reply_markup=back_button
            )
    except Exception as e:
        print(e)
        await app.error(e)

# settings-page
@app.bot.on_callback_query(filters.regex("settings-tab"))
@app.alert_user
async def _settings(_, cb: CallbackQuery):
    await cb.edit_message_text(
        text=app.settings_tab_string(),
        reply_markup=InlineKeyboardMarkup(
            [
                [
                    InlineKeyboardButton(
                        "Restart bot", callback_data="restart-tab",
                    ),
                ],
                [
                    InlineKeyboardButton(
                        "Shutdown bot", callback_data="shutdown-tab",
                    )
                ],
                [
                    InlineKeyboardButton(
                        "Update bot", callback_data="update-tab",
                    )
                ],
                app.BuildKeyboard((["Home", "close-tab"], ["Back", "home-tab"])),
            ]
        ),
    )

# shutdowm-page
@app.bot.on_callback_query(filters.regex("shutdown-tab"))
@app.alert_user
async def _shutdown_tron(_, cb: CallbackQuery):
    await cb.edit_message_text(
        text=app.shutdown_tab_string("`Press confirm to shutdown userbot.`"),
        reply_markup=InlineKeyboardMarkup(
            [
                [
                    InlineKeyboardButton(
                        text="Confirm",
                        callback_data="confirm-shutdown"
                    )
                ],
                [
                    InlineKeyboardButton(
                        text="Home",
                        callback_data="close-tab"
                    ),
                    InlineKeyboardButton(
                        text="Back",
                        callback_data="settings-tab"
                    )
                ]
            ]
        )
    )


@app.bot.on_callback_query(filters.regex("confirm-shutdown"))
@app.alert_user
async def _shutdown_core(_, cb):
    back_button=InlineKeyboardMarkup(
        [
            [
                InlineKeyboardButton(
                    text="Back",
                    callback_data="settings-tab"
                )
            ]
        ]
    )

    await cb.edit_message_text(
        text=app.shutdown_tab_string("`Trying to shutdown DeadlyUserbot . . .`"),
        reply_markup=back_button
    )

    if not app.heroku_app():
        await cb.edit_message_text(
            text=app.shutdown_tab_string("`Failed to shutdown userbot . . .`"),
            reply_markup=back_button
        )
    else:
        res = app.heroku_app().process_formation()["worker"].scale(0)
        process = "Successfully" if res else "Unsuccessfully"
        await cb.edit_message_text(
            text=app.shutdown_tab_string(f"`Shutdown {process} . . .`"),
            reply_markup=back_button
        )

# stats-page
@app.bot.on_callback_query(filters.regex("stats-tab"))
@app.alert_user
async def _stats(_, cb: CallbackQuery):
    await cb.edit_message_text(
        text=app.stats_tab_string(),
        reply_markup=InlineKeyboardMarkup(
            [
                app.BuildKeyboard((["Home", "close-tab"], ["Back", "home-tab"]))
            ]
        ),
    )

#update-page
@app.bot.on_callback_query(filters.regex("update-tab"))
@app.alert_user
async def _update_callback(_, cb: CallbackQuery):
    await cb.answer(
            text="This feature is not added yet.",
            show_alert=True
        )
