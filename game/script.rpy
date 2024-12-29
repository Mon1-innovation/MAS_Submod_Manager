# 游戏的脚本可置于此文件中。

# 声明此游戏使用的角色。颜色参数可使角色姓名着色。

label start:
    python:
        submod_dict = {
        "submod_1": SubMod(
            name="Example SubMod",
            version="1.0",
            author="John Doe",
            coauthors=["Jane Doe", "Alex Smith"],
            description="This is an example submod.",
            location=None
        ),
        "submod_2": SubMod(
            name="Another SubMod",
            version="2.5",
            author="Alice",
            coauthors=[],
            description=None,
            location=None

        )
        }
    if persistent.mas_basedir == "":
        "您没有选择MAS目录，请在设置内选择后再使用本Submod管理器。"
        return
    show screen Submod_Exploer_GUI()
    return


label projects_directory_preference:
    call choose_projects_directory
    jump preferences
label preferences:
    call screen preferences
    jump preferences
label choose_projects_directory:
    python:
        MAS_Basedir_Choose()
    if persistent.notify_choice == 1:
        show screen notify("错误：您并未选择任何一个文件。")
    if persistent.notify_choice == 2:
        show screen notify("已设定新的MAS目录")
    if persistent.notify_choice == 3:
        show screen notify("错误：您选择的文件并非MAS启动程序（DDLC.exe）")
    if persistent.notify_choice == 4:
        show screen notify("错误：您选择的文件所在目录并不包含Submods文件夹，请检查此DDLC.exe是否为MAS的DDLC.exe，以及您是否安装了任何一个Submod")
    return
label choose_submod_directory(test):#这个入参是判断玩家使用的是文件夹安装还是压缩包安装，1是压缩包2是文件夹
    python:
        if test == 1:
            Submod_Choose_1()#压缩包安装
        elif test == 2:
            Submod_Choose_2()#文件夹安装
    if persistent.notify_choice == 1:
        show screen notify("错误：您并未选择任何一个文件。")
    if persistent.notify_choice == 2:
        show screen notify("错误：您并未选择任何一个目录。")
    if persistent.notify_choice == 3:
        show screen notify("错误：您选择的文件并非支持的压缩包格式（.zip .rar .7z）")
    if persistent.notify_choice == 4:
        show screen notify("错误：您选择的目录文件过多，我们无法使用")
    show screen confirm_2("安装完成", Hide("confirm_2"))
    

