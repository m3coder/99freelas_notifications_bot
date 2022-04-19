import posixpath
import time

from loguru import logger
import telepot
import yaml

import nnfreelas


# Storing full current relative path.
RELATIVE_PATH = posixpath.abspath(posixpath.dirname(__file__))

# Storing config filename.
CONFIG_FILENAME = posixpath.join(RELATIVE_PATH, 'config.yml')

# Storing freela message format.
FREELA_MESSAGE_FORMAT = (
    '<b>👷‍♂️ 99Freelas</b>\n\n'
    '<a href="{url}"><b>{title}</b></a>\n\n'
    '<i>{description}</i>'
)

# Storing interval seconds.
INTERVAL_SECONDS = 10


if __name__ == '__main__':
    # Verifying if config file exists.
    if not posixpath.exists(CONFIG_FILENAME):
        # Logging critical message for 'config file not found'.
        logger.critical(
            f'Arquivo de configuração "{CONFIG_FILENAME}" inexistente.'
        )

        # Quitting with 2 - No such file or directory.
        exit(2)

    # Reading YAML config file.
    with open(CONFIG_FILENAME, encoding='utf-8') as file:
        config = yaml.safe_load(file)

    # Creatting telegram bot manager instance.
    telegram_bot = telepot.Bot(config['bot_token'])

    # Setting a set of projects.
    projects = set()

    # Storing a reference time.
    reference_time = 0

    while True:
        # Skip to next loop if interval seconds has not reached yet.
        if not (time.time() - reference_time >= INTERVAL_SECONDS):
            continue

        # If interval has reached, iterating projects found.
        for project in nnfreelas.search('python'):
            # If project is not in projects set.
            if project not in projects:
                # Adding current project to project set.
                projects.add(project)

                # Sending text message to telegram chat.
                telegram_bot.sendMessage(
                    chat_id=config['chat_id'],
                    text=FREELA_MESSAGE_FORMAT.format(
                        url=project.url,
                        title=project.title,
                        description=project.description
                    ),
                    parse_mode='html',
                    disable_web_page_preview=True
                )

                # Logging freelance was sent to telegram chat.
                logger.info('Um freelance foi enviado!')
            else:
                # Logging freelance already sent to telegram chat.
                logger.info('O freelance a enviar ja foi enviado antes.')

        # Breaking line.
        print()

        # Updating reference time.
        reference_time = time.time()
