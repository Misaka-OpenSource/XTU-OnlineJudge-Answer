""" 
示例-获取OJ答案 
以爬取exam_id为401, problem_id为1461的题目为例
"""

from OJ爬虫模块 import Answer
import json
import os


async def main(exam_id: int, problem_id: int, max_num=3):
    answer = Answer()
    codeList: list[str] = await answer.getAnswer(exam=exam_id, problem=problem_id, max_num=max_num)

    if not os.path.exists(f"docs/answer/{exam_id}"):
        os.makedirs(f"docs/answer/{exam_id}")

    html_index = '<meta charset="utf-8">'
    for index in range(max_num):
        with open(f"docs/answer/{exam_id}/{problem_id}-{index+1}.cpp", "w")as fw:
            fw.write(codeList[index])
        with open(f"docs/answer/{exam_id}/{problem_id}-{index+1}.html", "w")as fw:
            fw.write(
                answer.htmlList[index]+f'<a href="./{problem_id}-{index+1}.cpp">下载CPP文件</a>')
        html_index += f'<p><a href="./{problem_id}-{index+1}.html">代码示例{index+1}</a></p>'
    with open(f"docs/answer/{exam_id}/{problem_id}.html", "w", encoding="utf-8")as fw:
        fw.write(html_index)

    with open("docs/answer/index.json", "r")as fr:
        data: list = json.load(fr)
    data += [{'exam_id': exam_id, 'problem_id': problem_id, 'max_num': max_num}]
    with open("docs/answer/index.json", "w")as fw:
        json.dump(data, fw, ensure_ascii=False, indent=4)
