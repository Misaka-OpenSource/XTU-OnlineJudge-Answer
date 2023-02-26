from bs4 import BeautifulSoup
from urllib import parse
from .登录 import Login


class AcceptedRoster(Login):
    """ AC名单爬虫 """

    async def __getAcceptedHTML(self, exam: int, problem: int, page: int = None) -> str:
        """ 获取AC名单HTML """
        url = parse.urljoin(
            self.url, f"solution/onlinestatus/exam_id/{exam}/p/{page}")
        resp = await self.client.get(url=url, cookies=self.cookies)
        token = self.getToken(resp.text)
        data: dict = {
            'crsf_token': token[3],
            'username': '',
            'problem_id': problem,
            'result': '31',
            'language': '',
            'Submit5': 'GO'
        }
        resp = await self.client.post(url=url, data=data, cookies=self.cookies, headers=self.headers)
        return resp.text

    def __analysisHTML(self, html: str) -> list[dict]:
        """ 解析HTML """
        soup = BeautifulSoup(html, 'html.parser')
        表格区 = soup.find('div', id='content')
        所有提交 = 表格区.find_all('tr')
        所有学号: list[str] = \
            [{'学号': int(提交.find_all('td')[1].next_element.strip()),
              '提交ID':int(提交.find_all('td')[0].next_element.strip())}
             for 提交 in 所有提交[3:-1]]
        return 所有学号

    async def getList(self, exam: int, problem: int) -> list[dict]:
        """ 返回AC名单的列表 """
        res: list[dict] = []
        for page in range(2):
            res += self.__analysisHTML(await self.__getAcceptedHTML(exam, problem, page))
        print(f"AC名单 {res}")
        return res
