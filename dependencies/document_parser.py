from dependencies.common_funcs import pre_process
import nltk

nltk.download("punkt")


def doc_parser(path, log=False):
    if log:
        log("Started to execute doc_parser")

    total_entity_list = []

    for doc_id in range(5):
        with open(f"{path}/{doc_id}.text", "r") as file:
            # read file and pass it to the pre_proessor
            entity_list = pre_process(file.read(), return_base=True)

            # adding document id and token position to token entities
            for i in range(len(entity_list)):
                entity_list[i]["doc_id"] = doc_id
                entity_list[i]["tkn_pos"] = i + 1
            total_entity_list += entity_list
    return total_entity_list
