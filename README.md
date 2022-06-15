<center> 高考志愿-各校专业成绩 </center>
==== 
>数据来自[掌上高考](https://www.gaokao.cn)，程序仅供学习使用，不得参与任何商业模式

#### 基于 python 获取 各校专业成绩 的爬虫

### 使用过程
* 安装所需的 python 库
```cmd
pip install xlsxwriter
pip install requests
pip install selenium
pip install bs4
```

* 根据电脑上的 Chrome 版本自行下载 [chromedriver.exe](https://registry.npmmirror.com/binary.html?path=chromedriver) ，需要保证 Chrome 浏览器前三个版本号相同
* 修改 getScore.py 97 行，将下载的 chromedriver.exe 路径填写至 executable_path
* 运行 getScore.py 填写想要获取的专业，爬取结束后自动导出 Excel 表格


### 注意事项：
* 使用 Chrome 浏览器来示范
* 使用 selenium 模拟浏览器访问 [掌上高考](https://www.gaokao.cn/)
* 通过 BeautifulSoup 来对数据进行解析
* 通过 getJson.py 来获取 init.json 文件，其中包括专业的基本信息
* 所有数据来自 掌上高考 ，数据可能不全，还望谅解



#### Author：忆古陌烟
