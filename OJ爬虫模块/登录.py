from bs4 import BeautifulSoup
from urllib import parse
import warnings
import asyncio
import httpx


class Login(object):
    """ OJ登录基类 """
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3"}
    timeout = 3
    max_retry = 2
    proxy = None

    cookies: dict = None
    username: str = None
    password: str = None
    url: str = None

    def __init__(
        self,
        username: str,
        password: str = None,
        cookies: dict = None,
        login_url: str = "https://acm.xtu.edu.cn/exam/index.php/"
    ) -> None:
        self.client = httpx.AsyncClient(
            http2=True, timeout=self.timeout, headers=self.headers, verify=False, proxies=self.proxy)
        self.url = login_url
        self.username = username
        self.password = password if password else username
        self.cookies = cookies
        warnings.simplefilter('ignore', ResourceWarning)

    async def __accessHome(self) -> str:
        """ 访问首页(登录页), 返回HTML """
        try:
            resp = await self.client.get(
                url=self.url, cookies=self.cookies)
            assert resp.status_code == 200
        except (Exception, BaseException) as e:
            await asyncio.sleep(4)  # 获取失败时暂停4秒
            return await self.__accessHome()
        else:
            self.cookies = resp.cookies
            return resp.text

    def getToken(self, html: str) -> list[str]:
        """ 从HTML页面获取token, 并返回 """
        soup = BeautifulSoup(html, 'html.parser')
        tokens = [str(x.attrs['value'])
                  for x in soup.find_all('input', id='crsf_token')]
        if len(tokens):
            return tokens
        else:
            raise Exception("被防火墙拦截")

    async def __login(self, tokens: list[str]) -> bool:
        """ 发送登录请求 """
        data = {
            'crsf_token': tokens[0],
            'username': str(self.username).strip(),
            'password': str(self.password).strip(),
            'capture': 'login',
            'Submit': 'Login'
        }
        try:
            resp = await self.client.post(
                url=self.url, data=data, cookies=self.cookies)
            assert resp.status_code == 200, f"登录失败 {resp.status_code}!"
            await asyncio.sleep(1)
            assert await self.checkLogin(resp.text), "登录不成功"
        except (Exception, BaseException) as e:
            print(e)
            return False
        else:
            return True

    async def checkLogin(self, html: str = None) -> bool:
        """ 检查登录是否成功且有效 """
        try:
            html = html if html else \
                (await self.client.get(url=self.url, cookies=self.cookies)).text
            assert self.username in html
        except:
            with open('error.html', 'w') as fw:
                fw.write(html)
            return False
        else:
            return True

    async def __call__(self) -> dict:
        """ 登录, 返回cookies """
        tokens = self.getToken(await self.__accessHome())
        await asyncio.sleep(1)
        assert await self.__login(tokens), "登录异常, 请检查账号密码"
        return dict(self.cookies)
