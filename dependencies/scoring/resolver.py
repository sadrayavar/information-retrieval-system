from dependencies.scoring.scoring import tf_idf, extract_posting
from dependencies.common_funcs import pre_process


class RankedResolver:
    def __init__(self, query, pos_dict, docs_vector, log):
        self.log = log
        self.pos_dict = pos_dict
        tkns = pre_process(query)

        # generate query vector
        TF = self.get_tf(tkns)
        query_vector = self.gen_vector(tkns, TF)

        # calculate simularity
        results = self.rank(query_vector, docs_vector)

        # print the results
        print("Documents sorted by there simularity:")
        for key, value in reversed(results.items()):
            print(f"\t{key} => {value}")

    def rank(self, q_vector, d_vectors):
        sim_dict = {}

        for doc_id in d_vectors:
            sim_dict[doc_id] = self.cos_sim(q_vector, d_vectors[doc_id])

        # sort and return the dictionary
        return dict(sorted(sim_dict.items(), key=lambda item: item[1]))

    def sort_dict(self, dict):
        return

    def cos_sim(self, v1, v2):
        top = self.dot_product(v1, v2)

        if top == 0:
            return 0

        bottom_l = sum([value**2 for _, value in v1.items()])
        bottom_r = sum([value**2 for _, value in v2.items()])

        return top / (bottom_l * bottom_r)

    def dot_product(self, v1, v2):
        sum = 0
        for i in v1:
            for j in v2:
                if i == j:
                    sum += v1[i] * v2[j]
        return sum

    def gen_vector(self, tkns, TF):
        vector = {}

        for tkn in tkns:
            tkn = tkn["stem"]

            if tkn not in vector:
                # extracting posting list
                if tkn in self.pos_dict:
                    posting = extract_posting(self.pos_dict[tkn]["path"])

                    df = len(posting)
                    tf = TF[tkn]

                    vector[tkn] = tf_idf(tf, df, 5)
                else:
                    self.log(f'"{tkn}" does not exist in dictionary')

        return vector

    def get_tf(self, tkns):
        TF = {}
        for tkn in tkns:
            tkn = tkn["stem"]
            if tkn not in TF:
                TF[tkn] = 0
            TF[tkn] += 1
        return TF
