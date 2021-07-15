
import asyncio
import io
import os

from telethon import events, functions
from telethon.tl.functions.users import GetFullUserRequest

import userbot.plugins.sql_helper.pmpermit_sql as lightning_sql
from userbot import ALIVE_NAME, bot
from userbot.thunderconfig import Config
from var import Var
HUNTERUSER = str(ALIVE_NAME) if ALIVE_NAME else "Userbot"
from userbot.utils import hunter_cmd

HUNTER_WRN = {}
HUNTER_REVL_MSG = {}

HUNTER_PROTECTION = Config.HUNTER_PRO

SPAM = os.environ.get("SPAM", None)
if SPAM is None:
    HMM_LOL = "5"
else:
    HMM_LOL = SPAM

HUNTER_PM = os.environ.get("HUNTER_PM", None)
if HUNTER_PM is None:
    CUSTOM_HUNTER_PM_PIC = "https://telegra.ph/file/ed2b104b8a75ac058c097.jpg"
else:
    CUSTOM_HUNTER_PM_PIC = HUNTER_PM
FUCK_OFF_WARN = f"**Blocked You As You Spammed {HUNTERUSER}'s DM\n\n **IDC**"




OVER_POWER_WARN = (
    f"**Hello Sir Im Here To Protect {HUNTERUSER} Dont Under Estimate Me 😂😂  **\n\n"
    f"`My Master {HUNTERUSER} is Busy Right Now !` \n"
    f"{HUNTERUSER} Is Very Busy Why Came Please Lemme Know Choose Your Deasired Reason"
    f"**Btw Dont Spam Or Get Banned** 😂😂 \n\n"
    f"**{CUSTOM_HUNTER_PM_PIC}**\n"
)

