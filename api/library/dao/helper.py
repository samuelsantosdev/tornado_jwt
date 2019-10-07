def make_where(key, value):
    if key.find('__contains') != -1 : 

        key = key.replace('__contains', '')
        return '''{} CONTAINS '{}' '''.format(key, value)

    elif key.find('__isnull') != -1:

        key = key.replace('__isnull', '')
        if value:
            return '''{} IS NULL '''.format(key, value)
        else:
            return '''{} IS NOT  NULL '''.format(key, value)
        
    if key.find('__in') != -1 : 

        key = key.replace('__in', '')
        return '''{} IN ({}) '''.format(key, ",".join(value))

    else:
        
        return '''{}='{}' '''.format(key, value)