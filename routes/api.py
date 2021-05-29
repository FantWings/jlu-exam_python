from flask import Blueprint, request, make_response

from lib.response import json_res
import lib.db as Oprater

api = Blueprint('api', __name__)


@api.route('/ping')
def ping_check():
    return make_response('Pong')


@api.route('/getState', methods=["GET"])
def get_state():
    """
    状态接口，承接前端第一次请求
    返回程序被使用次数
    """
    state = {'count': Oprater.getPaperCount()}
    return make_response(json_res(data=state))


@api.route('/paper/<paper_id>', methods=['GET', 'POST'])
def paper(paper_id):
    """
    试卷处理接口
    """
    userIdent = request.headers.get('userIdent', None)
    if request.method == "GET":
        # 获取试卷数据
        answers = Oprater.getPapers(paper_id, userIdent)
        # 处理完成，返回答案数据给前端
        return make_response(answers)

    if request.method == "POST":
        if userIdent is None:
            return make_response(json_res(msg='无效的识别码Header，禁止提交', code=1))
        # 获取前端传来的JSON数据
        submit_info = request.get_json()
        # 将问卷数据交给答案处理函数，并保存返回值
        answers = Oprater.addPapers(submit_info['question_data'], userIdent)
        # 更新这张试卷的所有者
        Oprater.updatePaperOwner(paper_id, userIdent)
        # 处理完成，返回试卷号给前端
        print(answers)
        return make_response(answers)


@api.route('/paper/setPaperName', methods=['POST'])
def remane():
    """
    试卷名称修改接口，处理用户的试卷名称更新请求
    """
    submit = request.get_json()
    result = Oprater.setPaperName(submit['paper_id'], submit['new_name'],
                                  request.headers.get('userIdent'))
    return make_response(result, 200)


@api.route('/paper/lists', methods=['GET'])
def get_paper_list():
    """
    获取工具存储的试卷列表
    """
    limit = int(request.args.get('limit', default=10))
    index = int(request.args.get('index', default=1))
    return make_response(Oprater.getPaperList(limit, index))
