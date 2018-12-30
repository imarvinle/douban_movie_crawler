# -*-coding: utf-8 -*-

import threading
import time

isend = False

class MyThread(threading.Thread):

    # 创建并启动线程
    def __init__(self, workqueue, taskname=""):
        threading.Thread.__init__(self)
        self.taskname = taskname
        self.workqueue = workqueue
        self.start()



    def run(self):
        no_task = 0
        while True:  # 除非确认队列中已经无任务，否则时刻保持线程在运行
            try:
                func, args, kwargs = self.workqueue.get(block=isend)  # 如果队列空了，直接结束线程。根据是否还有任务
                if self.taskname == "[数据库插入]":
                    print("---------当前还有 %d 条电影数据待插入-------" % self.workqueue.qsize())
                elif self.taskname == "[电影详细信息]":
                    print("---------当前还有 %d 部电影待爬取-------" % self.workqueue.qsize())
                elif self.taskname == "[电影ID获取]":
                    print("---------当前还有 %d 种类型电影分类待爬取-------" % self.workqueue.qsize())
                try:
                    func(*args, **kwargs)
                except Exception as e:
                    print('bad execution: %s' % (str(e)))
                no_task = 0
                self.workqueue.task_done()
                #print("%s 线程-%s完成一个任务，马上领取下一个任务\n" % (self.taskname, self.getName()))
            except Exception as e:
                no_task = no_task + 1
                if no_task <= 60:
                    print("%s 线程-%s目前无任务可做, 正在第 %d 次等待\n" % (self.taskname, self.getName(), no_task))
                    time.sleep(5)
                    continue
                else:
                    print("%s 线程-%s等待了120次还是无任务...立即退出\n" % (self.taskname, self.getName()))
                    break


class MyThreadPool():

    def __init__(self, movie_tag_queque, movie_queue, shortqueue, commentqueue, db_queue, movie_tag_size, movie_size, short_size, comment_size, db_size=5):
        self.movie_queue = movie_queue
        self.shortqueue = shortqueue
        self.commentqueue = commentqueue
        self.movielistqueque = movie_tag_queque
        self.db_size = db_size
        self.pool = []
        print("-----------创建线程池 包含 %d 个工作线程-----------\n" % (movie_tag_size + movie_size + short_size + comment_size))
        for i in range(movie_tag_size):
            self.pool.append(MyThread(movie_tag_queque, taskname="[电影ID获取]"))
        print("-----------抓取电影id列表共 %d 个线程创建完毕-----------\n" % (movie_tag_size))

        for i in range(movie_size):
            self.pool.append(MyThread(movie_queue, taskname="[电影详细信息]"))
        print("-----------*抓取电影详细信息共 %d 个线程创建完毕-----------\n" % (movie_size))

        for i in range(short_size):
            self.pool.append(MyThread(shortqueue, taskname="[短评获取]"))
        print("-----------抓取电影短评信息共 %d 个线程创建完毕-----------\n" % (short_size))

        for i in range(comment_size):
            self.pool.append(MyThread(commentqueue, taskname="[影评获取]"))
        print("-----------抓取电影评论信息共 %d 个线程创建完毕-----------\n" % (comment_size))

        for i in range(self.db_size):
            self.pool.append(MyThread(db_queue, taskname="[数据库插入]"))
        print("-----------数据库插入共 %d 个线程创建完毕-----------\n" % (self.db_size))

    def joinAll(self):
        for thread in self.pool:
            if thread.isAlive():
                thread.join()



if __name__ == '__main__':
   pass