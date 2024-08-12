from exceptions import ApiError


def rights_required(rights: list, have_all: bool = False):
    def _rights_required(fn):
        def wrapper(user, *args, **kwargs):
            user_rights = [user_right.right.slug for user_right in user.rights]

            right_count = 0
            for right in rights:
                if right in user_rights:
                    right_count += 1

            if have_all:
                if len(rights) != right_count:
                    raise ApiError.Forbidden()
            else:
                if right_count < 1:
                    raise ApiError.Forbidden()

            return fn(user, *args, **kwargs)

        wrapper.__name__ = fn.__name__
        return wrapper

    return _rights_required
