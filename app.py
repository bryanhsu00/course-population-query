from NcnuCourse import Course
from tkinter import * 
from tkinter.ttk import Treeview
from tkinter import ttk

def cb():
    l = []
    for cate, chk in zip(category, chkBtn):
        if chk.get() == 1:
            l.append(cate)
    updateTree(obj.filterCourse(l))

def updateTree(course):
    tree.delete(*tree.get_children())

    for c in course:
        result = []
        for e in enlab[1:]:
            try:
                result.append(c[e])
            except:
                pass
        if int(c['limit']) > int(c['seleced_no']):
            tree.insert("",index=END, text=c[enlab[0]], values=result, tags = ('available',))
        else:
            tree.insert("",index=END, text=c[enlab[0]], values=result)

obj = Course()

enlab = ('year', 'courseid', 'class', 'cname', 'deptid',
         'division', 'grade', 'teachers', 'place', 'not_accessible',
         'time', 'limit', 'seleced_no', 'classify')

chlab = ("學期", "課號", "班別", "中文課名", "開課系所代碼", 
         "部別", "年級", "開課教師", "地點", "非無障礙教室", 
         "時間", "人數上限", "選修人數", "類別")

category = ( '人文-文學與藝術', '人文-歷史哲學與文化',
             '社會-法政與教育', '社會-社經與管理', 
             '自然-工程與科技', '自然-生命與科學',
             '特色通識-東南亞', '特色通識-綠概念', 
             '特色通識-在地實踐', '只顯示人數未滿')

chkBtn = []

root = Tk()

f = Frame(root)

for index, content in enumerate(category):
    var = IntVar()
    var.set(1)
    chkBtn.append(var)
    c = Checkbutton(f, text=content, variable=var, command=cb, font=(None, 10))
    c.grid(row = 0, column = index)

chkBtn[-1].set(0)

f.pack()

scrollbar = Scrollbar(root)
scrollbar.pack(side=RIGHT, fill=Y)

tree = Treeview(root, columns=enlab, yscrollcommand=scrollbar.set, height=20)

style = ttk.Style()
style.configure("Treeview.Heading",rowheight=40, font=(None, 10))
style.configure("Treeview", rowheight=40, font=(None, 10))

for i, l in enumerate(chlab):
    tree.heading("#"+str(i), text=chlab[i])
    tree.column("#"+str(i), minwidth=0, width=120, stretch=NO, anchor=CENTER)

cb()
tree.tag_configure('available', background='#E8E8E8')
tree.pack(fill='x')
scrollbar.config(command=tree.yview)

root.mainloop()

