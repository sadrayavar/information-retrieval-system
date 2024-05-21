from dependencies.common_funcs import extract_posting, tf_idf


def get_vectors(positional_dict):
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

    return vectors
