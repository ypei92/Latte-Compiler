#include <math.h>
struct SolverState{
    int iter;
    float obj_val;
    float learning_rate;
    float momentum;
    SolverState(int it, float val, float lr, float mom){
        iter = it;
        obj_val = val;
        learning_rate = lr;
        momentum = mom;
    }
};


struct LearningRatePolicy{
    virtual ~LearningRatePolicy(){}
};

struct Fixed : LearningRatePolicy{
    float base_lr;
};

struct Step : LearningRatePolicy{
    float base_lr;
    float gamma;
    int step_size;
    Step(){
        base_lr = 0.01;
        gamma = 0.1;
        step_size = 100000;
    }
    Step(float bl, float g, int ss){
        base_lr = bl;
        gamma = g;
        step_size = ss;
    }
};

struct Exp : LearningRatePolicy{
    float base_lr;
    float gamma;
    Exp(float bl, float g){
        base_lr = bl;
        gamma = g;
    }
};

struct Inv : LearningRatePolicy{
    float base_lr;
    float gamma;
    float power;
    Inv(float bl, float g, float p){
        base_lr = bl;
        gamma = g;
        power = p;
    }
};

struct Decay : LearningRatePolicy{
    float base_lr;
    float decay;
    Decay(float bl, float d){
        base_lr = bl;
        decay = d;
    }
};

struct Poly : LearningRatePolicy{
    float base_lr;
    float max_iter;
    float power;
    Poly(float bl, float mi, float p){
        base_lr = bl;
        max_iter = mi;
        power = p;
    }
};

void set_learning_rate(LearningRatePolicy* lrp, SolverState& ss){

    if(Fixed* pol = dynamic_cast<Fixed*>(lrp)){
        ss.learning_rate = pol->base_lr;
    } else if(Step* pol = dynamic_cast<Step*>(lrp)){
        ss.learning_rate = pol->base_lr * pow(pol->gamma, floor((float)(ss.iter) / pol->step_size));
    } else if(Exp* pol = dynamic_cast<Exp*>(lrp)){
        ss.learning_rate = pol->base_lr * pow(pol->gamma, (float) ss.iter);
    } else if(Inv* pol = dynamic_cast<Inv*>(lrp)){
        ss.learning_rate = pol->base_lr * pow((1 + pol->gamma * ss.iter), -pol->power);
    } else if(Decay* pol = dynamic_cast<Decay*>(lrp)){
        ss.learning_rate = pol->base_lr / (1 + ss.iter * pol->decay);
    } else if(Poly* pol = dynamic_cast<Poly*>(lrp)){
        ss.learning_rate = pol->base_lr * pow((1 - ss.iter / pol->max_iter), pol->power);
    }
}

struct MomentumPolicy{
    virtual ~MomentumPolicy(){}
};

struct MomFixed : MomentumPolicy{
    float base_mom;
    MomFixed(float bm){
        base_mom = bm;
    }
};

struct MomStep : MomentumPolicy{
    float base_mom;
    float gamma;
    int step_size;
    float max_mom;
    MomStep(float bm, float g, int ss, float mm){
        base_mom = bm;
        gamma = g;
        step_size = ss;
        max_mom = mm;
    }
};

struct MomLinear : MomentumPolicy{
    float base_mom;
    float gamma;
    int step_size;
    float max_mom;
    MomLinear(float bm, float g, int ss, float mm){
        base_mom = bm;
        gamma = g;
        step_size = ss;
        max_mom = mm;
    }
};

void set_momentum(MomentumPolicy* mp, SolverState& ss){

    if(MomFixed* pol = dynamic_cast<MomFixed*>(mp)){
        ss.momentum = pol->base_mom;
    } else if(MomStep* pol = dynamic_cast<MomStep*>(mp)){
        ss.momentum = min(pol->base_mom * pow(pol->gamma, floor((float)(ss.iter) / pol->step_size)), pol->max_mom);
    } else if(MomLinear* pol = dynamic_cast<MomLinear*>(mp)){
        ss.momentum = min(pol->base_mom + floor((float)(ss.iter) / pol->step_size) * pol->gamma, pol->max_mom);
    }
}

struct SolverParameters{
    LearningRatePolicy* lrp;
    MomentumPolicy* mp;
    int max_epoch;
    float regu_coef;
    SolverParameters(){
        lrp = new Decay(.01, 5.0e-7);
        mp = new MomFixed(0.9);
        max_epoch = 300;
        regu_coef = .0005;
    }
    SolverParameters(LearningRatePolicy* lp, MomentumPolicy* m, int me, float re){
        lrp = lp;
        mp = m;
        max_epoch = me;
        regu_coef = re;
    }
};

struct Solver{
    SolverParameters params;
    SolverState state;
    Solver(SolverParameters sp){
        params = sp;
        state = SolverState(0, 0.0, 0.0, 0.0);
    }
    Solver(SolverParameters sp, SolverState ss){
        params = sp;
        state = ss;
    }
};

void sgd_update(float learning_rate, float momentum, NArray param, NArray gradient, NArray hist){

}

void l2_regularization(float rc, NArray param, NArray gradient){

}

void regularize(Solver& solver, Net& net){
    for(int i = 0; i < net.params.size(); ++i){
        l2_regularization(solver.params.regu_coef * net.params[i]->regu_coef,
            net.params[i]->value, net.params[i]->gradient);
    }
}

void update(Solver& solver, Net& net){
    for(int i = 0; i < net.params.size(); ++i){
        l2_regularization(solver.params.regu_coef * net.params[i]->regu_coef,
            net.params[i]->value, net.params[i]->gradient);
        sgd_update(solver.learning_rate * net.params[i]->learning_rate, 
            solver.state.momentum, net.params[i]->value, net.params[i]->gradient,
            net.params[i]->hist);
    }
}

void update(Solver& solver, Param* param){
    float gradient = 0;
    l2_regularization(solver.params.regu_coef * param->regu_coef, param->value, gradient);
    sgd_update(solver.state.learning_rate * param->learning_rate,
        solver.state.momentum, param->value, gradent, param->hist);
}

void update(Solver& solver, Net& net, Param* param){
    for(int i = 0; i < net.params.size(); ++i){
        if(net.params[i] == param){
            update(solver, param);
        }
    }
}

void solve(Solver& solver, Net& net){
    set_learning_rate(solver.params.lrp, solver.state);
    set_momentum(solver.params.mp, solver.state);
    int curr_train_epoch = net.train_epoch;
    while(curr_train_epoch < solver.params.max_epoch){
        solver.state.iter += 1;
        forward(net, solver);
        clear_gd(net);
        backward(net, solver);
        solver.state.obj_val = get_loss(net);
        set_learning_rate(solver.params.lrp, solver.state);
        set_momentum(solver.params.mp, solver.state);
        clear_values(net);
        if(solver.state.iter % 20 == 0){
            cout << "LOSS: " << solver.state.obj_val << endl;
        }
    }
}

















































