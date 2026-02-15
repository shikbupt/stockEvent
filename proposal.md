# 方案设计

## 目标

通过`github action` 定时生成股市事件的ics日历数据, 用于日历client的订阅.

## 要求
- 编程语言是 Python
- `github action` 每天凌晨1点运行

## 方案

### 数据源
数据源 URL: `https://calendar-api.fxsstatic.com`
数据源 Path: `/en/api/v2/eventDates/2026-02-15T03:20:55Z/2026-02-17T05:20:55Z`
> Path其中的日期表示event的起始日期

数据源 Query: 

| 参数         | 含义   | 取值                 |
|--------------|--------|----------------------|
| volatilities | 重要性 | NONE,LOW,MEDIUM,HIGH |
| countries    | 国家   | US,JP                |
| categories   | 类别   | 见下备注             |

> 类别代码:
8896AA26-A50C-4F8B-AA11-8B3FCCDA1DFD Bond Auctions
FA6570F6-E494-4563-A363-00D0F2ABEC37 Capital Flows
C94405B5-5F85-4397-AB11-002A481C4B92 Central Banks
E229C890-80FC-40F3-B6F4-B658F3A02635 Consumption
24127F3B-EDCE-4DC4-AFDF-OB3BD8A964BE Economic Activity
DD332FD3-6996-41BE-8C41-33F277074FA7 Energy
7DFAEF86-C3FE-4E76-9421-8958CC2F9A0D Holidays
1E06A304-FAC6-440C-9CED-9225A6277A55 Housing Market
33303F5E-1E3C-4016-AB2D-AC87E98F57CA Inflation
9C4A731A-D993-4D55-89F3-DC707CC1D596 Interest Rates
91DA97BD-D94A-4CE8-A02B-B96EE2944E4C Labor Market
E9E957EC-2927-4A77-AE0C-F5E4B5807C16 Politics

>举例: 获取2026-02-15T03:47:11Z到2026-02-17T05:47:11Z时间内,美国和日本所有重要性和类别的财经事件
https://calendar-api.fxsstatic.com/en/api/v2/eventDates/2026-02-15T03:47:11Z/2026-02-17T05:47:11Z?&volatilities=NONE&volatilities=LOW&volatilities=MEDIUM&volatilities=HIGH&countries=US&countries=JP&categories=8896AA26-A50C-4F8B-AA11-8B3FCCDA1DFD&categories=FA6570F6-E494-4563-A363-00D0F2ABEC37&categories=C94405B5-5F85-4397-AB11-002A481C4B92&categories=E229C890-80FC-40F3-B6F4-B658F3A02635&categories=24127F3B-EDCE-4DC4-AFDF-0B3BD8A964BE&categories=DD332FD3-6996-41BE-8C41-33F277074FA7&categories=7DFAEF86-C3FE-4E76-9421-8958CC2F9A0D&categories=1E06A304-FAC6-440C-9CED-9225A6277A55&categories=33303F5E-1E3C-4016-AB2D-AC87E98F57CA&categories=9C4A731A-D993-4D55-89F3-DC707CC1D596&categories=91DA97BD-D94A-4CE8-A02B-B96EE2944E4C&categories=E9E957EC-2927-4A77-AE0C-F5E4B5807C16


Header:
> Accept: application/json
Accept-Encoding: gzip, deflate, br
Accept-Language: zh-CN,zh-Hans;q=0.9
Origin: https://www.fxstreet.com
Priority: u=3, i
Referer: https://www.fxstreet.com/
Sec-Fetch-Dest: empty
Sec-Fetch-Mode: cors
Sec-Fetch-Site: cross-site
User-Agent: Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/26.2 Safari/605.1.15

### 数据存储
1. 利用数据源的api获取原始数据存储在文件夹`event`中,event下文件结构如下:
>event
├── JP                   //按国家分类
│   ├── 2016-01
│   │   ├── 2016-01-01  //文本文件,按日期存具体时间
│   │   └── 2016-01-02
│   └── 2016-02
│       ├── 2016-01-01
│       └── 2016-01-02
└── US
    ├── 2016-01
    │   ├── 2016-01-01
    │   └── 2016-01-02
    └── 2016-02
        ├── 2016-01-01
        └── 2016-01-02

2. 根据上述原始数据生成ics数据,按国家粒度进行生成, 如US.ics, JP.ics
用context7使用ICS-Py实现.

### 运行逻辑
1. 项目需要配置文件,可以配置如下重要参数:
- 时间范围
- 国家
- 事件的重要性
- 事件类别
2. 每天凌晨1点, `github action`触发,action中需要做以下事情:
   - 通过数据源api获取原始数据,api中的参数来自于1中的配置文件
   - 获取原始数据后,根据event文件下所有的数据,生成所需要的ics文件
   - 将event及生成的ics文件`git add`进入git仓库管理

