from unittest import result


def merge_dicts(dict1, operator, dict2, offset):
    new_dict = {}

    # add doc_id's to new dictionary
    unique_docs = set(list(dict1.keys()) + list(dict2.keys()))
    for doc_id in unique_docs:

        # making sure the doc_id exists in the both dictionaries
        if doc_id not in dict1:
            dict1[doc_id] = []
        if doc_id not in dict2:
            dict2[doc_id] = []

        if operator == "AND" or operator[0] == "\\":
            new_dict[doc_id] = and_lists(dict1[doc_id], offset, dict2[doc_id])
        elif operator == "NOT":
            new_dict[doc_id] = not_lists(dict1[doc_id], offset, dict2[doc_id])
        elif operator == "OR":
            new_dict[doc_id] = or_lists(dict1[doc_id], dict2[doc_id])
        else:
            print(f"Wrong operator: {operator}")

    # remove empty pairs
    return {key: value for key, value in new_dict.items() if value != []}


def not_lists(list1, offset, list2):
    result = list1.copy()

    for i in list1:
        for j in list2:
            if i + offset == j:
                result.remove(i)

    return result


def and_lists(list1, offset, list2):
    result = []

    for i in list1:
        for j in list2:
            if i + offset == j:
                result.append(i)
            elif i + offset < j:
                break

    return result


def or_lists(list1, list2):
    result = list(set(list1) | set(list2))
    result.sort()
    return result
