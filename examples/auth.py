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
        raw = anix.get(endpoints.PROFILE, 1)
        print(Profile.from_response(raw))
    except AnixartAPIRequestError as e:
        print(e.message)
        print(e.code)
