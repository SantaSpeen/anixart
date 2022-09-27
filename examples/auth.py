from anixart import AnixartAPI, AnixartUserAccount, PROFILE

user = AnixartUserAccount("SantaSpeen", "I_H@ve_Very_Secret_P@ssw0rd!")
anix = AnixartAPI(user)


if __name__ == '__main__':
    me = anix.execute("GET", PROFILE.format(user.id))
    print(me.json())
