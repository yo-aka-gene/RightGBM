library(gprofiler2)

egost <- function(
    gene,
    organism="hsapiens",
    correction_method="fdr", 
    user_threshold=0.05, 
    domain_scope="annotated",
    sources="GO"
){
    stopifnot(is.vector(gene))
    stopifnot(is.character(gene))
    stopifnot(is.character(organism))
    stopifnot(is.character(correction_method))
    stopifnot(is.numeric(user_threshold))
    return(
        gost(
            query=gene,
            organism=organism,
            correction_method=correction_method,
            user_threshold=user_threshold,
            domain_scope=domain_scope,
            sources=sources
        )
    )
}
