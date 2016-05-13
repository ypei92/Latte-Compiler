function transform_neuron_fn(fn, ensemble)
    function walker(node, cbdata, index, top_level, read)
        if !isa(node, Expr)
            return ASTWALK_RECURSE
        end
        if node.head == :(.) && node.args[1] == :neuron
            name = node.args[2].value
            N = ndims(cbdata.ensemble)
            if name == :index
                # N += 1  # batch_dim
                idx = :($(symbol(:_neuron_index_,N)) - 1)
                buffer = symbol(cbdata.ensemble.name, :value)
                for i in N-1:-1:1
                    size = :(size($buffer, $i))
                    idx = :($idx * $size + $(symbol(:_neuron_index_,i)) - 1)
                end
                return :($idx + 1)
            end
            name = symbol(cbdata.ensemble.name,name)
            idx = Any[symbol(:_neuron_index_,i) for i in 1:N]
            str_name = string(name)
            if !contains(str_name, "inputs")
                push!(cbdata.args, name)
            end
            return :($name[$(idx...)])
        elseif node.head == :ref
            for i in 2:length(node.args)
                node.args[i] = AstWalk(node.args[i], walker, cbdata)
            end
            result = AstWalk(node.args[1], walker, cbdata)
            str_target = string(result.args[1])
            if endswith(str_target, "inputs")
                @assert length(node.args[3:end]) == 0
                index = result.args[2:end]
                conn_index = node.args[2]
                result.args[1] = symbol(result.args[1], conn_index)
                push!(cbdata.args, result.args[1])
                node = Expr(:ref, result.args[1], index...)
            elseif contains(str_target, "inputs")
                conn_index = parse(Int, split(str_target, "inputs")[end])
                if cbdata.ensemble.connections[conn_index].is_one_to_one
                    # FIXME: Needs tiling enabled check
                    @assert length(node.args[2:end]) == 1 && node.args[2] == 1
                    if result.args[end] != :NOTILE
                        push!(result.args, :NOTILE)
                    end
                    return result
                else
                    node = Expr(:ref, result.args[1], node.args[2:end]..., result.args[2:end]...)
                end
            else
                node = Expr(:ref, result.args[1], node.args[2:end]..., result.args[2:end]...)
            end
            return node
        elseif node.head == :call && node.args[1] == :length
            node.args[2] = AstWalk(node.args[2], walker, cbdata)
            if isa(node.args[2], Expr) && node.args[2].head == :ref
                if contains(node.args[2].args[1], "inputs")
                    return Expr(:call, :size, node.args[2].args[1], 1)
                end
            end
        end
        ASTWALK_RECURSE
    end
    cbdata = NeuronTransformerData(ensemble)
    ast = AstWalk(fn, walker, cbdata)
    ast, cbdata.args
end