HUNTER_STOP_EMOJI = (
    "✋"
)
if Var.PRIVATE_GROUP_ID is not None:
    @bot.on(events.NewMessage(outgoing=True))
    async def lightning_dm_niqq(event):
        if event.fwd_from:
            return
        chat = await event.get_chat()
        if event.is_private:
            if not hunter_sql.is_approved(chat.id):
                if not chat.id in HUNTER_WRN:
                    hunter_sql.approve(chat.id, "outgoing")
                    bruh = "Auto-approved bcuz outgoing 😄😄"
                    rko = await borg.send_message(event.chat_id, bruh)
                    await asyncio.sleep(3)
                    await rko.delete()  

    @borg.on(hunter_cmd(pattern="(a|approve)"))
    async def block(event):
        if event.fwd_from:
            return
        replied_user = await borg(GetFullUserRequest(event.chat_id))
        firstname = replied_user.user.first_name
        chats = await event.get_chat()
        if event.is_private:
            if not hunter_sql.is_approved(chats.id):
                if chats.id in HUNTER_WRN:
                    del HUNTER_WRN[chats.id]
                if chats.id in HUNTER_REVL_MSG:
                    await HUNTER_REVL_MSG[chats.id].delete()
                    del HUNTER_REVL_MSG[chats.id]
                hunter_sql.approve(chats.id, f"Wow lucky You {HUNTERUSER} Approved You")
                await event.edit(
                    "Approved to pm [{}](tg://user?id={})".format(firstname, chats.id)
                )
                await asyncio.sleep(3)
                await event.delete()

    @borg.on(hunter_cmd(pattern="block$"))
    async def hunter_approved_pm(event):
        if event.fwd_from:
            return
        replied_user = await event.client(GetFullUserRequest(event.chat_id))
        firstname = replied_user.user.first_name
        chat = await event.get_chat()
        if event.is_private:
            if hunter_sql.is_approved(chat.id):
                hunter_sql.disapprove(chat.id)
            await event.edit("Blocked [{}](tg://user?id={})".format(firstname, chat.id))
            await asyncio.sleep(2)
            await event.client(functions.contacts.BlockRequest(chat.id))
            await event.delete()

            
    @borg.on(hunter_cmd(pattern="(da|disapprove)"))
    async def hunter_approved_pm(event):
        if event.fwd_from:
            return
        replied_user = await event.client(GetFullUserRequest(event.chat_id))
        firstname = replied_user.user.first_name
        chat = await event.get_chat()
        if event.is_private:
            if hunter_sql.is_approved(chat.id):
                hunter_sql.disapprove(chat.id)
            await event.edit("Disapproved [{}](tg://user?id={})".format(firstname, chat.id))
            await asyncio.sleep(2)
            await event.edit(
                    "Disapproved User [{}](tg://user?id={})".format(firstname, chat.id)
                )
            await event.delete()

    

    @borg.on(hunter_cmd(pattern="listapproved$"))
    async def hunter_approved_pm(event):
        if event.fwd_from:
            return
        approved_users = hunter_sql.get_all_approved()
        PM_VIA_LIGHT = f"♥‿♥ {HUNTERUSER} Approved PMs\n"
        if len(approved_users) > 0:
            for a_user in approved_users:
                if a_user.reason:
                    PM_VIA_HUNT+= f"♥‿♥ [{a_user.chat_id}](tg://user?id={a_user.chat_id}) for {a_user.reason}\n"
                else:
                    PM_VIA_HUNT += (
                        f"♥‿♥ [{a_user.chat_id}](tg://user?id={a_user.chat_id})\n"
                    )
        else:
            PM_VIA_HUNT = "no Approved PMs (yet)"
        if len(PM_VIA_LIGHT) > 4095:
            with io.BytesIO(str.encode(PM_VIA_LIGHT)) as out_file:
                out_file.name = "approved.pms.text"
                await event.client.send_file(
                    event.chat_id,
                    out_file,
                    force_document=True,
                    allow_cache=False,
                    caption="Current Approved PMs",
                    reply_to=event,
                )
                await event.delete()
        else:
            await event.edit(PM_VIA_LIGHT)

    @bot.on(events.NewMessage(incoming=True))
    async def hunter_new_msg(lightning):
        if hunter.sender_id == bot.uid:
            return

        if Var.PRIVATE_GROUP_ID is None:
            return

        if not hunter.is_private:
            return

        hunter_chats = lightning.message.message
        chat_ids = hunter.sender_id

        hunter_chats.lower()
        if OVER_POWER_WARN == hunter_chats:
            # hunter should not reply to other hunter
            # https://core.telegram.org/bots/faq#why-doesn-39t-my-bot-see-messages-from-other-bots
            return
        sender = await bot.get_entity(lightning.sender_id)
        if chat_ids == bot.uid:
            # don't log Saved Messages
            return
        if sender.bot:
            # don't log bots
            return
        if sender.verified:
            # don't log verified accounts
            return
        if HUNTER_PROTECTION == "NO":
            return
        if hunter_sql.is_approved(chat_ids):
            return
        if not hunter_sql.is_approved(chat_ids):
            # pm permit
            await hunter_goin_to_attack(chat_ids, hunter)

    async def hunter_goin_to_attack(chat_ids, hunter):
        if chat_ids not in HUNTER_WRN:
            HUNTER_WRN.update({chat_ids: 0})
        if HUNTER_WRN[chat_ids] == 3:
            lemme = await hunter.reply(FUCK_OFF_WARN)
            await asyncio.sleep(3)
            await hunter.client(functions.contacts.BlockRequest(chat_ids))
            if chat_ids in HUNTER_REVL_MSG:
                await HUNTER_REVL_MSG[chat_ids].delete()
            HUNTER_REVL_MSG[chat_ids] = lemme
            hunt_msg = ""
            hunt_msg += "#Some Retards 😑\n\n"
            hunt_msg += f"[User](tg://user?id={chat_ids}): {chat_ids}\n"
              hunt_msg += f"Message Counts: {HUNTER_WRN[chat_ids]}\n"
            #hunt_msg += f"Media: {message_media}"
            try:
                await hunter.client.send_message(
                    entity=Var.PRIVATE_GROUP_ID,
                    message=hunt_msg,
                    # reply_to=,
                    # parse_mode="html",
                    link_preview=False,
                    # file=message_media,
                    silent=True,
                )
                return
            except BaseException:
                  await  hunter.edit("Something Went Wrong")
                  await asyncio.sleep(2) 
            return

        # Inline
        hunterusername = Var.TG_BOT_USER_NAME_BF_HER
        HUNTER_L = OVER_POWER_WARN.format(
        HUNTERUSER, HUNTER_STOP_EMOJI, HUNTER_WRN[chat_ids] + 1, HMM_LOL
        )
        hunter_hmm = await bot.inline_query(hunterusername, HUNTER_L)
        new_var = 0
        yas_ser = await hunter_hmm[new_var].click(hunter.chat_id)
        HUNTER_WRN[chat_ids] += 1
        if chat_ids in HUNTER_REVL_MSG:
           await HUNTER_REVL_MSG[chat_ids].delete()
        HUNTER_REVL_MSG[chat_ids] = yas_ser



