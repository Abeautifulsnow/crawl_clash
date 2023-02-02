# 使用说明

需要python版本 `python3.8` 及以上，以及 `clash客户端`。

安装需要的第三方库: `pip install -r requirements.txt`。

- 运行脚本

```bash
python3 clash.py
```

运行完后，脚本会在本地 `$HOME/.config/clash/` 下创建一个 `${date}.yaml` 文件，文件名字以 `月日时分` 作为名称，比如 `02011919.yaml` 代表2月1日19时19分生成的文件。

生成好文件之后，clash客户端会自动加载该目录下的配置文件，并展现在clash客户端菜单的 `配置目录` 下，只需要你日常使用的时候选择对应时间的文件就行。

- 截图如下:

![clash.png](https://raw.githubusercontent.com/Abeautifulsnow/crawl_clash/main/clash.png)
