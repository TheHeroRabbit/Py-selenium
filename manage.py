from threading import Thread
from apps.auto_chrome import AutoChrome


t1 = Thread(target=AutoChrome('dev', '').formTest, daemon=True)
t2 = Thread(target=AutoChrome('dev', 'baidu').baiduTest, daemon=True)
t3 = Thread(target=AutoChrome('dev', 'verifyCode').verifyCodeTest, daemon=True)

tasks = [t1, t2, t3]

for t in tasks:
    t.start()

for t in tasks:
    t.join()
