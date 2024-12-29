screen Submod_Exploer_GUI():
    tag menu
    add "white"
    viewport id "scrollme":
        scrollbars "vertical"
        mousewheel True
        draggable True

        has vbox:
            style_prefix "check"
            xfill True
            xmaximum 1000

        for submod in sorted(submod_dict.values(), key=lambda x: x.name):
            vbox:
                xfill True
                xmaximum 1000

                label submod.name:
                    yanchor 0
                    xalign 0
                    text_text_align 0.0

                if submod.coauthors:
                    $ authors = "v{0}{{space=20}}by {1}, {2}".format(submod.version, submod.author, ", ".join(submod.coauthors))

                else:
                    $ authors = "v{0}{{space=20}}by {1}".format(submod.version, submod.author)

                text "[authors]":
                    yanchor 0
                    xalign 0
                    text_align 0.0
                    layout "greedy"
                    style "main_menu_version"

                if submod.description:
                    text submod.description text_align 0.0
                textbutton "删除":
                    style "SEG_tb"
                    action Show(screen="confirm", message="你确定吗，这个子模组将会被删除且无法从回收站找回。（真的是消失很久很久！）（当然你可以再装回来）", yes_action=Function(Delete_Submod, submod.location), no_action=Hide(screen="confirm"))
    vbox:
        xalign 1.0  # 右对齐
        yanchor 1.0  # 底部对齐

image white = "#ffffff"
image frame_bg = Frame("images/frame_bg.png")
style SEG_tb:
    font "miui.ttf"
    color "#fff"
    background "frame_bg"
    size 85
    hover_outlines [(4, "#6d6d6d", 0, 0), (2, "#dbdbdb", 2, 2)]
    insensitive_outlines [(4, "#fff", 0, 0), (2, "#fff", 2, 2)]