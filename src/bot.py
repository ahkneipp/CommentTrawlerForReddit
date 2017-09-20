import praw

reddit = praw.Reddit(client_id='NOV_1-m6lREGaA', client_secret="ojPsfAEv2LD6JVOl5sy7XbtH0Kg",
                     password='JQ8qPajXFJDzJK', user_agent='linux:tk.alexk.CommentMapper:v0.0.1 (by /u/canine505)',
                     username='comment-mapper-9000')
print(reddit.read_only)

allusers = []

def get_index_from_username(users, username):
    for i in range(0, len(users), 1):
        if users[i].name == username:
            return i
    return -1

def create_square_adjency_matrix(m):
    return [[0] * m for i in range(m)]

def build_user_list(comment_tree):
    users = []
    all_comments = comment_tree.list()
    for comment in all_comments:
        if not comment.author in users:
            users.append(comment.author)
    while None in users:
        users.remove(None)
    return users

def build_adjency_matrix(mat, comment_tree):
    temp = mat
    for comment in comment_tree:
        comment.refresh()
        if comment.replies.__len__() != 0:
            temp = build_adjency_matrix(mat, comment.replies)
        else:
            temp[get_index_from_username(allusers, comment.author)][
                get_index_from_username(allusers, comment.parent().author)] += 1
            return temp

def expand_all_more_comments(comment_tree):
    for comment in comment_tree:
        comment.refresh()
        if comment.replies.__len__() != 0:
            comment.replies.replace_more(limit=None)
            expand_all_more_comments(comment.replies)

def main():
    submission = (reddit.subreddit('AskReddit').random())
    for comment1 in submission.comments.list():
        comment1.refresh()
        print(comment1.replies)
    print("\n\n")
    submission.comments.replace_more()
    for comment in submission.comments.list():
        comment.refresh()
        print(comment.replies)



if __name__ == '__main__':
    main()

# for comment in top_level_comments:
#     users.append(comment.author.name)
#     print(comment.author.name)
#
# for submission in reddit.subreddit('learnpython').hot(limit=10):
#     print(submission.title)
