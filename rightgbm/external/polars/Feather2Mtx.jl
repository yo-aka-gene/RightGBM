module Feather2Mtx
using Feather
using SparseArrays


function feather2mtx(from::AbstractString, to::AbstractString)
    df = Feather.read(from)
    sparse_matrix = sparse(convert(Matrix, df))
    SparseArrays.sparsematrix_market(to, sparse_matrix)
end

end
