from ast import walk
import tkinter as tk
import shutil,datetime,configparser,re,requests,os,base64
from tkinter.font import BOLD
from icon import img
from tkinter import messagebox as tkbox


path1 = "Z:/Favorite.ini"  #堯乾贏家自選股檔案路徑_NAS
path2 = "Z:/SymbolList.xml" #嘉實XQ自選股檔案路徑_NAS


#自選股檔案判斷是否存在
def check_the_file():
    if btn1str.get() == "檢查":
        if os.path.exists(path1):
            tk.Label(win, textvariable = dsustr,fg="Green", font=('標楷體', 15, BOLD), width=7).place(x=120, y=15)
            dsustr.set("檔案存在")
        else:
            tk.Label(win, textvariable = dsustr,fg="Red", font=('標楷體', 15, BOLD), width=7).place(x=120, y=15)
            dsustr.set("檔案不在")
            tkbox.showerror("錯誤訊息","請檢查網路磁碟或檔案")
        if os.path.exists(path2):
            tk.Label(win, textvariable = xqstr,fg="green", font=('標楷體', 15, BOLD), width=7).place(x=120, y=80)
            xqstr.set("檔案存在")
        else:
            tk.Label(win, textvariable = xqstr,fg="red", font=('標楷體', 15, BOLD), width=7).place(x=120, y=80)
            xqstr.set("檔案不在")
            tkbox.showerror("錯誤訊息","請檢查網路磁碟或檔案")

#自選股上傳
def upload_file():
    nowtime = datetime.datetime.now().strftime("%Y%m%d-%H%M")
    De_Stack = "C:/Syspower/Deimos/A123/Template/MSimpleSelfSel/" #堯錢贏家自選股路徑_本機
    XQ_Stack = "C:/SysJust/XQ2005/User/TACHAN-17/Data/" #XQ自選股路徑_本機
    
    #堯乾贏家 自選股備份 重新命名加上日期
    dsusort = 'ini'
    for root, dirs, files in os.walk(De_Stack):
        for file in files:
            if file.split('.')[1] == dsusort:
                source = De_Stack + 'Favorite.ini'
                DePath = source
                destination = 'Z:/bak/' + str(nowtime) + '_' + 'Favorite.ini'
                shutil.copy(source, destination)

    #讀取堯乾贏家自選股股票代碼添加.TW
    DeimosConf = configparser.ConfigParser()
    DeimosConf.read(source)

    DeimosText = DeimosConf['自選群組']['自選 1']
    stock_id = DeimosText.split(',')
    stock_xq = ".TW,".join(stock_id)

    #XQ自選股 替換
    XQPath = XQ_Stack + 'SymbolList.xml'
    XQnew = '    <List ID="9E55ECC3-6F66-4389-8369-C6D98D0075A5" Name="MASTER" Value="'+ stock_xq + '.TW" Flag="0" SortIdx="1" Version="1" />\n'
    with open(XQPath, "r") as file: #讀取第四行資料暫存在XQold
        XQold = file.readlines()[3]

    with open(XQPath, "r") as file: #讀取全文
        x = file.read()

    with open(XQPath, "w") as file: #替換第四行資料
        x = x.replace(XQold,XQnew).replace("FITX1.TW", "FITX1.TF")
        file.write(x)
        
    #嘉實XQ 自選股備份 重新命名加上日期
    xqsort = 'xml'
    for root, dirs, files in os.walk(XQ_Stack):
        for file in files:
            if file.split('.')[1] == xqsort:
                source = XQ_Stack + 'SymbolList.xml'
                destination = 'Z:/bak/' + str(nowtime) + '_' + 'SymbolList.xml'
                shutil.copy(source, destination)
              
    #Copy嘉實XQ自選股 To 好神通自選股
    shutil.copy(source,'C:/SINOAP/User/Data/SymbolList.xml') #好神通自選股
    
    #堯錢贏家&嘉實XQ 自選股 Copy To NAS(老闆專用資料夾)
    shutil.copy(DePath,'Z:/') #堯錢贏家 自選股
    shutil.copy(XQPath,'Z:/') #嘉實XQ 自選股
    

    #手機自選股上傳
    DeimosPath = open("C:/Syspower/Deimos/A123/Template/MSimpleSelfSel/Favorite.ini", "r")
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

    if(iphone_code.status_code == 200):
        tkbox.showinfo("訊息","上傳完成")
    else:
        tkbox.showerror("訊息","上傳失敗")

#圖形化介面框架
win = tk.Tk()
win.title('自選股上傳')
win.geometry('310x140') #視窗尺寸
win.resizable(False, False)
win.configure(background="#F0F0F0") #背景顏色

ico = open("1.ico", 'wb+')
ico.write(base64.b64decode(img))
ico.close()
win.iconbitmap('1.ico') #標題小圖示
os.remove('1.ico')

#檢查檔案的框架
tk.Label(win, text="堯乾贏家：", font=('標楷體', 15, BOLD)).place(x=15, y=15)

dsustr = tk.StringVar()
dsu = tk.Label(win, textvariable = dsustr, font=('標楷體', 15, BOLD), width=7).place(x=120, y=15)
dsustr.set("未知")


tk.Label(win, text="嘉 實 XQ：", font=('標楷體', 15, BOLD)).place(x=15, y=80)
tk.Label(win, text="Ver: 2022.06.29", font=('標楷體', 10)).place(x=15, y=120)

xqstr = tk.StringVar()
xq = tk.Label(win, textvariable = xqstr, font=('標楷體', 15, BOLD), width=7).place(x=120, y=80)
xqstr.set("未知")

btn1str = tk.StringVar()
btn1 = tk.Button(win, textvariable = btn1str, command=check_the_file, font=('標楷體', 15, BOLD)).place(x=220, y=15)
btn1str.set("檢查")

#自選股檔案上傳的框架
btn2str = tk.StringVar()
btn2 = tk.Button(win, textvariable = btn2str, command=upload_file, font=('標楷體', 15, BOLD)).place(x=220, y=80)
btn2str.set("上傳")

win.mainloop()