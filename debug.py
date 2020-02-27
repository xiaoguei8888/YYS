import cv2,numpy,time,random
import os,sys,traceback
from PIL import ImageGrab
import action_adb as action

# 读取文件 精度控制   显示名字
imgs = action.load_imgs()

#debug 1 表示调试模式
debug = 0

start_time = time.time()
print('程序启动，现在时间', time.ctime())
def log(f):
    def wrap(*agrs, **kwagrs):
        try:
            ans = f(*agrs, **kwagrs)
            return ans
        except:
            traceback.print_exc()
            time.sleep(60)

    return wrap

@log
def select_mode():
    print('''\n菜单：
        1 剧情任务（在庭院中，或者在剧情中）
        2 探索 - 个人（打开对应探索章节）
        3 御魂/觉醒 - 个人（打开对应层数）
        ''')
    action.alarm(1)
    raw = input("选择功能模式：")
    index = int(raw)

    mode = [0, juqing, tansuo_solo, yuhun_juexing_solo]
    mode[index]()

def fanhuitingyuan():
    screen = action.screen_shot_and_load()
    guanbi(screen)
    while not is_tingyuan(screen):
        if fanhui(screen):
            screen = action.screen_shot_and_load()
            continue
        if jixu(screen):
            screen = action.screen_shot_and_load()
            continue
        if guanbi(screen):
            screen = action.screen_shot_and_load()
            continue

        screen = action.screen_shot_and_load()

def tansuo_solo():
    count = 0;
    while True:
        start = time.time()
        screen = action.screen_shot_and_load()
        print("截屏用时", str(time.time() - start))
        if screen is None:
            continue
        if touch_img(["queren"]) is not None:
            print("用时", str(time.time() - start))
            continue
        # 960, 600 - 1260. 690
        want = imgs["gudingzhenrong"]
        # 剪切图片优化
        target = action.cut(screen, (800, 600), (1260, 690))
        pts = action.locate(target, want, debug)
        if not len(pts) == 0:
            # 探索场景中

            # 战斗结束小纸人, 小纸人一般位于中间
            want = imgs["tansuo_faxian"]
            # 剪切图片优化
            target = action.cut(screen, (200, 250), (900, 560))
            pts = action.locate(target, want, debug)
            if not len(pts) == 0:
                # 退出
                print("探索完毕...退出")
                fanhui(screen)
                continue
            # 查找
            touch = touch_img(["zhandou", "shouling"], screen)
            if touch is None:
                if count < 5:
                    count += 1
                    # 没找到 移动
                    action.move_radom()
                else:
                    print("连续%s次没有找到...退出" % count)
                    count = 0
                    fanhui(screen)
                    continue
        else:
            count = 0
            for i in ["zhunbei", "jiangli", "jixu", "tansuo_anniu"]:
                want = imgs[i]
                target = screen
                pos_left_up = (0, 0)
                pos_right_bottom = get_size(screen)
                # 探索按钮位置(860, 480)(1050, 580)
                if want[2] == "tansuo_anniu":
                    pos_left_up = (860, 480)
                    pos_right_bottom = (1050, 580)
                    target = action.cut(screen, pos_left_up, pos_right_bottom)
                pts = action.locate(target, want, debug)
                if not len(pts) == 0:
                    action.touch_want(want, pts, pos_left_up)
                    action.wait()
                    break
            action.move_radom()
        print("用时", str(time.time() - start))

def touch_img(name, target = None):
    if target is None:
        target = action.screen_shot_and_load()
    for i in name:
        want = imgs[i]
        pts = action.locate(target, want, debug)
        if not len(pts) == 0:
            action.touch_want(want, pts)
            action.wait()
            return want

def get_size(target):
    size = target.shape
    h, w, ___ = size
    result = (w, h)
    return result

# 剧情
def juqing():
    while True:
        screen = action.screen_shot_and_load()
        for i in ["renwu_duihua", "renwu_tiaoguo", "renwu_wenhao", "renwu_chakan", "renwu_dianji", "renwu_kuaijin", "zhandou", "zhunbei"]:
            want = imgs[i]
            target = screen
            pts = action.locate(target, want, debug)
            if not len(pts) == 0:
                action.touch_want(want, pts)
                action.wait()
                break
        if guanbi(target):
            continue
        action.move_radom()

def yuhun_juexing_solo():
    while True:
        screen = action.screen_shot_and_load()
        for i in ["yuhun_tiaozhan", "zhunbei", "jiangli", "jixu", "xueliang"]:
            want = imgs[i]
            target = screen
            pts = action.locate(target, want, debug)
            if not len(pts) == 0:
                action.touch_want(want, pts)
                action.wait()
                break

# 是否在庭院中
def is_tingyuan(target):
    for i in ["tingyuan", "tingyuan1"]:
        want = imgs[i]
        pts = action.locate(target, want, debug)
        if not len(pts) == 0:
            print("在庭院中", want[2], pts)
            return True
    return False

# 关闭页面
def guanbi(target):
    for i in ["guanbi", "guanbi1", "guanbi2"]:
        want = imgs[i]
        pts = action.locate(target, want, debug)
        if not len(pts) == 0:
            print("关闭页面中", want[2], pts)
            size = want[0].shape
            h, w , ___ = size
            xx = action.cheat(pts[0], w, h)
            action.touch(xx)
            action.wait()
            return True
    return False

# 关闭页面
def fanhui(target):
    for i in ["fanhui", "fanhui1"]:
        want = imgs[i]
        pts = action.locate(target, want, debug)
        if not len(pts) == 0:
            print("返回中", want[2], pts)
            size = want[0].shape
            h, w , ___ = size
            xx = action.cheat(pts[0], w, h)
            action.touch(xx)
            action.wait()
            return True
    return False

def jixu(target):
    for i in ["jixu", "jixu1", "wenhao1"]:
        want = imgs[i]
        pts = action.locate(target, want, debug)
        if not len(pts) == 0:
            print("继续", want[2], pts)
            size = want[0].shape
            h, w , ___ = size
            xx = action.cheat(pts[0], w, h)
            action.touch(xx)
            action.wait()
            return True
    return False

if __name__ == '__main__':
    select_mode()
