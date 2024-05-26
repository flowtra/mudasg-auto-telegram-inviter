from functions import *
import time

delay = int(input('Enter checking delay: '))

while True:
    new_signups_dict = checkSheets()
    for signup_row in new_signups_dict.values():
        print(f"New Signup | {signup_row['name']}, {signup_row['email']}")
        invLinkObject = createInvite()
        if invLinkObject == False:
            print(f"! ERROR CREATING INVITE LINK ! | {signup_row['name']}, {signup_row['email']}")
            continue

        emailStatus = sendEmail(signup_row['email'], signup_row['name'], invLinkObject.to_dict()['invite_link'])
        if not emailStatus:
            status = updateRowStatus('ISSUE', signup_row['rowNo'])
            if not status:
                print(f"! ERROR UPDATING STATUS TO ISSUE ! | {signup_row['name']}, {signup_row['email']}")
            else:
                print(f" UPDATED STATUS TO ISSUE | {signup_row['name']}, {signup_row['email']}")

            print(f"! ERROR SENDING EMAIL ! | {signup_row['name']}, {signup_row['email']}")
            continue
        print(f" EMAIL SENT | {signup_row['name']}, {signup_row['email']}")

        status = updateRowStatus('YES', signup_row['rowNo'])
        if not emailStatus:
            print(f"! ERROR UPDATING STATUS TO YES ! | {signup_row['name']}, {signup_row['email']}")
        print(f" UPDATED STATUS TO YES | {signup_row['name']}, {signup_row['email']}")

    time.sleep(delay)