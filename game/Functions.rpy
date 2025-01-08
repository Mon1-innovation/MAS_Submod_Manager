init python:#这里写本地增删mod涉及到的函数
    import os 
    import _renpytfd
    import main
    def MAS_Basedir_Choose():
        fliter_list = ["MAS启动文件","DDLC.exe"]#过滤器得是列表形式的，第一个是描述，第二个是具体条件
        fileName_choose = _renpytfd.openFileDialog("请在本窗口选择您的MAS启动文件（DDLC.exe）","C:\"" ,fliter_list, None)#第一个参数是窗口标题，第二个参数是窗口起始路径，第三个参数是过滤器变量（好像不能直接写个列表在这里面）第四个咱也不知道干什么用的直接空着没写
        #切记，四个变量哪怕有空也不能少任何一个，不然直接给你爆！！！掉
        if fileName_choose == None:#如果这个傻逼一个文件没选就右上角报错，报错内容详见script.rpy，写这里会renpy炸掉
            persistent.notify_choice = 1
        else:
            if fileName_choose.find("DDLC.exe") != -1:
                persistent.mas_basedir = fileName_choose[:-8].replace('\\', '/')
                persistent.mas_submod_dir = persistent.mas_basedir + "game/Submods/"
                if not os.path.isdir(persistent.mas_submod_dir):
                    persistent.notify_choice = 4#如果这个傻逼没有装submod或者选错了DDLC.exe就右上角报错，报错内容详见script.rpy，写这里会导致renpy炸掉
                    return
                persistent.mas_mod_assets_dir = persistent.mas_basedir + "game/mod_assets/"
                persistent.notify_choice = 2#如果这个用户选对了路径就提示正确然后在设置里写上当前路径
            else:
                persistent.notify_choice = 3#如果这个傻逼选了一个非DDLC.exe的文件那就报错说他选的不是DDLC.exe
    def Submod_Choose_1():#通过压缩文件安装
        fliter_list = ["其中一种压缩包格式","**.7z"]#过滤器得是列表形式的，第一个是描述，第二个是具体条件
        fileName_choose = _renpytfd.openFileDialog("请在本窗口选择您要安装的Submod文件（仅支持zip，rar，7z格式的无密码压缩包）","C:\"" ,fliter_list, None)#第一个参数是窗口标题，第二个参数是窗口起始路径，第三个参数是过滤器变量（好像不能直接写个列表在这里面）第四个咱也不知道干什么用的直接空着没写
        #切记，四个变量哪怕有空也不能少任何一个，不然直接给你爆！！！掉
        if fileName_choose == None:#如果这个傻逼一个文件没选就右上角报错，报错内容详见script.rpy，写这里renpy会炸掉
            persistent.notify_sub_choice = 1
        else:
            if fileName_choose.find(".rar") != -1 or fileName_choose.find(".zip") != -1 or fileName_choose.find(".7z") != -1:
                persistent.submod_file_dir = fileName_choose[:-8].replace('\\', '/')
                Submod_Install(persistent.submod_file_dir,None)
            else:
                persistent.notify_choice = 3#如果这个傻逼选了一个非DDLC.exe的文件那就报错说他选的不是DDLC.exe
    def Submod_Choose_2():#通过文件夹安装
        fliter_list = None#过滤器得是列表形式的，第一个是描述，第二个是具体条件
        filedir_choose = _renpytfd.selectFolderDialog("请在本窗口选择您要安装的Submod文件夹","C:\"" )#第一个参数是窗口标题，第二个参数是窗口起始路径
        #切记，两个变量哪怕有空的也不能少任何一个，不然直接给你爆！！！掉
        if filedir_choose == None:#如果这个傻逼一个文件夹没选就右上角报错，报错内容详见script.rpy，写这里renpy会炸掉
            persistent.notify_sub_choice = 2
        else:
            Submod_Folder_Test(filedir_choose)
            if persistent.it_works:
                persistent.submod_folder_dir = filedir_choose[:-8].replace('\\', '/')
                Submod_Install(None,persistent.submod_folder_dir)
            else:
                persistent.notify_choice = 4#如果这个傻逼选了一个文件过多的文件夹那就报错，报错内容详见script.rpy，写这里renpy会炸掉
    def Submod_Install(file_dir,dir):#识别Submod，后端干的活，我就不参与了（第一个入参是通过文件形式安装的submod的压缩包文件绝对路径，第二个入参是通过文件夹形式安装的Submod文件夹绝对路径，这两者不可能同时有赋值）
        __init__(self, persistent.mas_basedir)
        
        pass
    def Delete_Submod(location):#删除一个submod的函数，思路是传个包含了所有文件相对路径的list然后走os模块删除
        return
    def Jump_start():
        renpy.jump_out_of_context("start")



init python:#这里写Submod这个类
    class SubMod:
        def __init__(self, name, version, author, coauthors=None, description=None,location=None):
            self.name = name  # 子模块名称
            self.version = version  # 子模块版本号
            self.author = author  # 作者名称
            self.coauthors = coauthors if coauthors else []  # 共同作者列表（默认为空列表）
            self.description = description  # 描述文本（可选）
            self.location = location  #应当为一个list，是该submod涉及到的所有文件的相对路径
init python:#关于拖拽文件到windows窗口上的可行性

    import pygame


    class FileGetter(renpy.Displayable):
        def __init__(self, pos, size, *args, **properties):
            self.pos = pos
            self.size = size
            super().__init__(*args, **properties)

        def render(self, width, height, st, at):
            render = renpy.Render(width, height)
            canvas = render.canvas()
            canvas.rect((255, 255, 255), (*self.pos, *self.size), width=1)
            return render
    
        def event(self, ev, x, y, st):
            if (
                (not self.pos[0] <= x <= self.pos[0] + self.size[0]) or 
                (not self.pos[1] <= y <= self.pos[1] + self.size[1])
            ):
                return
            if ev.type == pygame.MOUSEBUTTONDOWN:
                renpy.notify("mouse button down")
            if ev.type == pygame.DROPBEGIN:
                renpy.notify("something is being dropped")
            if ev.type == pygame.DROPCOMPLETE:
                renpy.notify("something was dropped")
            if ev.type == pygame.DROPFILE:
                renpy.notify("file dropped: " + ev.file)


        



