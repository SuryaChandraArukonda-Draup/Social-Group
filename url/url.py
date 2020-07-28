from view.view import Role1, Group1, User1, Post1, Comment1, AddToGroup1, RemoveGroup1


def initialize_routes(api):
    api.add_resource(Role1, '/api/role/<id>')
    api.add_resource(Group1, '/api/<id>/group')
    api.add_resource(User1, '/api/user')
    api.add_resource(Post1, '/api/Group/<id>/post')
    api.add_resource(Comment1, '/api/<gid>/<pid>/comment')
    api.add_resource(AddToGroup1, '/api/atg/<id>')  # atg = AddToGroup
    api.add_resource(RemoveGroup1, '/api/rfg/<id>')  # rfg = RemoveFromGroup
