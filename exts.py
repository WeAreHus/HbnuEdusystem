# coding:utf8
from models import Student, Subject, Score


# 计算平均学分
def exts(cla):
    # 所有课程的学分
    allcredit = 0
    # 未获得的学分
    gotcredit = 0
    # 平均绩点
    GPA = 0
    for c in cla:
        if cmp(c.test_category.encode('utf-8'), '正常考试'):
            if c.score < 60:
                gotcredit = gotcredit + c.credit
        else:
            GPA = GPA + c.GPA * c.credit
            allcredit = allcredit + c.credit
    GPA = GPA/allcredit
    GPA = round(GPA, 2)
    credit = [allcredit, gotcredit, GPA]
    return credit


def sub_query(id, year, term):
    lists = []
    stu = Score.query.filter(Score.stu_id == id).all()
    if year == 'all':
        for cla in stu:
            if cla.school_term == int(term):
                lists.append(cla)
    elif term == 'all':
        for cla in stu:
            if cla.school_year == year:
                lists.append(cla)
    else:
        for cla in stu:
            if cla.school_term == int(term) and cla.school_year == year:
                lists.append(cla)
    if lists:
        credit = exts(lists)
    else:
        credit = [0,0,0]

    return credit, lists



def drow(id):
    year_list = []
    term_list = []
    score_list = []
    credit_list = []
    time_list = []
    sco = Score.query.filter(Score.stu_id == id).all()
    for s in sco:
        if s.school_year in year_list:
            pass
        else:
            year_list.append(s.school_year)
        if s.school_term in term_list:
            pass
        else:
            term_list.append(s.school_term)
    for year in year_list:
        for term in term_list:
            for s in sco:
                if s.school_year == year and s.school_term == term:
                    score_list.append(s)
            time = str(year) + '(' + str(term) + ')'
            print time
            time_list.append(time)
            credit = exts(score_list)
            credit_list.append(credit)
            score_list = []
            print credit
    return credit_list, time_list


