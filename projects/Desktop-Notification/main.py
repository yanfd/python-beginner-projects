# import win10toast

# from win10toast import ToastNotifier

# # create an object to ToastNotifier class

# n = ToastNotifier()

# n.show_toast(
#     "Python project",
#     "Here is your notification body",
#     duration=20,
#     icon_path="logo.ico",
# )


#using Mac, so i switch it to a different version

from pync import Notifier

# 显示通知
Notifier.notify(
    "Here is your notification body",  # 通知内容
    title="Python Project",  # 通知标题
    app_name="Settings",  # 应用程序名称（可选）
)