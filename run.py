from flask import (
    Flask,request,render_template
    )
import feature
from icann import whoisurl
from nlink import nlink

def Features(url): 
    status = []
    status.append(feature.having_ip_address(url))
    status.append(feature.abnormal_url(url))
    status.append(feature.count_dot(url))
    status.append(feature.count_www(url))
    status.append(feature.count_atrate(url))
    status.append(feature.no_of_dir(url))
    status.append(feature.no_of_embed(url))
    status.append(feature.shortening_service(url))
    status.append(feature.count_https(url))
    status.append(feature.count_http(url))
    status.append(feature.count_per(url))
    status.append(feature.count_ques(url))
    status.append(feature.count_hyphen(url))
    status.append(feature.count_equal(url))
    status.append(feature.url_length(url))
    status.append(feature.hostname_length(url))
    status.append(feature.suspicious_words(url))
    status.append(feature.digit_count(url))
    status.append(feature.letter_count(url))
    status.append(feature.fd_length(url))
    status.append(feature.tld_length(url))
    status.append(feature.google_index(url))
    return status

app=Flask(__name__)

@app.route('/')
def get_html():
    return render_template('url.html')

@app.route('/result',methods = ['GET'])
def print_result():
    url=request.values.get('url')
    page = request.values.get('page')
    print(page)
    if page == '1':
        who = whoisurl(url)
        data = []
        for x,y in who.items():
            data.append({'topic':x, 'name':y})
        return render_template('result1.html',data=data,url=url)
    elif page == '2':
        data = nlink(url)
        return render_template('result2.html',
                               url=url,
                               data=data)
    else:
        fe = Features(url)
        ans = '良好'
        data=[
            {'name':fe[0],'topic':'having_ip_address','disc':'通常攻擊者會利用ip來替代網域，以此來隱藏網站身分。本組利用正規表示式來進行檢查，並且其中的 ip 有包括 ipv4 和 ipv6'},
            {'name':fe[1],'topic':'abnormal_url','disc':'對於合法網站，身份通常是其 URL的一部分。'},
            {'name':fe[21],'topic':'google_index','disc':'由於釣魚網站只能在短時間間內訪問，所以很多釣魚網頁無法在 Google 索引中找到，本組利用此特性檢查網址是否有被google編入索引'},
            {'name':fe[2],'topic':'count\'.\'','disc':'網路釣魚或惡意軟體網站通常在 URL 中使用多個以上的子域。每個域用點（.）分隔，因此本組去數每個 URL 中的點（.）個數來得知他有幾個子域'},
            {'name':fe[3],'topic':'count_www','disc':'大多數安全網站的URL中都有一個 www，所以如果網址中沒有或包含多個 www 則很有可能為惡意網站'},
            {'name':fe[5],'topic':'count_dir','disc':'URL 中存在多個目錄通常表示可疑網站，因此本組去數斜線（/）的數量來得知此 URL 有幾層目錄'},
            {'name':fe[8],'topic':'count_https','disc':'通常惡意 URL 不使用 HTTPS 協議，因為憑證頒發機構僅信任合法的網站'},
            {'name':fe[11],'topic':'count?','disc':'URL 中問號（?） 的存在表示 URL 將要傳遞變數到伺服器，而更多數量的問號（?）表示其越有可能為可疑的網址。若由直方圖來看，count? 此特徵在 defacement 中特別明顯'},
            {'name':fe[13],'topic':'count=','disc':'URL 中存在等於（=）表示變數值將送出表單，這樣會增加風險，因為任何人都可以更改值來修改頁面。'},
            {'name':fe[14],'topic':'url_length','disc':'攻擊者通常使用較長的 URL 讓域名較不顯眼，以此達到隱藏的效果'},
            {'name':fe[15],'topic':'hostname_length','disc':'主機名的長度也是檢測惡意 URL 的重要功能。'},
            {'name':fe[17],'topic':'digit_count','disc':'安全 URL 通常沒有數字，因此計算 URL 中的數字是檢測惡意 URL 的重要功能。'},
            {'name':fe[18],'topic':'letter_count','disc':'當攻擊者試圖增加 URL 的長度以隱藏域名時，通常會伴隨著增加URL中的字母和位數'},
            {'name':fe[20],'topic':'Length of top-level domains','disc':'範圍為2到3的 TLD 通常表示安全 URL，越下層的域表示其安全性可能越低'},
            ]
        return render_template('result0.html',ans=ans,data=data,url=url)



# class="nav-link" aria-current="page" href=""

if __name__=='__main__':
    app.run('0.0.0.0',5000,debug=True)