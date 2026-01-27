from  retrieval.query_expander import QueryExpander

expander = QueryExpander(n_queries=4)

queries = expander.expand(
    "How does FAISS store and search vectors ?"
)

for q in queries:
    print("-", q)