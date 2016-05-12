num_of_threads = 4;

class Buffer:
    def __init__(self, new = True, src = None, reshape = False):
        self.init_func = None
        self.shape = None
        self.name = None 
        self.new = new
        self.src = src
        self.reshape = reshape

for ensemble in net.ensemble_list:
    for field in ensemble.neuron_field_list:
        if field.name == "inputs" || field.name == "gd_inputs":
            pass
        elif field.name == "value" || field.name == "gd_value":
            buff = Buffer()
            buff.init_func = "zeros"
            buff.shape = (ensemble.neuron_size, net.batch_size)
            buff.name = ensemble.name + "_" + field.name
            net.buffer_list[buff.name] = buff
        elif field.type != "float" || field.type != "int":
            buff = Buffer()
            buff.init_func = field.init
            buff.shape = (field.size, ensemble.neuron_size)
            buff.name = ensemble.name + "_" + field.name
            net.buffer_list[buff.name] = buff
        else:
            buff = Buffer()
            buff.init_func = field.init
            buff.shape = (ensemble.neuron_size,)
            buff.name = ensemble.name + "_" + field.name
            net.buffer_list[buff.name] = buff

for ensemble in net.ensemble_list:
    for field in ensemble.neuron_field_list:
        if field.name == "inputs" || field.name == "gd_inputs":
            attr = "value" if field.name == "inputs" else "gd_value"
            for (index, src) in enumerate(net.source_list):
                key = ensemble.name + "_" + field.name + "_" + str(index)
                src_buff = src.name + "_" + attr
                if src_buff in net.buffer_list:
                    if src.is_dim_fixed:
                        src.copy = False
                        buff = Buffer(False, net.buffer_list[src_buff], True)
                        buff.shape = (src.size, net.batch_size)
                        buff.name = key
                        net.buffer_list[buff.name] = buff
                    elif src.is_one_to_one:
                        src.copy = False
                        buff = Buffer(False, net.buffer_list[src_buff])
                        buff.name = key
                        net.buffer_list[buff.name] = buff
                    else:
                        #TODO
                        pass
                else:
                    buff = Buffer()
                    buff.init_func = field.init
                    buff.shape = (0,)
                    buff.name = key
                    net.buffer_list[buff.name] = buff
