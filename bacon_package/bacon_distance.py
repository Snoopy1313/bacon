from typing import Union

from bacon_package.db_generate import initialize_connection, get_colleagues_of_actor, actor_exists, get_actor_id

conn = initialize_connection()


def bacon_distance(source_id: int, target_id: int) -> Union[int, float]:
    """
    Calculate bacon distance between actors using BFS

    :source_id: ID of the source actor
    :target_id: ID of the target actor
    """
    if not (actor_exists(source_id, conn) and actor_exists(target_id, conn)):
        raise LookupError("No such source or target")

    if source_id == target_id:
        return 0

    visited = [source_id]
    queue = [(source_id, 0)]

    while queue:
        source_node = queue.pop(0)
        source_id = source_node[0]
        source_depth = source_node[1]

        for colleague_id in get_colleagues_of_actor(source_id, conn):

            if colleague_id == target_id:
                return source_depth + 1

            if colleague_id not in visited:
                queue.append((colleague_id, source_depth + 1))
                visited.append(colleague_id)

    return float("inf")


def choose_actor(massage: str) -> int:
    """
    Choose actor base on name

    :massage: The massage to print before asking actor name
    """
    name = input(massage)
    name_ids = get_actor_id(name, conn)

    if name_ids:

        if len(name_ids) == 1:
            return name_ids[0]

        print("Choose:")
        for name_id in name_ids:
            print(f"ID: {name_id}, Name: {name}")
        return int(input())

    else:
        raise Exception("No such actor name")


if __name__ == "__main__":
    source_id = choose_actor("Enter source name:\n")
    target_id = choose_actor("Enter target name:\n")
    print(f"Bacon distance is: {bacon_distance(source_id, target_id)}")
