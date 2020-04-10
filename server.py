from socket import *
import _thread,os,time

connect_users = []
files = []
server_update_max = 99999

def server_meg():
    files = os.listdir("data/")
    return files

def user_download(skt,user):
    print(str(user[0])+"加入文件下载函数。")
    try:
        while True:
            file_name = skt.recv(1024).decode()
            if file_name not in files:
                print(str(user[0])+"请求不存在的文件，已经驳回。")
                skt.close()
                print("自动停止对方连接。")
            else:
                file_data = open("data/"+file_name,"rb")
                print(file_data)
                for data in file_data:
                    skt.send(data)
                print("成功向"+str(user[0])+"发送文件："+file_name)
                skt.close()
                print("退出下载进程。")
                connect_users.remove(skt)
                break
    except:
        print(str(user[0]) + "断开连接。")
        skt.close()


def user_update(skt,user):
    try:
        skt.send("ready".encode())
        file_name = skt.recv(1024).decode()
        file_update = open("data/"+file_name,"ab")
        while True:
            data = skt.recv(server_update_max)
            if not data:
                print(str(user[0])+" 文件上传成功："+file_name)
                skt.close()
                connect_users.remove(skt)
                break
            file_update.write(data)
    except:
        print(str(user[0])+"在上传文件时连接丢失。")
        skt.close()


def user_del(skt,user_meg):
    try:
        skt.send("ready".encode())
        file_name = skt.recv(1024).decode()
        print("正在删除文件："+file_name)
        os.remove(("data\ "+file_name).replace(" ",""))
        print("文件删除成功。")
        skt.send("del over".encode())
    except:
        print(str(user_meg[0])+" 删除不存在的文件，已经驳回。")
        skt.close()



def user_re(skt,user_meg):
    global files
    try:
        while True:
            code = skt.recv(1024).decode()
            if code == "download":
                print(str(user_meg[0])+" 发送文件下载请求。")
                files = server_meg()
                all = ""
                for data in files:
                    all += data +"#"
                skt.send(all.encode())
                print("已发送文件列表。")
                user_download(skt,user_meg)
            elif code == "update":
                print(str(user_meg[0])+" 发送文件上传请求")
                user_update(skt,user_meg)
            elif code == "del":
                print(str(user_meg[0]) + " 发送文件删除请求")
                user_del(skt,user_meg)
    except:
        print(str(user_meg[0])+"断开连接。")
        skt.close()



def wait_user(server):
    global connect_users
    print("等待客户端连入...")
    try:
        while True:
            skt,user_meg = server.accept()
            print(str(user_meg[0])+"连接到服务器。")
            _thread.start_new_thread(user_re,(skt,user_meg))
            print("成功为"+str(user_meg[0])+"创建用户处理进程。")
            connect_users.append(skt)
            print("客户已经加入到列表中。")
    except:
        print("创建进程时发生错误，已经修复。")


if __name__ == '__main__':
    #设置服务器信息
    host = "127.0.0.1"
    port = 5555
    addr = (host,port)
    max_users = 20
    print("服务器配置设置完毕。")
    #创建服务器
    server = socket(AF_INET, SOCK_STREAM)
    server.bind(addr)
    server.listen(max_users)
    print("服务器创建完毕。")
    wait_user(server)

