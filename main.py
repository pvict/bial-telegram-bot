from telegram.ext import Updater, CommandHandler
import logging

import datetime
import random
import time
import pytz

tz_BR = pytz.timezone('America/Sao_Paulo')

from paredaoList import paredaoArray
from liderVar import liderValue
from anjoVar import anjoValue
from monstroList import monstroArray
from quoteList import quoteArray
from participantes import elenco

TOKEN = "1550816757:AAFsw0wsY3MnbfIQmSg6kVlVUpXs0l_1jmY"

def getParticipante():
  randomNumber = random.randint(0, len(elenco)-1)
  integrante = elenco[randomNumber]
  return integrante

def getWeekDay():
    weekDay = datetime.datetime.now(tz_BR).weekday()
    return weekDay

def getRemainingDays():
    today = datetime.date.fromtimestamp(time.time()-10800)
    ending = datetime.date(2021, 5, 4)
    remaining = ending - today
    return str(remaining.days)

def getRejectionLevel():
    level = round(random.uniform(0, 100), 2)
    return level

def getPhoneQuote():
    randomNumber = random.randint(0, len(quoteArray)-1)
    phoneQuote = quoteArray[randomNumber]
    return phoneQuote

def start(update, context):
    s = "Vem dar uma espiadinha! 👁"
    update.message.reply_text(s)


def quemsoueu(update, context):
    participante = getParticipante()
    s = "No BBB21, você seria {}".format(participante[0])
    update.message.reply_text(s)
    context.bot.send_photo(chat_id=update.effective_chat.id, photo = participante[1] )

def bigfone(update, context):
    s = "📞  ATENÇÃO, ATENÇÃO! PRESTE MUITA ATENÇÃO:"
    update.message.reply_text(s)
    quote = getPhoneQuote()
    time.sleep(2.5)
    context.bot.send_message(chat_id=update.effective_chat.id, text=quote)

def rejeicao(update, context):
    rejectionLevel = getRejectionLevel()
    user = update.message.from_user
    username = user['username']
    firstName = user['first_name']
    sticker = ""

    if rejectionLevel > 50 and rejectionLevel <= 80:
      sticker = "😒"
    elif rejectionLevel > 20 and rejectionLevel <= 50:
      sticker = "😐"
    elif rejectionLevel > 80:
      sticker = "🤬"
    else:
      sticker = "😊"

    if len(str(user['username'])) < 5:
      s = '{}, seu nível de rejeição no BBB21 seria de {}% {}'.format(firstName, rejectionLevel, sticker)
      print('eai')
    else:
      s = '{}, seu nível de rejeição no BBB21 seria de {}% {}'.format(username, rejectionLevel, sticker)
    update.message.reply_text(s)

def contagem(update, context):
    s = "Faltam " + getRemainingDays() + " dias para o fim do BBB 21 🗓"
    update.message.reply_text(s)

def lider(update, context):
    s = "O líder é " + liderValue + " 👑"
    update.message.reply_text(s)

def anjo(update, context):
    if getWeekDay() >= 4:
      s = "O anjo é: " + anjoValue + " 😇"
    else:
      s = "Não há anjo definido! ❌"
    update.message.reply_text(s)

def monstro(update, context):
  if getWeekDay() >= 4:
    if len(monstroArray) > 1:
      s = "Os monstros são: "
      for x in range(len(monstroArray)):
        if x == 0:
          s = s + monstroArray[x] + " e "
        else:
          s = s + monstroArray[x] + " 😈"
    else:
      s = "O monstro é: " + monstroArray[0] + " 😈"
  else:
    s = "Não há monstro definido! ❌"
  update.message.reply_text(s)

def paredao(update, context):
  if getWeekDay() <= 1:
    s = "Estão no paredão: "
    for x in range(len(paredaoArray)):
      if x == len(paredaoArray)-1:
        s = s + paredaoArray[x] + " 🧱"
      elif x == len(paredaoArray)-2:
        s = s + paredaoArray[x] + " e "
      else:
        s = s + paredaoArray[x] + ", "
  else:
    s = "Não há paredão formado! ❌"
  update.message.reply_text(s)


def main():
    logger = logging.getLogger(__name__)
    logging.basicConfig(
        format='%(asctime)s [%(levelname)s] %(message)s', level=logging.INFO
    )

    updater = Updater(TOKEN)
    dp = updater.dispatcher

    dp.add_handler(CommandHandler("start", start))
    dp.add_handler(CommandHandler("paredao", paredao))
    dp.add_handler(CommandHandler("lider", lider))
    dp.add_handler(CommandHandler("monstro", monstro))
    dp.add_handler(CommandHandler("anjo", anjo))
    dp.add_handler(CommandHandler("contagem", contagem))
    dp.add_handler(CommandHandler("rejeicao", rejeicao))
    dp.add_handler(CommandHandler("bigfone", bigfone))
    dp.add_handler(CommandHandler("quemsoueu", quemsoueu))

    updater.start_polling()
    logging.info("=== Bot running! ===")
    updater.idle()
    logging.info("=== Bot shutting down! ===")

if __name__ == "__main__":
    main()
