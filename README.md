# 湘潭大学OJ爬虫模块

## 使用

> 确保Python版本>=3.9

### 安装依赖
```shell
pip install -r requirements.txt
```

### 爬取答案

参见`demo.py`的示例

## 实现

使用设定的账号和密码登录OJ, 进去评测记录页面获取AC名单, 逐一尝试以默认密码登录, 成功登录则返回代码记录
