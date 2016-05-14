    for ensemble in net.ensemble_list:
        if ensemble.ensemble_type == "DataEnsemble":
            old_list = []
            new_list = []
            d1 = 1
            for act in ensemble.forward_actuals_list:
                key = ensemble.name + "_" + act
                old_list.append(act)
                new_list.append(key)
                if key in net.buffer_list:
                    d1 = net.buffer_list[key].shape[0]
            y.setParam(old_list, new_list, 0, d1, False)
            y.visit(ensemble.forward_ast)
        elif ensemble.ensemble_type == "Ensemble":
            old_list = []
            new_list = []
            for act in ensemble.forward_actuals_list:
                if act == "neuron":
                    old_list.append(act)
                    new_list.append(ensemble.name)
            d1 = net.buffer_list[ensemble.name + "_weights"].shape[0]
            d2 = net.buffer_list[ensemble.name + "_weights"].shape[1]
            y.setParam(old_list, new_list, d1, d2, True)
            y.visit(ensemble.forward_ast)
        else:
            old_list = []
            new_list = []
            for act in ensemble.forward_actuals_list:
                old_list.append(act)
                if act == "loss":
                    new_list.append(act + "_value")
                    new_list.append(act + "_prob_0")
                elif act == "input":
                    new_list.append(ensemble.source_list[0].source_ensemble.name + "_value")
                elif act == "label":
                    new_list.append(act + "_value")
            d1 = ensemble.source_list[0].source_ensemble.neuron_size
            d2 = ensemble.neuron_size
            y.setParam(old_list, new_list, d1, d2, True)
            y.visit(ensemble.forward_ast)
        
    for ensemble in net.ensemble_list:
        if ensemble.ensemble_type == "DataEnsemble":
            old_list = []
            new_list = []
            d1 = 1
            for act in ensemble.forward_actuals_list:
                key = ensemble.name + "_" + act
                old_list.append(act)
                new_list.append(key)
                if key in net.buffer_list:
                    d1 = net.buffer_list[key].shape[0]
            y.setParam(old_list, new_list, 0, d1, False)
            y.visit(ensemble.backward_ast)
        elif ensemble.ensemble_type == "Ensemble":
            old_list = []
            new_list = []
            for act in ensemble.forward_actuals_list:
                if act == "neuron":
                    old_list.append(act)
                    new_list.append(ensemble.name)
            d1 = net.buffer_list[ensemble.name + "_weights"].shape[0]
            d2 = net.buffer_list[ensemble.name + "_weights"].shape[1]
            y.setParam(old_list, new_list, d1, d2, True)
            y.visit(ensemble.backward_ast)
        else:
            old_list = []
            new_list = []
            for act in ensemble.forward_actuals_list:
                old_list.append(act)
                if act == "loss":
                    new_list.append(act + "_value")
                    new_list.append(act + "_prob_0")
                elif act == "input":
                    new_list.append(ensemble.source_list[0].source_ensemble.name + "_value")
                elif act == "label":
                    new_list.append(act + "_value")
            d1 = ensemble.source_list[0].source_ensemble.neuron_size
            d2 = ensemble.neuron_size
            y.setParam(old_list, new_list, d1, d2, False)
            y.visit(ensemble.backward_ast)