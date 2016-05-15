#include <omp.h>
#include <ctime>
#include <stdio.h>
using namespace std;
//std::vector<clock_t> tictoc_stack;
/*
void tic() {
    tictoc_stack.push(clock());
}

void toc() {
    std::cout << "Time elapsed: "
              << ((double)(clock() - tictoc_stack.top())) / CLOCKS_PER_SEC
              << std::endl;
    tictoc_stack.pop();
}
*/

int main(){
    //tic();
    //clock_t start;
    //start = std::clock();
    #pragma omp parallel
    printf("Hello\n");
    //printf("time: %f\n", (std::clock() - start) / (double)(CLOCKS_PER_SEC / 1000));
    printf("t:%d\n", omp_get_num_threads());
    //std::cout << "Time: " << (std::clock() - start) / (double)(CLOCKS_PER_SEC / 1000) << " ms" << std::endl;
    //toc();
    return 0;
}