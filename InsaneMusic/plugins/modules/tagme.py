# Assuming you have defined the client object and necessary setup for the Telegram bot

spam_chats = []

TAGMES = ["hi", "hello", "good morning", "good evening", "good night", "yellarum yenna pandringa","vetiya iruntha vc ku vanga work la irrunthalum vanga😉", "bore adikuthey yenna panalam"]
EMOJI = ["😊", "👋", "🌞", "🌙","❤️", "💚", "💙", "💜", "🖤"]


#@app.on_message(filters.command(["tagme"], prefixes=["/", "@", "!"]))
@app.on_message(filters.regex(r'^/tagme ?(.*)'))
async def tagme_handler(client, message: Message):
    chat_id = message.chat.id
    if chat_id in spam_chats:
        await message.reply("The tagme command use pannitenga 🌝.")
        return

    #if message.reply_to_message and message.text:
    if message.matches[0].group(1) and message.reply_to_message:
        return await message.reply("/tagme ** ᴛʀʏ ᴛʜɪs ɴᴇxᴛ ᴛɪᴍᴇ uh ғᴏʀ ᴛᴀɢɢɪɴɢ...*")
    #elif message.text:
    elif message.matches[0].group(1):
        mode = "text_on_cmd"
        #msg = message.text
        msg = message.matches[0].group(1)
    elif message.reply_to_message:
        mode = "text_on_reply"
        msg = message.reply_to_message
        #msg = await app.get_messages(message.chat.id, message.reply_to_message.message_id)
        if msg is None:
            return await message.reply("I cannot mention msgs sent before I was added in group")
    else:
        return await message.reply("Reply to message or give me a message for mentioning - [ yaraiyavathu tag panni command kudungal ]")
              
    spam_chats.append(chat_id)
    usrnum = 0
    usrtxt = ""

    async for usr in client.iter_chat_members(chat_id):
        if not chat_id in spam_chats:
            break

        if usr.user.is_bot:
            continue

        usrnum += 1
        #usrtxt += f"[{usr.user.first_name}](tg://user?id={usr.user.id}) "
        usrtxt += f"{usr.user.mention}"

        if usrnum == 1:
            if mode == "text_on_cmd":
                txt = f"{usrtxt} {random.choice(TAGMES)}"
                markup = blast_markup()                    
                await message.reply_text(
                          txt, 
                          reply_markup=markup
                )
            elif mode == "text_on_reply":
                #await message.delete()
                markup = blast_markup()                       
                await msg.reply_text(
                          f"[{random.choice(EMOJI)}](tg://user?id={usr.user.id})", 
                          #reply_markup=markup
                )

            # Generate a random sleep time between 10 and 30 seconds(0 and 5 seconds)
            sleep_time = random.randint(0, 7)
            await asyncio.sleep(sleep_time)

            usrnum = 0
            usrtxt = ""

    try:
        spam_chats.remove(chat_id)
    except:
        pass

@app.on_callback_query(filters.regex("^blast$"))
async def on_callback_query(client, events):
    print("Callback query received:", events.data)
    if events.data == "blast":
              print("Blast button clicked!")
              morning_quote = f"Good morning {events.from_user.mention}! Here's a beautiful quote to start your day:\n\n""Life is what happens when you're busy making other plans. - John Lennon"                             
              await events.answer(f"Getting..")
              await events.message.edit_text(morning_quote)
