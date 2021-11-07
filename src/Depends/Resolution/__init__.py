


def resolve(pkg):
    return resolve_dependencies(pkg, [], [])

def resolve_dependencies(pkg, seen, resolved):

    for dependency in pkg.depends:
        if dependency not in resolved:
            if dependency in seen:
                return None 
            seen.append(dependency)
            rtrnVal = resolve_dependencies(dependency, seen, resolved)
            if rtrnVal == None:
                return None

    resolved.append(pkg)
    return resolved