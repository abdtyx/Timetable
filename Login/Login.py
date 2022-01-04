# coding=utf-8

# 登录ehall
# @params: 账号密码
# @return: Session变量

# 调试变量
import requests
import json
debug = False
def LoginEhall(userinfo, s):
    auth_info = {
        "loginType" : 1,
        "username" : userinfo['netid'],
        "pwd" : userinfo['password'],
        "jcaptchaCode" : ""
    }
    print("Logining...")
    r = s.get("http://ehall.xjtu.edu.cn/jwapp/sys/wdkb/*default/index.do#/wdkb", allow_redirects=False)
    url = r.headers['Location']
    if debug:
        print("Goto:" + url)
    r = s.get(url, allow_redirects=False)
    url = r.headers['Location']
    if debug:
        print("Goto:" + url)
    s.get(url)
    r = s.post("http://org.xjtu.edu.cn/openplatform/g/admin/login", json=auth_info, allow_redirects=False)
    if debug:
        print(r.text)
    logindata = json.loads(r.text)
    userinfo['memberId'] = str(logindata['data']['orgInfo']['memberId'])
    s.cookies.set("memberId", userinfo['memberId'])
    s.cookies.set("open_Platform_User", logindata['data']['tokenKey'])
    r = s.get("http://org.xjtu.edu.cn/openplatform/g/admin/getUserIdentity?memberId=" + userinfo['memberId'])
    if debug:
        print(r.text)
    r = s.get("http://org.xjtu.edu.cn/openplatform/oauth/auth/getRedirectUrl?userType=1&personNo=" + str(userinfo['netid']), headers = {"Referer" : "http://org.xjtu.edu.cn/openplatform/login.html"})
    if debug:
        print(r.text)
    url = json.loads(r.text)['data']
    if debug:
        print("Goto:" + url)
    s.get(url)
    # r = s.get("http://ehall.xjtu.edu.cn/appMultiGroupEntranceList?r_t=1634137905928&appId=4768574631264620&param=",allow_redirects=False)
    r = s.get("http://ehall.xjtu.edu.cn/appMultiGroupEntranceList?r_t=1634137905928&appId=4770397878132218&param=",allow_redirects=False)
    if debug:
        print("select_role:",r.text)
    nurl = json.loads(r.text)['data']['groupList'][0]['targetUrl']
    r = s.get("http://ehall.xjtu.edu.cn/portal/html/select_role.html?appId=4770397878132218")
    if debug:
        print(r.status_code)
    # r = s.get("http://ehall.xjtu.edu.cn/jwapp/sys/wdkb/*default/index.do?amp_sec_version_=1&gid_=S3dzUjIyZ1lnbzdra0gwMk1BaWwwUkpQUHp1VlY3MHRiWDNpRW9FeU9qb2tSUDhKbStqUVlxZllYR2YxU1doRmFTdlpnVWhWUWxRamtieUxvZE1rZEE9PQ&EMAP_LANG=zh&THEME=millennium#/xskcb")
    r = s.get(nurl)
    if debug:
        print(r.status_code)
    return s