from ids.group import Role1, Permissions1, Group1, User1, Post1, Comment1


def initialize_routes(api):
    api.add_resource(Role1, '/api/groups')
    api.add_resource(Permissions1, '/api/group/permissions')
    api.add_resource(Group1, '/api/group')
    api.add_resource(User1, '/api/user')
    api.add_resource(Post1, '/api/group/<id>/user/<id>/post')
    api.add_resource(Comment1, '/api/group/<id>/user/<id>/post/<id>/comment')
