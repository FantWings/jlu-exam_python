from re import compile


def getAnswers(originalData):
    """
    答案解析函数第二版，用于解析作业试题答案，比第一版代码量更少，更高效，拥有更强自的适应性，可应对学校未来可能出现的新题型。

    * original_data：考试系统的试卷数据
    """

    # 创建空字典
    answers = {}

    # 预定义正则表达式，用于清理题目上乱七八糟的杂项数据
    pattern = compile(r'<[^>]+>', re.S)

    # 处理答案
    for question in originalData:
        # 检测字典内有没有这个题型，没有就创建一个并赋予一个空数组
        if not answers.get(question['questiontypename']):
            answers[question['questiontypename']] = []

        options = []
        for option in question.get('answerArea').get('optionList'):
            options.append(pattern.sub('', option.get('content')))

        # 定义答案常量，将答案从原始数据中取出，进行完形填空
        const = dict(
            id=question.get('questionId', None),
            type=question.get('questiontypename', None),
            answer=question.get('answer', None),
            options=options,
            question=pattern.sub('', question.get('stem')),
        )

        # 将常量追加到字典对应题型的数组内
        answers[question['questiontypename']].append(const)

    # 返回处理结果
    return answers
