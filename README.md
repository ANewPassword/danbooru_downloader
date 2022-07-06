## 它可以做什么

此脚本可通过[yande.re](https://yande.re/)公开 API 获取帖子列表以多线程的方式批量下载图片，可选择根据`页面ID`/`图片ID`区间下载两种下载模式，另支持自定义设置`每页帖子数量`、`搜索/排除的标签`、`线程数`、`文件保存路径`、`http代理`、`校验文件完整性`等。

脚本可自动判断图片文件是否已存在，避免重复下载消耗流量。

---

## 使用方法

### 运行方式

使用**shell**运行，仅测试了在`Windows 10 + PowerShell + Python 3.9.1 64-bit`环境下可以正常运行。

### 参数

|      参数名      | 短写参数名 | 类型 |        默认值        |                                                                                                      描述                                                                                                      |
| :--------------: | :--------: | :--: | :------------------: | :------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------: |
|       mode       |     m      | 必选 |          无          | 指定运行模式，取值范围：`["id", "page", "update", "file", "copyright"]`，`id`：通过 ID 下载 / `page`：通过页码下载 / `update`：更新脚本 / `file`：使用`json`格式的配置文件运行，同时需要指定`file-config-path` |
|      start       |     s      | 可选 |        (int)1        |                                                                                                    开始 ID                                                                                                     |
|       end        |     e      | 可选 |        (int)1        |                                                                               结束 ID，`-1` 表示下载到最新一张图/下载到最后一页                                                                                |
|      limit       |     l      | 可选 |      (int)1000       |                                                                                      每页的图片数量，取值范围：`1 - 1000`                                                                                      |
|       tags       |     t      | 可选 |       (str)""        |                                                                         搜索(`tagname`)/排除(`-tagname`)指定 tags，使用`+`连接多个 tag                                                                         |
|      thread      |     T      | 可选 |        (int)5        |                                                                            线程数，建议设置为 `5` 或更低，过高可能造成 HTTP429 错误                                                                            |
|       path       |     p      | 可选 |     (str)"./img"     |                                                                                                  文件保存路径                                                                                                  |
|      proxy       |     P      | 可选 |       (str)""        |                                                                             http 代理地址，格式：`http://[用户名:密码@]IP[:端口]`                                                                              |
|     options      |     o      | 可选 |       (str)""        |  附加操作，使用“+”连接多个参数，取值范围：`["chksums", "make-config"]`，`chksums`：下载后进行文件完整性校验**（推荐）** / `make-config`：生成一个空白的配置文件，此时`file-config-path`将视为配置文件生成路径  |
| file-config-path |    _无_    | 可选 | (str)"./config.json" |                                                                                    配置文件路径，只在运行模式为`file`时生效                                                                                    |
|    retry-max     |    _无_    | 可选 |        (int)5        |                                                                                     最大重试次数，`-1`表示重试直到下载成功                                                                                     |

### 示例

#### `id`模式

**yande.re 的 post id 会递增：post id 越大，帖子上传时间越晚，最新帖子的 post id 永远大于其他 post id。**

##### 示例一

```shell
python3 main.py -m id -s 301 -e 301
```

含义：根据`图片ID`下载，从`301`下载到`301`（仅下载 ID 为`301`的图片）。

##### 示例二

```shell
python3 main.py -m id -s 123456 -e 654321
```

含义：根据`图片ID`下载，从`123456`下载到`654321`（下载 ID 在`[123456,654321]`区间中的图片，实际下载时会倒序下载，即从 654321 开始下载）。

##### 示例三

```shell
python3 main.py -m id -s 123456 -e -1
```

含义：根据`图片ID`下载，从`123456`下载到`最新一张图`（下载 ID 大于等于`123456`的图片，实际下载时会倒序下载，即从最新一张图开始下载）。

##### 示例四

```shell
python3 main.py -m id -s 1 -e -1
```

含义：根据`图片ID`下载，从`1`下载到`最新一张图`（下载 ID 大于等于`1`的图片，即`全部下载`，实际下载时会倒序下载，即从最新一张图开始下载）。

#### `page`模式

**yande.re 的 page id 会动态更新：page id 越大，帖子上传时间越早，最新帖子所在的 page id 永远为 1。**

##### 示例五

```shell
python3 main.py -m page -s 301 -e 301
```

含义：根据`页面ID`下载，从`301`下载到`301`（仅下载第`301`页的图片）。

##### 示例六

```shell
python3 main.py -m page -s 123 -e 456
```

含义：根据`页面ID`下载，从`123`下载到`456`（下载所在位置在`[123,456]`区间页中的图片）。

##### 示例七

```shell
python3 main.py -m page -s 123 -e -1
```

含义：根据`页面ID`下载，从`123`下载到`最后一页`（下载所在位置大于等于第`123`页中的图片）。

##### 示例八

```shell
python3 main.py -m page -s 1 -e -1
```

含义：根据`页面ID`下载，从`1`下载到`最后一页`（下载所在位置大于等于第`1`页的图片，即`全部下载`）。

#### `update`模式

##### 示例九

```shell
python3 main.py -m update
```

含义：更新脚本。

##### 示例十

```shell
python3 main.py -m update -p "./downloader" -P "http://username:password@127.0.0.1:8080"
```

含义：更新脚本，日志保存到当前目录下名为`downloader`的目录（如不存在则自动创建），使用 HTTP 代理：`http://username:password@127.0.0.1:8080`。

#### `file`模式

**配置文件的`键`（`key`）均需使用`长命令`，且`-`应被替换为`_`。当指定为`file`模式时，配置文件的优先级最高。当配置文件内未提供参数的值或值为空字符串时，使用命令行传入的参数的值，如果命令行仍未指定，使用默认值。**

##### 示例十一

```shell
python3 main.py -m file "--file-config-path" "./config.json"
```

与此同时，`./config.json`的内容：

```text
{
    "args": {
		"mode": "page",
		"start": 1,
		"end": 5,
		"limit": 5,
		"tags": "angel+-tagme+tail+-ass",
		"thread": 5,
		"path": "./downloader",
		"proxy": "http://username:password@127.0.0.1:8080",
		"options": "chksums",
        "file_config_path": "",
        "retry_max": "20"
    }
}
```

含义：以配置文件中的配置运行。

配置文件含义：根据`页面ID`下载，下载所在位置大于等于第`1`页且小于等于第`5`页的图片，下载后校验文件完整性，每次获取`5`个帖子（图片），只获取标签中包含`["angel", "tail"]`且不包含`["tagme", "ass"]`的帖子，`5`线程下载，下载到当前目录下名为`downloader`的目录（如不存在则自动创建），使用 HTTP 代理：`http://username:password@127.0.0.1:8080`，超时重试`20`次。

##### 示例十二

```shell
python3 main.py -m file "--file-config-path" "./config.json" -p "./yande" -l 100 -o "chksums" -e 100
```

与此同时，`./config.json`的内容：

```text
{
    "args": {
		"mode": "page",
		"start": 1,
		"end": 5,
		"limit": null,
		"tags": "angel+-tagme+tail+-ass",
		"thread": 5,
		"proxy": "http://username:password@127.0.0.1:8080",
		"options": "",
		"file_config_path": "",
        "retry_max": ""
}
```

含义：以配置文件中的配置运行，下载到到当前目录下名为`yande`的目录（如不存在则自动创建），每次获取`100`个帖子（图片），下载后校验文件完整性，**但指定的`结束ID`将不会生效**。

配置文件含义：根据`页面ID`下载，下载所在位置大于等于第`1`页且小于等于第`5`页的图片，只获取标签中包含`["angel", "tail"]`且不包含`["tagme", "ass"]`的帖子，`5`线程下载，使用 HTTP 代理：`http://username:password@127.0.0.1:8080`。

#### 其他参数

##### 示例十三

```shell
python3 main.py -m page -s 1 -e -1 -l 100 -t "angel+-tagme+tail+-ass" -T 4 -p "./downloader" -P "http://username:password@127.0.0.1:8080" -o "chksums" --retry-max -1
```

也可以选择不使用短写参数：

```shell
python3 main.py --mode page --start 1 --end -1 --limit 100 --tags "angel+-tagme+tail+-ass" --thread 4 --path "./downloader" --proxy "http://username:password@127.0.0.1:8080" --options "chksums" --retry-max -1
```

含义：根据`页面ID`下载，下载所在位置大于等于第`1`页的图片（即`全部下载`），下载后校验文件完整性，每次获取`100`个帖子（图片），只获取标签中包含`["angel", "tail"]`且不包含`["tagme", "ass"]`的帖子，`4`线程下载，下载到当前目录下名为`downloader`的目录（如不存在则自动创建），使用 HTTP 代理：`http://username:password@127.0.0.1:8080`，取消失败重试次数限制直到下载成功。

##### 示例十四

```shell
python3 main.py -m id
python3 main.py -m page
```

含义：当只指定下载模式时，其他参数将均使用**默认值**，即：开始 ID 与结束 ID 均为`1`，每次获取`1000`个帖子（图片），不指定/排除标签，`5`线程下载，下载到当前目录下名为`img`的目录（如不存在则自动创建），不使用 HTTP 代理。

##### 示例十五

```shell
python3 main.py -m file -o make-config "--file-config-path" "./cfg.json"
```

含义：在当前目录下生成一个空白的配置文件，命名为`cfg.json`。

---

## 常见问题

### ModuleNotFoundError: No module named 'xxxxxx'

使用`pip install`命令下载对应的库即可。

---

## 更新日志

### V1.5.1

1. 代码规范性改进。
2. 添加了生成空白配置文件功能。
3. 添加了自定义最大失败重试次数功能。
4. 修改了参数格式及帮助信息。

### V1.4.1

1. 添加了使用配置文件进行下载功能。
2. 添加了校验文件完整性功能。
3. 修改了命令行参数格式及帮助信息。

### V1.3.4

1. 代码规范性改进。
2. 调整了目录结构。
3. 完善了运行时的状态信息。

### V1.3.1

1. 重写了日志模块（修复了日志记录可能不完整的 bug、添加了根据日志类型在控制台输出日志颜色）。

### V1.2.5

1. 美化代码，更换更新接口。

### V1.2.0

1. 修改了通过图片 ID 区间下载时获取图片列表的方法，不再使用估算值。

### V1.1.1

1. 修改了代码逻辑：将图片链接添加到下载列表前判断 file_url 键是否存在。

### V1.1.0

1. 添加了在线更新功能。
2. 修改了帮助信息。

### V1.0.3

1. 添加了错误处理。
2. 修改了下载器判断下载任务完成的逻辑，减少卡死几率。

### V1.0.1

1. 添加了版权信息。

### V1.0.0

1. 正式版上线。
