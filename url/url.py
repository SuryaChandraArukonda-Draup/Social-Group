from view.view import Group1, User1, Post1, Comment1, AddToGroup1, RemoveUserGroup1, DeletePost1, DeleteComment1, ReadGroup1


def initialize_routes(api):
    api.add_resource(User1, '/api/add-user')
    api.add_resource(Group1, '/api/group')
    api.add_resource(AddToGroup1, '/api/group/<group_id>/add')
    api.add_resource(RemoveUserGroup1, '/api/group/<group_id>/remove')
    api.add_resource(ReadGroup1, '/api/group/<group_id>/read')
    api.add_resource(Post1, '/api/group/<group_id>/post/add')
    api.add_resource(DeletePost1, '/api/group/<group_id>/post/<post_id>/delete')
    api.add_resource(Comment1, '/api/group/<group_id>/post/<post_id>/comment/add')
    api.add_resource(DeleteComment1, '/api/group/<group_id>/comment/<comment_id>/delete')