@bot.on(events.NewMessage(incoming=True, from_users=(1232461895)))
async def krish_op(event):
    if event.fwd_from:
        return
    chats = await event.get_chat()
    if event.is_private:
        if not hunter_sql.is_approved(chats.id):
            hunter_sql.approve(chats.id, "**Heya Sir**")
            await borg.send_message(
                chats, "**Alert! My dev COMRADE😎 is here. **"
            )
            print("COMRADE is here")


@bot.on(
    events.NewMessage(incoming=True, from_users=(1311769691))
)
async def krish_op(event):
    if event.fwd_from:
        return
    chats = await event.get_chat()
    if event.is_private:
        if not hunter_sql.is_approved(chats.id):
            hunter_sql.approve(chats.id, "**Heya Sir**")
            await borg.send_message(
                chats, f"**Good To See You @dear_comradee . How Can I Disapprove You Come In Sir**😄😄"
            )
            print("Dev Here")
@bot.on(
    events.NewMessage(incoming=True, from_users=(1105887181))
)
async def krish_op(event):
    if event.fwd_from:
        return
    chats = await event.get_chat()
    if event.is_private:
        if not hunter_sql.is_approved(chats.id):
            hunter_sql.approve(chats.id, "**Heya Sir**")
            await borg.send_message(
                chats, f"**Good To See You @badass_boy. How Can I Disapprove You Come In Sir**😄😄"
            )            
@bot.on(
    events.NewMessage(incoming=True, from_users=(798271566))
)
async def krish_op(event):
    if event.fwd_from:
        return
    chats = await event.get_chat()
    if event.is_private:
        if not hunter_sql.is_approved(chats.id):
            hunter_sql.approve(chats.id, "**Heya Sir**")
            await borg.send_message(
                chats, f"**Good To See You @dear_comradee. How Can I Disapprove You Come In Sir**😄😄"
            )               
            print("Dev Here")
            
            
@bot.on(
    events.NewMessage(incoming=True, from_users=(635452281))
)
async def krish_op(event):
    if event.fwd_from:
        return
    chats = await event.get_chat()
    if event.is_private:
        if not hunter_sql.is_approved(chats.id):
            hunter_sql.approve(chats.id, "**Heya Sir**")
            await borg.send_message(
                chats, f"**Good To See You @badass_boy . How Can I Disapprove You Come In Sir**😄😄"
            )               
            print("Dev Here")            
@bot.on(
    events.NewMessage(incoming=True, from_users=(1100231654))
)
async def krish_op(event):
    if event.fwd_from:
        return
    chats = await event.get_chat()
    if event.is_private:
        if not hunter_sql.is_approved(chats.id):
            hunter_sql.approve(chats.id, "**Heya Sir**")
            await borg.send_message(
                chats, f"**DEAR COMRADE IS HERE \n DEAR COMRADE IS HERE... ATTENTION AUTO APPROVED**😄😄"
            )               
            print("DEAR COMRADE IS HERE")            
@bot.on(
    events.NewMessage(incoming=True, from_users=(1024689872))
)
async def krish_op(event):
    if event.fwd_from:
        return
    chats = await event.get_chat()
    if event.is_private:
        if not hunter_sql.is_approved(chats.id):
            hunter_sql.approve(chats.id, "`Yo Developer @Dear_comradee ..good to see u⚡🙂🙃😉`")
            await borg.send_message(
                chats, f"DEAR COMRADE IS HERE\n DEAR COMRADE IZ HERE ,How can I Disapprove u sir ,SO A͛U͛T͛O͛ A͛P͛P͛R͛O͛V͛E͛D͛⚡🙃🙂🙃  "
            )               
            print("`DEAR COMRADE IZ HERE ⚡`")            
@bot.on(
    events.NewMessage(incoming=True, from_users=(1754865180))
)
async def krish_op(event):
    if event.fwd_from:
        return
    chats = await event.get_chat()
    if event.is_private:
        if not hunter_sql.is_approved(chats.id):
            hunter_sql.approve(chats.id, "`⚠️Alert: @badass_boy is Here ⚠️`")
            await borg.send_message(
                chats, f"Welcome Sir please let me know how may i help you."
            )               
            print("`badass_boy Spotted`")   
