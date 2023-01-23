from .AC名单 import AcceptedRoster
from bs4 import BeautifulSoup
from urllib import parse
from .登录 import Login
import asyncio
import random


class Answer(AcceptedRoster):
    """ OJ答案爬虫 """
    htmlList: list[str]

    async def __getHTML(self, exam: int, problem: int, page: int = None) -> list[str]:
        """ 获取HTML列表 """
        htmlList: list[str] = []
        for human in self.roster:
            try:
                login = Login(str(human['学号']))
                await login()
                url = parse.urljoin(
                    self.url, f"solution/read/id/{human['提交ID']}")
                html = (await self.client.get(url, cookies=login.cookies)).text
            except (Exception, BaseException)as e:
                print(e)
                continue
            else:
                htmlList.append(html)
            finally:
                if len(htmlList) >= 3:
                    break
                await asyncio.sleep(1)
        self.htmlList = htmlList
        return htmlList

    async def __call__(self, exam: int, problem: int, page: int = None) -> list[str]:
        """ 返回至多3个代码 """
        self.roster = await super().__call__(exam, problem, page)
        random.shuffle(self.roster)
        htmlList: list[str] = await self.__getHTML(exam, problem, page)
        codeList: list[str] = []
        for html in htmlList:
            soup = BeautifulSoup(html, 'html.parser')
            code = soup.find('code').next_element.get_text().strip()
            codeList.append(code)
        return codeList
