from json import loads, dumps
from time import mktime
from sqlalchemy import func

from sql.model import db
from sql.tables.t_paper import Paper
from lib.response import json_res
from lib.artifact import getAnswers


def addPapers(paper_data, userIdent):
    """
    添加一张试卷数据

    * paper_data（试卷数据）
    * userIdent（用户身份识别码）

    """

    # 将试卷号存储到变量
    paper_id = paper_data['data']['answerPaperRecordId']
    paper = Paper.query.get(paper_id)

    # 判断数据库内是否已经有这份试卷了
    if paper is None:
        try:
            # 调用答案解析函数，解析答案，存储到变量
            try:
                getAnswers(paper_data['data']['questions'])
            except Exception:
                return json_res(msg='你输入的试卷数据不正确或试卷数据不完整，解析失败！', code=1)

            # 将试卷号、提交者IP地址、原试卷数据、答案数据写入数据库
            new_paper = Paper(id=paper_id,
                              submit_ip=paper_data['data']['sourceIp'],
                              original=dumps(paper_data['data']['questions']),
                              owner=userIdent)
            db.session.add(new_paper)
            db.session.commit()

            # 返回处理结果以及试卷号
            return json_res(msg='答案处理成功', code=0)
        # 异常处理
        except Exception as e:
            return json_res(msg=str('后端错误：{}'.format(e)), code=1)

    paper.used_count = Paper.used_count + 1
    db.session.commit()
    return json_res(msg="答案已在数据库中，直接从数据库中返回答案数据")


def getPapers(paper_id, userIdent):
    """
    从数据库获取试卷（含答案）

    * paper_id（试卷号）
    * userIdent（用户识别码，用于判断这个用户是否是这个试卷的所有者）
    """

    paper = Paper.query.get(paper_id)

    # 判断数据库内是否已经有这份试卷了
    if paper is None:
        return json_res(msg='试卷不存在，请检查试卷号是否正确。', code=1)
    else:
        response = {
            'paper_id': paper.id,
            'paper_name': paper.paper_name,
            'submit_time': int(mktime(paper.submit_time.timetuple())) * 1000,
            'isOwner': userIdent == paper.owner,
            'answers': getAnswers(loads(paper.original))
        }
        return json_res(data=response)


def setPaperName(paper_id, new_name, userIdent):
    """
    命名试卷名称

    * paper_id： 试卷UUID
    * new_name： 试卷名称
    * token：所有者密钥
    """
    paper = Paper.query.get(paper_id)
    if userIdent == paper.owner:
        try:
            paper.paper_name = new_name
            db.session.commit()
            return json_res(msg="试卷数据更新成功！")
        except Exception as e:
            return json_res(msg=e, code=1)
    else:
        return json_res(msg='你不是该试卷的所有者，无法改动试卷数据！', code=1)


def updatePaperOwner(paper_id, userIdent):
    """
    为试卷设定/更新所有者，为其后续提供修改权限

    * paper_id（试卷号）
    * userIdent（用户识别码）
    """
    try:
        paper = Paper.query.get(paper_id)
        paper.owner = userIdent
        db.session.commit()
    except Exception as e:
        print(e)
        pass


def getPaperCount():
    """
    统计数据库内的试卷被使用次数之和

    """
    result = db.session.query(func.sum(Paper.used_count)).scalar() or 0
    return int(result)


def getPaperList(limit, index):
    """
    从数据库获取试卷列表
    """
    results = Paper.query.order_by(
        Paper.submit_time.desc()).limit(limit).offset(
            (index - 1) * limit).with_entities(
                Paper.id, Paper.paper_name,
                func.date_format(Paper.submit_time, "%Y年%m月%d日 %H时%i分")).all()
    total = Paper.query.count()
    data = []
    for result in results:
        data.append(list(result))
    return json_res(data={"results": data, "total": total})
