from threading import Thread
from apps.auto_chrome import AutoChrome

t1 = Thread(target=AutoChrome('pro', 'form').formTest, daemon=True)
t2 = Thread(target=AutoChrome('pro', 'baidu').baiduTest, daemon=True)
t3 = Thread(target=AutoChrome('pro', 'verifyCode').verifyCodeTest, daemon=True)

tasks = [t1, t2, t3]

for t in tasks:
    t.start()

for t in tasks:
    t.join()
