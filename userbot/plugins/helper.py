
import os.path
import re
from typing import Tuple

from userbot import client
from userbot.utils.events import NewMessage


plugin_category: str = "helper"
split_exp: re.Pattern = re.compile(r'\||\/')


@client.onMessage(
    command=("<code>help</code>", plugin_category), builtin=True,
    outgoing=True, regex=r"help(?: |$)(\w*)(?: |$)(dev|details|info)?"
)
async def helper(event: NewMessage.Event) -> None:
    arg = event.matches[0].group(1)
    enabled, senabled = await solve_commands(client.commands)
    if arg == '1' or not arg:
        text = "<b>🌍 Lista Comandi 🌍</b>\n\n"
        text += "\n".join([f'<code>.{name}</code>' for name in sorted(enabled)])+"\n\n<i>Scrivi .help 2 per vedere le funzioni dei comandi!</i>"
    elif arg == '2':
        text = """<b>— Comando | Funzione</b> —

<code>.addfilter</code> | <i>Tramite questo comando è possibile creare dei  filtri che restano in modo permanente.

</i><code>.addsticker</code> | <i>Tramite questo comando è possibile trasformare un sticker, o una foto in uno sticker che verrà aggiunto nel vostro pack.

</i><code>.afk</code> | <i>Tramite questo comando </i>è possibile andare AFK o tornare non AFK. Andando AFK riceverai le notifiche solo di chi è approvato.

<code>.approve</code> | Tramite questo comando puoi approvare un utente, che potrà scriverti quando sei AFK.

<code>.approved</code> | <i>Tramite questo comando è</i> possibile vedere la lista di approvati, che possono scriverti quando sei AFK.

<code>.bio</code> | <i>Tramite questo comando è possibile visualizza la propria bio o cambiarla.

</i><code>.calc </code>| <i>Tramite questo comando è possibile eseguire operazioni matematiche.

</i>.<code>covid</code> | <i>Tramite questo comando è possibile vedere le informazioni sul Covid-19 nella propria nazione o in altre.

</i>.<code>.del</code> | <i>Tramite questo comando è possibile eliminare tutti i propri messaggi rispondendo al messaggio da cui iniziare la pulizia.

</i>.<code>.delfilter</code> | <i>Tramite questo comando è possibile rimuovere un filtro.

</i>.<code>.disapprove</code> | <i>Tramite questo comando è possibile disapprovare un utente, che quindi non può più scriverti quando sei AFK.

</i><code>.filterlist</code> | <i>Tramite questo comando è possibile visualizzare la lista di filtri impostati.

</i><code>.getpic</code> | <i>Tramite questo comando è possibile convertire uno sticker in un'immagine.

</i> <code>.hack</code> | <i>Tramite questo comando è possibile fingere di hackerare un account.

</i>.<code>.id</code> | <i>Tramite questo comando è possibile ottenere l'ID di un utente.

</i><code>.info</code> | <i>Tramite questo comando è possibile ottenere le info di un utente

</i><code>.mute</code> | <i>Tramite questo comando è possibile mutare un utente in privato, o in un gruppo se si dispone dei permessi adatti.

</i>.<code>.off</code> | <i>Questo comando aggiungerà al vostro nome il prefisso [Offline]

</i>.<code>.on</code> | <i>Questo comando aggiungerà al vostro nome il prefisso [Online]

</i><code>.pack</code> | <i>Tramite questo comando è possibile visualizzare i pack creati con</i> <code>.addsticker</code>.

<code>.pfp</code> | <i>Tramite questo comando è possibile cambiare foto profilo rispondendo ad una foto o visualizzare la propria.

</i><code>.ph</code> | <i>Abbiamo capito..

</i><code>.ping</code> | <i>Tramite questo comando è possibile visualizzare il proprio ping.

</i><code>.purge</code> | <i>Tramite questo comando è possibile eliminare tutti i messaggi rispondendo al messaggio da cui iniziare la pulizia.

</i><code>.restart</code> | <i>Tramite questo comando è possibile riavviare l'userbot.

</i><code>.spam</code> | <i>Tramite questo comando è possibile spammare un messaggio quante volte si vuole.

</i><code>.speedtest</code> | <i>Tramite questo comando è possibile eseguire uno speedtest.

</i><code>.timer</code> | <i>Tramite questo comando è possibile creare messaggi programmati.

</i><code>.tr</code> | <i>Tramite questo comando è possibile tradurre un messaggio da qualsiasi lingua ad una predefinita (Italiano).

</i><code>tspam</code> | <i>Tramite questo comando è possibile inviare un messaggio lettera per lettera</i>.

<code>.type</code> | <i>Tramite questo comando è possibile inviare un messaggio come se fosse una macchina da scrivere</i>.

<code>.unmute</code> | <i>Tramite questo comando è possibile smutare un utente in privato, o in un gruppo se si dispone dei permessi.

</i><code>.username</code> | <i>Tramite questo comando è possibile visualizza o cambiare il proprio username.</i>"""
    await event.answer(text, parse_mode='html')

async def solve_commands(commands: dict) -> Tuple[dict, dict]:
    new_dict: dict = {}
    com_tuples: dict = {}
    for com_names, command in commands.items():
        splat = split_exp.split(com_names)
        if splat:
            for n in splat:
                com_tuples[n] = command
            new_dict[''.join(splat)] = command
        else:
            new_dict[com_names] = command
    return new_dict, com_tuples
