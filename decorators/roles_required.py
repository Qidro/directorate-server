from exceptions import ApiError


def roles_required(roles: list, have_all: bool = False):
    def _roles_required(fn):
        def wrapper(user, *args, **kwargs):
            user_roles = [user_right.right.slug for user_right in user.rights]

            role_count = 0
            for role in roles:
                if role in user_roles:
                    role_count += 1

            if have_all:
                if len(roles) != role_count:
                    raise ApiError.Forbidden()
            else:
                if role_count < 1:
                    raise ApiError.Forbidden()

            return fn(user, *args, **kwargs)

        wrapper.__name__ = fn.__name__
        return wrapper

    return _roles_required
