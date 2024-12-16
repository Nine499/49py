# 导入随机数模块
import random

# 生成一个1到100之间的随机整数
secret_number = random.randint(1, 100)

# 初始化猜测次数
guesses = 0

# 打印游戏开始的欢迎信息
print("欢迎来到猜数字游戏！")
print("我已经想好了一个1到100之间的数字。")

# 使用while循环，直到玩家猜对为止
while True:
    # 提示玩家输入一个猜测的数字
    guess = int(input("请输入你猜测的数字："))

    # 增加猜测次数
    guesses += 1

    # 判断玩家猜测的数字与随机数的大小关系，并给出提示
    if guess < secret_number:
        print("太小了！再试一次。")
    elif guess > secret_number:
        print("太大了！再试一次。")
    else:
        # 如果猜对了，打印恭喜信息并显示猜测次数，然后退出循环
        print(f"恭喜你！你猜对了！这个数字是 {secret_number}。")
        print(f"你总共猜测了 {guesses} 次。")
        break
