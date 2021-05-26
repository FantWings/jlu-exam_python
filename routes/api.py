from flask import Blueprint, request, make_response, session, current_app
import os
import base64

from lib.response import json_res
import lib.db as Oprater

api = Blueprint('api', __name__)


@api.before_request
def before_request():
    """
    设置用户Session有效期
    """
    session.permanent = True


@api.route('/ping')
def ping_check():
    return make_response('Pong')


@api.route('/getState', methods=["GET"])
def get_state():
    """
    状态接口，承接前端第一次请求
    返回程序被使用次数，用户登录态
    """
    isAuthed = session.get('authed')
    state = {'count': Oprater.getPaperCount(), 'authed': isAuthed}
    return make_response(json_res(data=state))


@api.route('/paper/<paper_id>', methods=['GET', 'POST'])
def paper(paper_id):
    """
    试卷处理接口
    """
    if request.method == "GET":
        # 获取试卷数据
        answers = Oprater.getPapers(paper_id, session.get('token'))
        # 处理完成，返回答案数据给前端
        return make_response(answers)

    if request.method == "POST":
        # 获取前端传来的JSON数据
        submit_info = request.get_json()

        # 将问卷数据交给答案处理函数，并保存返回值
        answers = Oprater.addPapers(submit_info['question_data'])

        # 判断用户是否带了Token，没有则随机生成一个给他
        token = session.get('token')
        if token is None:
            token = base64.b64encode(os.urandom(16)).decode('ascii')
            session['token'] = token
        # 更新这张试卷的所有者
        Oprater.updatePaperOwner(paper_id, token)

        # 为这个用户设置已登录标识，后续无需再让其输入执行token
        session['authed'] = True

        # 处理完成，返回试卷号给前端
        return make_response(answers)


@api.route('/paper/setPaperName', methods=['POST'])
def remane():
    """
    试卷名称修改接口，处理用户的试卷名称更新请求
    """
    submit = request.get_json()
    result = Oprater.setPaperName(submit['paper_id'], submit['new_name'],
                                  session.get('token'))
    return make_response(result, result['code'])


@api.route('/paper/lists', methods=['GET'])
def get_paper_list():
    """
    获取工具存储的试卷列表
    """
    limit = int(request.args.get('limit', default=10))
    index = int(request.args.get('index', default=1))
    return make_response(Oprater.getPaperList(limit, index))
