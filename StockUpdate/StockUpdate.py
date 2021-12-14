import tkinter as tk
import shutil,datetime,configparser,re,requests,os,base64
from tkinter.font import BOLD
from icon import img
from tkinter import messagebox as tkbox


path1 = "z:/Favorite.ini"  #堯乾贏家自選股檔案路徑
path2 = "z:/SymbolList.xml" #嘉實XQ自選股檔案路徑


#自選股檔案判斷是否存在
def check_the_file():
    if btn1str.get() == "檢查":
        if os.path.exists(path1):
            dsustr.set("檔案存在")
        else:
            dsustr.set("檔案不在")
        if os.path.exists(path2):
            xqstr.set("檔案存在")
        else:
            xqstr.set("檔案不在")
            tkbox.showerror("錯誤訊息","請檢查網路連線或網路磁碟")

#自選股上傳
def upload_file():
    #堯乾贏家&嘉實XQ 自選股 本機 To 網路磁碟
    shutil.copy('C:/Users/Tachan-MIS/Documents/Deimos(Broker)/A123/Template/MSimpleSelfSel/Favorite.ini' ,'z:/Favorite.ini') #堯乾贏家自選股
    shutil.copy('C:/SysJust/XQ2005/User/Data/SymbolList.xml' ,'z:/SymbolList.xml') #嘉實XQ自選股

    #堯乾贏家&嘉實XQ 自選股備份 重新命名加上日期
    nowtime = datetime.datetime.now().strftime("%Y%m%d-%H%M")
    dir = "z:/"
    xqsort = 'xml'
    dsusort = 'ini'
    for dirs, files in os.walk(dir):
        if 'bakup' in dirs:
            dirs.remove('bakup')
            for file in files:
                if file.split('.')[1] == xqsort and dsusort:
                    shutil.copy(src=f'z:/SymbolList.xml', dst=f'z:/bakup/' + str(nowtime) + '_' + 'SymbolList.xml' )
                    shutil.copy(src=f'z:/Favorite.ini', dst=f'z:/bakup/' + str(nowtime) + '_' + 'Favorite.ini' )

    #讀取堯乾贏家自選股股票代碼添加.TW
    DeimosConf = configparser.ConfigParser()
    DeimosConf.read('z:/Favorite.ini')

    DeimosText = DeimosConf['自選群組']['自選 1']
    stock_id = DeimosText.split(',')
    stock_xq = ".TW,".join(stock_id)

    #XQ自選股 替換
    XQPath = "z:/SymbolList.xml"
    XQnew = '    <List ID="9E55ECC3-6F66-4389-8369-C6D98D0075A5" Name="MASTER" Value="'+ stock_xq + '.TW" Flag="0" SortIdx="1" Version="1" />\n'
    with open(XQPath, "r") as file: #讀取第四行資料暫存在XQold
        XQold = file.readlines()[3]

    with open(XQPath, "r") as file: #讀取全文
        x = file.read()

    with open(XQPath, "w") as file: #替換第四行資料
        x = x.replace(XQold,XQnew).replace("FITX1.TW", "FITX1.TF")
        file.write(x)

    #手機自選股上傳
    DeimosPath = open("z:/Favorite.ini", "r")
    line = DeimosPath.readlines()[1]
    line = re.sub("自選 1=","",line) #刪除字元
    iphone_stock_group = ""
    if(line != ""):
        stock = line.split(',')
        iphone_count = 0
        iphone_group_count = 1
        for s in stock:
            if(iphone_count == 30):
                iphone_count = 0
                iphone_group_count += 1
            if(iphone_count < 30):
                if(iphone_count == 0):
                    iphone_stock_group += "G" + str(iphone_group_count) + "="
                iphone_count += 1
                if(iphone_count != 30):
                    iphone_stock_group += s + ","
                else:
                    iphone_stock_group += s + "&"

    #傳送自選股API
    iphone_stock = iphone_stock_group[:-1] #刪除最後一個字元
    iphone_url = "http://pda.mitake.com.tw/api/tacvip.asp?org=IPHONE&" #手機
    ipad_url = "http://pda.mitake.com.tw/api/tacvip.asp?org=IPAD&" #平板
    
    stock_iphone = iphone_url + iphone_stock
    iphone_code = requests.get(stock_iphone)
    

    stock_ipad = ipad_url + iphone_stock
    requests.get(stock_ipad)

    if(iphone_code == 200):
        upstr.set('上傳成功')
    else:
        upstr.set('上傳失敗')



#圖形化介面框架
win = tk.Tk()
win.title('自選股上傳')
win.geometry('250x200') #視窗尺寸
win.resizable(False, False)
win.configure(background="#F0F0F0") #背景顏色

ico = open("1.ico", 'wb+')
ico.write(base64.b64decode(img))
ico.close()
win.iconbitmap('1.ico') #標題小圖示
os.remove('1.ico')


#檢查檔案的框架
lab1 = tk.Label(win, text="堯乾贏家：", font=('微軟正黑體', 11))
lab1.grid(column=0, row=0, pady=10, sticky=tk.N+tk.W)

dsustr = tk.StringVar()
dsu = tk.Label(win, textvariable = dsustr, font=('微軟正黑體', 11, BOLD), width=7)

dsustr.set("未知")
dsu.grid(column=0, row=0, padx=80, pady=10, sticky=tk.N+tk.W)



lab2 = tk.Label(win, text="嘉實XQ：", font=('微軟正黑體', 11))
lab2.grid(row=0,column=0, pady=35, sticky=tk.N+tk.W)

xqstr = tk.StringVar()
xq = tk.Label(win, textvariable = xqstr, font=('微軟正黑體', 11, BOLD), width=7)

xqstr.set("未知")
xq.grid(row=0,column=0, pady=35, padx=80, sticky=tk.N+tk.W)

btn1str = tk.StringVar()
btn1 = tk.Button(win, textvariable = btn1str, command=check_the_file)
btn1str.set("檢查")
btn1.grid(row=0, column=0, padx=150, ipadx=30, ipady=30)

#自選股檔案上傳的框架
upstr = tk.StringVar()
up = tk.Label(win, textvariable = upstr, font=('微軟正黑體', 11, BOLD), width=7)

upstr.set("尚未上傳")
up.grid(row=1,column=0, pady=25, padx=30, sticky=tk.N+tk.W)

btn2str = tk.StringVar()
btn2 = tk.Button(win, textvariable = btn2str, command=upload_file)
btn2str.set("上傳")
btn2.grid(row=1, column=0, padx=150, ipadx=30, ipady=30)

win.mainloop()
