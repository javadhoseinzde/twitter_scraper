import re

def split_username(username):

    pattern = r'@(\w+)'

    usernames1 = re.findall(pattern, username)

    print(usernames1[0] if usernames1 else "نام کاربری پیدا نشد")

    if usernames1:
        return usernames1[0]
    else:
        return "@ not found in username"
