from collections import namedtuple
from hashlib import md5

import httpx
import parsel

# Namedtuple for project.
Project = namedtuple('Project', ['project_id', 'title', 'description', 'url'])


def search(term: str):
    # HTTP client session to do HTTP requests.
    http_client = httpx.Client(http2=True, timeout=40)

    # HTTP request to 99freela searching for any term.
    request = http_client.get(
        url="https://www.99freelas.com.br/projects",
        params=dict(q=term)
    )

    # Parsed response text of previous request.
    parsed_response = parsel.Selector(text=request.text)

    # Getting projects of previous query.
    projects = parsed_response.xpath('//ul[@class="result-list"]//li')

    # Iterating projects.
    for project in projects:
        # Getting project title.
        title = project.xpath('.//h1[@class="title"]/a/text()').get()

        # Getting project description.
        description = project.xpath(
            './/div[@class="item-text description formatted-text"]/text()'
        ).getall()

        # Stripping description.
        description = '\n'.join(map(str.strip, description))

        # Getting project url.
        url = (
            "https://www.99freelas.com.br"
            + project.xpath('.//h1[@class="title"]/a/@href').get()
        )

        # Getting project id.
        project_id = md5((title + description + url).encode()).hexdigest()

        # Yielding project.
        yield Project(project_id, title, description, url)
