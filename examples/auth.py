from anixart import AnixartAPI, AnixartAccount
from anixart import endpoints
from anixart.exceptions import AnixartAPIRequestError
from anixart.profile import Profile

anix = AnixartAPI()  # По умолчанию используется гость

# acc = AnixartAccount("SantaSpeen", "I_H@ve_Very_Secret_P@ssw0rd!")
# # id у аккаунта появляется только после
# anix.use_account(acc)

if __name__ == '__main__':
    try:
        raw = anix.execute("GET", endpoints.PROFILE.format(1))
        profile = {"is_my_profile": raw['is_my_profile'], **raw['profile']}
        print(Profile(**profile))
    except AnixartAPIRequestError as e:
        print(e.message)
        print(e.code)
