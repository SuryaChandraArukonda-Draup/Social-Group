from view.user import SignUpAPI
from view.group import GroupAPI, AddToGroupAPI, RemoveUserGroupAPI, ReadGroupAPI
from view.post import PostAPI, DeletePostAPI
from view.comment import CommentAPI, DeleteCommentAPI


def initialize_routes(api):
    api.add_resource(SignUpAPI, '/api/user/create')
    api.add_resource(GroupAPI, '/api/group/create')
    api.add_resource(AddToGroupAPI, '/api/group/<gid>/add')
    api.add_resource(RemoveUserGroupAPI, '/api/group/<gid>/remove')
    api.add_resource(ReadGroupAPI, '/api/group/<gid>/read')
    api.add_resource(PostAPI, '/api/group/<gid>/post/add')
    api.add_resource(DeletePostAPI, '/api/group/<gid>/post/<pid>/delete')
    api.add_resource(CommentAPI, '/api/group/<gid>/post/<pid>/comment/add')
    api.add_resource(DeleteCommentAPI, '/api/group/<gid>/comment/<cid>/delete')
