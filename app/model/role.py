class Role():
    def __init__(self, name, permissions):
        self.name = name
        self.permissions = permissions

    def get_permissions(self):
        return self.permissions
    
admin_role = Role("Admin", ["create_user", "delete_user", "suspend_user"])
guest_role = Role("Guest", ["get"])

