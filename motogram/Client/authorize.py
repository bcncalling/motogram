#motogram: An asynchronous Python wrapper for the Telegram Bot API.
#
#This library is based on pyrogram (https://github.com/pyrogram/pyrogram).
#Copyright (C) 2023 [Santhu]
#
#motogram is free software: you can redistribute it and/or modify
#it under the terms of the GNU General Public License as published by
#the Free Software Foundation, either version 3 of the License, or
#(at your option) any later version.

#motogram is distributed in the hope that it will be useful,
#but WITHOUT ANY WARRANTY; without even the implied warranty of
#MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#GNU General Public License for more details.
#
#You should have received a copy of the GNU General Public License
#along with motogram.  If not, see <https://www.gnu.org/licenses/>.

import motogram
from motogram.wrongs import BadRequest, SessionPasswordNeeded
from motogram.types import User 

async def authorize(mtclient):
    if mtclient.bot_token:
        return await sign_in_bot(mtclient, mtclient.bot_token)

    print(f"Welcome to Motogram (version {motogram.__version__})")
    print(f"Motogram is free software and comes with ABSOLUTELY NO WARRANTY. Licensed\n"
          f"under the terms of the {motogram.__license__}.\n")

    while True:
        try:
            if not mtclient.phone_number:
                while True:
                    value = await ainput("Enter phone number or bot token: ")

                    if not value:
                        continue

                    confirm = (await ainput(f'Is "{value}" correct? (y/N): ')).lower()

                    if confirm == "y":
                        break

                if ":" in value:
                    mtclient.bot_token = value
                    return await sign_in_bot(mtclient, value)
                else:
                    mtclient.phone_number = value

            sent_code = await send_code(mtclient, mtclient.phone_number)
        except BadRequest as e:
            print(e.MESSAGE)
            mtclient.phone_number = None
            mtclient.bot_token = None
        else:
            break

    sent_code_descriptions = {
        motogram.checks.CodeType.APP: "Telegram app",
        motogram.checks.CodeType.SMS: "SMS",
        motogram.checks.CodeType.CALL: "phone call",
        motogram.checks.CodeType.FLASH_CALL: "phone flash call",
        motogram.checks.CodeType.FRAGMENT_SMS: "Fragment SMS",
        motogram.checks.CodeType.EMAIL_CODE: "email code"
    }

    print(f"The confirmation code has been sent via {sent_code_descriptions[sent_code.type]}")

    while True:
        if not mtclient.phone_code:
            mtclient.phone_code = await ainput("Enter confirmation code: ")

        try:
            signed_in = await sign_in(mtclient, mtclient.phone_number, sent_code.phone_code_hash, mtclient.phone_code)
        except BadRequest as e:
            print(e.MESSAGE)
            mtclient.phone_code = None
        except SessionPasswordNeeded as e:
            print(e.MESSAGE)

            while True:
                print("Password hint: {}".format(await get_password_hint(mtclient)))

                if not mtclient.password:
                    mtclient.password = await ainput("Enter password (empty to recover): ", hide=mtclient.hide_password)

                try:
                    if not mtclient.password:
                        confirm = await ainput("Confirm password recovery (y/n): ")

                        if confirm == "y":
                            email_pattern = await send_recovery_code(mtclient)
                            print(f"The recovery code has been sent to {email_pattern}")

                            while True:
                                recovery_code = await ainput("Enter recovery code: ")

                                try:
                                    return await recover_password(mtclient, recovery_code)
                                except BadRequest as e:
                                    print(e.MESSAGE)
                                except Exception as e:
                                    log.exception(e)
                                    raise
                        else:
                            mtclient.password = None
                    else:
                        return await check_password(mtclient, mtclient.password)
                except BadRequest as e:
                    print(e.MESSAGE)
                    mtclient.password = None
        else:
            break

    if isinstance(signed_in, User):
        return signed_in

    while True:
        first_name = await ainput("Enter first name: ")
        last_name = await ainput("Enter last name (empty to skip): ")

        try:
            signed_up = await sign_up(mtclient, mtclient.phone_number, sent_code.phone_code_hash, first_name, last_name)
        except BadRequest as e:
            print(e.MESSAGE)
        else:
            break

    return signed_up
