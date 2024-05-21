# information-retrieval-system

query rules:

    - operators: AND, NOT, OR, \\N

    - the left operand is always considered a sentence
    - the right operand is always considered a word

    - SENTENCE AND WORD ==> the documents which has the "sentence + word" sentence in them
        - ali va hasan AND came == ali va hasan came

    - SENTENCE OR WORD ==> ?
        - ali va hasan OR came == ali va (hasan OR came)

    - SENTENCE NOT WORD ==> the document which have the SENTENCE in them except those who has WORD just after the SENTENCE
        - ali va hasan NOT came == (ali va hasan) - (ali va hasan came)

    - SENTENCE \\5 WORD ==> same as: SENTENCE AND WORD (with 5-2 offset)

    - no symbols beside operators
