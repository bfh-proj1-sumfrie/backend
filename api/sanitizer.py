import re


def remove_comments(sql):
    # comments may be used to hack around our pagination limits
    hashtag_comment_regex = re.compile('#.*')
    dash_comment_regex = re.compile('--.*')
    slash_comment_regex = re.compile(r'\/\*.*\*/')
    slash_comment_regex_half = re.compile(r'\/\*.*')

    sql = re.sub(hashtag_comment_regex, ' ', sql)
    sql = re.sub(dash_comment_regex, ' ', sql)
    sql = re.sub(slash_comment_regex, ' ', sql)
    sql = re.sub(slash_comment_regex_half, ' ', sql)
    return sql
