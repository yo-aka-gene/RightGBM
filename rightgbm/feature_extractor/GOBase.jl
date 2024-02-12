module GOBase
export enrichment
using RCall
using Base: source_path

rscript_path = joinpath(
    dirname(source_path(@__FILE__)), 
    "gprofiler.R"
)

R"source($rscript_path)"


function enrichment(
    gene; organism="hsapiens", correction_method="fdr", user_threshold=0.05, domain_scope="annotated",  sources="GO"
    )
    return rcopy(
        R"""
        egost(
            gene = $gene, 
            organism = $organism, 
            correction_method = $correction_method,
            user_threshold = $user_threshold,
            domain_scope = $domain_scope,
            source = $source
        )
        """
    )
end

end
