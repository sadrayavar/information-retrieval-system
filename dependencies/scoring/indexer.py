import json
from dependencies.common_funcs import extract_posting, tf_idf


def get_vectors(positional_dict, dict_path):
    vectors = {}
    for doc_id in range(5):
        doc_id = str(doc_id)

        vector = {}

        for tkn, value in positional_dict.items():
            posting = extract_posting(value["path"])

            df = len(posting)
            tf = len(posting[doc_id]) if (doc_id in posting) else 0
            vector[tkn] = tf_idf(tf, df, 5)

        vectors[doc_id] = vector

    # create file
    with open(f"{dict_path}/document_vectors.json", "w") as file:
        json.dump(vectors, file, indent=4)

    return vectors
