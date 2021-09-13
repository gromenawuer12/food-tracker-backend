def delete_attrs(user,lAttr):
    for attr in lAttr:
        delattr(user, attr)
    return user