# wxtopdf
## 根据公众号ID，爬取公众号的文章列表，并保存文章为html/pdf

经过调研，目前保存微信公众号的文章有三个思路，一是使用微信搜狗借口，二是使用微信公众号平台，三是使用客户端+代理的方式。
本方法使用的是微信公众号平台的方式：
1. 由于微信官方的限制,公众号每天最大访问量1000个请求,且每小时也有最大访问量限制,访问频率过快就会被封号24小时
2. bizNameLists 是要访问的公众号列表
3. 账号密码是自己注册的微信公众号平台,注册地址是 https://mp.weixin.qq.com/
4. 启动此脚本需要使用与本机浏览器适配的 dirve,比如chrome drive,或者Firefox drive, https://mirrors.huaweicloud.com/chromedriver/
