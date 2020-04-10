from socket import *
import _thread,os,sys

download_speed_max = 9999

def download():
    size = 0
    file_name = input("下载的文件(包括文件后缀 test.mp4)：")
    if file_name != "":
        client.send(file_name.encode())
        file = open("out/" + file_name, 'ab')
        while True:
            data = client.recv(download_speed_max)
            if not data:
                print("下载完成。")
                file.close()
                client.close()
                break
            file.write(data)
            mb = sys.getsizeof(data) / 1000000
            size += mb
            print("已经下载："+str(round(size,2))+"mb.")



def get_files():
    print("获取文件列表中...")
    client.send("download".encode())
    files = []
    data = client.recv(download_speed_max).decode()
    files = data.split("#")
    print("文件列表获得成功。")
    print("目前可下载文件：")
    for name in files:
        print(name)


def update():
    size = 0
    input("请将上传的文件放在update文件夹中，然后按 任意键 继续...")
    files = os.listdir("update/")
    print("欲上传的文件："+files[0])
    input("按 任意键 继续...")
    code = "update".encode()
    client.send(code)
    print("已向服务器发送上传信息。")
    client.recv(1024)
    print("服务器反馈成功，开始上传文件。")
    client.send(files[0].encode())
    file = open("update/"+files[0],"rb")
    for data in file:
        client.send(data)
        mb = sys.getsizeof(data) / 1000000
        size += mb
        print("已经上传："+str(round(size,2))+"mb.")
    print("文件上传成功。")
    client.close()



def del_file():
    print("发送删除请求中...")
    client.send("del".encode())
    print("等待服务器反馈。")
    client.recv(1024)
    del_file_name = input("服务器反馈成功，请输入欲删除的文件:")
    client.send(del_file_name.encode())
    print("删除命令已经发送，等待服务器反馈。")
    client.recv(1024)
    print("文件成功删除。")


if __name__ == '__main__':
    #设置服务器信息
    host = "127.0.0.1"
    port = 5555
    addr = (host,port)
    while True:
        # 连接服务器
        print("正在连接服务器...")
        client = socket(AF_INET, SOCK_STREAM)
        client.connect(addr)
        print("成功连接到服务器。")
        code = input("[1]下载文件 [2]上传文件 [3]删除文件")
        if code == "1":
            get_files()
            download()
        elif code == "2":
            update()
        elif code == "3":
            del_file()