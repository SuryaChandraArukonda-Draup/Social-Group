from view.user import SignUpAPI, GetUserAPI, DeleteUserAPI, EditUserAPI
from view.group import GroupAPI, AddToGroupAPI, RemoveUserGroupAPI, ReadGroupAPI, GetGroupAPI, DeleteGroupAPI, EditGroupAPI, ChangeRoleAPI
from view.post import PostAPI, DeletePostAPI, GetPostAPI, EditPostAPI
from view.comment import CommentAPI, DeleteCommentAPI, GetCommentAPI, EditCommentAPI


def initialize_routes(api):
    api.add_resource(SignUpAPI, '/api/user/create')
    api.add_resource(GroupAPI, '/api/group/create')

    api.add_resource(AddToGroupAPI, '/api/group/<gid>/add')

    api.add_resource(ChangeRoleAPI, '/api/group/<gid>/changerole')

    api.add_resource(EditGroupAPI, '/api/group/<gid>/edit')
    api.add_resource(EditUserAPI, '/api/user/edit')
    api.add_resource(EditPostAPI, '/api/group/<gid>/post/<pid>/edit')
    api.add_resource(EditCommentAPI, '/api/group/<gid>/comment/<cid>/edit')

    api.add_resource(PostAPI, '/api/group/<gid>/post/add')
    api.add_resource(CommentAPI, '/api/group/<gid>/post/<pid>/comment/add')

    api.add_resource(DeleteUserAPI, '/api/user/delete')
    api.add_resource(DeleteGroupAPI, '/api/group/<gid>/delete')
    api.add_resource(DeletePostAPI, '/api/group/<gid>/post/<pid>/delete')
    api.add_resource(DeleteCommentAPI, '/api/group/<gid>/comment/<cid>/delete')

    api.add_resource(GetGroupAPI, '/api/group/<gid>')  # get the group by id
    api.add_resource(GetPostAPI, '/api/group/<gid>/post/<pid>')  # get the post by id
    api.add_resource(GetCommentAPI, '/api/group/<gid>/comment/<cid>')  # get the comment by id
    api.add_resource(GetUserAPI, '/api/user')  # get the group by id

    api.add_resource(RemoveUserGroupAPI, '/api/group/<gid>/remove')

    api.add_resource(ReadGroupAPI, '/api/group/<gid>/read')
