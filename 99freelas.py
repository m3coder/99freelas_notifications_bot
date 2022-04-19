import httpx, parsel, time

from tqdm import tqdm #optional use

# your bot configuration (token_id, chat_id)

messages = []

bot_config = {
    "bot_token": "YOUR BOT TOKEN",
    "chat_id": "YOUR CHAT/GROUP/CHANNEL ID"
}


def search():
    global messages
    print("rodando")

    #making a request on the 99freelas page and getting the text to later make a parser collecting only the ul element of the hmtl
    hc =  httpx.Client(http2=True, timeout=40)
    page = hc.get(url="https://www.99freelas.com.br/projects?q=python").text

    list_items_html = parsel.Selector(text=page).xpath('//ul[@class="result-list"]').xpath(".//li")

    #doing an iteration with the for loop to get each item within the list
    for x in list_items_html:
        # getting the text of each title element
        tilte = x.xpath('.//h1[@class="title"]/a/text()').get() 

        #getting the value of the href that is the link of the service page
        url = "https://www.99freelas.com.br" + x.xpath('.//h1[@class="title"]/a/@href').get()

        #taking the informative description
        desc = x.xpath('.//div[@class="item-text description formatted-text"]/text()').get().strip()
        
        message = f'''<b>👷‍♂️ 99Freelas</b>\n\n<b>📌 titulo:</b><i> {tilte}</i>\n\n<b>ℹ️ informativo:</b><i> {desc}</i>\n\n<a href="{url}"> 🔗click aqui para ver</a>'''

        mm = f"{tilte}---{desc}"

        if mm not in messages:
            hc.get(f'https://api.telegram.org/bot{bot_config["bot_token"]}/sendMessage?',
            params=dict(chat_id=bot_config["chat_id"], text=message, parse_mode="HTML", disable_web_page_preview="True")
            )
            messages.append(mm)
        else:
            pass


def your_time(**kwargs):
    if kwargs.get("minutes") and kwargs.get("minutes") != 0:
       return kwargs["minutes"] * 60

    elif kwargs.get("hours") and kwargs.get("hours") != 0:
        return (kwargs["hours"] * 60 * 60)


new_messages = None


while 1:
    search()
    new_messages = len(messages) - 10
    time.sleep(your_time(hours=1))
    messages.clear() if new_messages == 10 else None
