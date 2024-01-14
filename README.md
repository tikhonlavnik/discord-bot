# Discord BOT for VK

## Description
To use this Discord bot you can write the command:
/get_info <vk_link>

Vk_link is link of user page or community page.

As the answer you'll get this info:

If it's user's link - his VK id, first and last name,
date of registration and profile photo also link_name or username.

Else if it's community page bot sends you its VK id, name,
community photo and link_name or username.

---

## Installing

1. First step, run:
```commandline
pip install -r requirements.txt
```

2. Don't forget to create .env file and put here your tokens for Discord and VK.

3. Use:
```commandline
python bot.py
```


