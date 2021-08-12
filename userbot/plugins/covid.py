
from covid import Covid

from userbot import client
from userbot.utils.events import NewMessage
from googletrans import Translator

plugin_category = "pandemic"
covid_str = f"`Casi totali registrati:`  **%(confirmed)s**\n`Positivi attuali:`  **%(active)s**\n`Morti giornalieri:`  **%(new_deaths)s**\n`Nuovi casi:`  **%(new_cases)s**"

@client.onMessage(
    command="`covid` `(Nazione)`",
    outgoing=True, regex="(?:covid|corona)(?: |$)(.*)"
)
async def covid19(event: NewMessage.Event) -> None:
    await event.edit('__Sto ottenendo le informazioni..__')
    covid = Covid(source="worldometers")
    match = event.matches[0].group(1)
    if match:
        strings = []
        failed = []
        args, _ = await client.parse_arguments(match)
        if match.lower() == "countries":
            strings = sorted(covid.list_countries())
        else:
            for c in args:
                try:
                    translator = Translator()
                    translated = translator.translate(c, dest='en')
                    cn = translated.text
                    country = covid.get_status_by_country_name(cn)
                    string = f"📊 **COVID-19** __({country['country']})__\n"
                    string += covid_str % country
                    strings.append(string)
                except ValueError:
                    failed.append(c)
                    continue
        if strings:
            await event.answer('\n\n'.join(strings))
        if failed:
            string = "`Impossibile trovare la nazione:` "
            string += ', '.join([f'`{x}`' for x in failed])
            await event.answer(string, reply=True)
    else:
        strings_ = []
        country = covid.get_status_by_country_name('italy')
        string = f"📊 **COVID-19** __(Italia)__\n"
        string += covid_str % country
        strings_.append(string)
        await event.answer('\n\n'.join(strings_))
       
   
