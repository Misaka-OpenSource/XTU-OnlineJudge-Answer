import asyncio
from OJ爬虫模块 import (
    Answer
)


async def demo():
    """ 
    示例-获取OJ答案 
    以爬取exam_id为403, problem_id为1416的题目为例
    id可以从题目的链接中得到
    """
    answer = Answer(username="2021********", password="****")
    dataList: list[str] = answer(exam=403, problem=1416)
    for value in dataList:
        print(value)

if __name__ == "__main__":
    asyncio.run(demo())
