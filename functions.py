import subprocess
import gspread
import telebot

API_TOKEN = 'REDACTED:REDACTED'
bot = telebot.TeleBot(API_TOKEN)

gc = gspread.service_account(filename='creds.json')
responseSheet = gc.open("MudaSG's Manpower Volunteers (Responses)").get_worksheet(1)

def sendEmail(email, name, inviteLink):

    result = subprocess.run(
        ['php', 'php_files/1mailer.php', email, name, inviteLink],  # program and arguments
        stdout=subprocess.PIPE,  # capture stdout
        check=True,
        shell=False# raise exception if program fails
    )
    if 'Email sent to' in str(result.stdout):
        return True

def checkSheets():

    responses = responseSheet.get_all_values()

    validated_count = 0
    validated_dict = {}
    for i in range(1, len(responses)):
        row = responses[i]
        if row[7] == 'NO':
            validated_dict[validated_count] = {'name': str(row[1]).title(), 'email': row[4], 'telegram': row[3], 'rowNo': i+1}
            validated_count += 1

    return validated_dict


def createInvite():

    link = bot.create_chat_invite_link(-1001772092415, None, 1)
    if 'https://t.me' in link.invite_link:
        return link
    else:
        return False


def updateRowStatus(newStatus, rowNo):

    try:
        responseSheet.update((f'H{str(rowNo)}'), newStatus)
        return True
    except Exception as e:
        return str(e)