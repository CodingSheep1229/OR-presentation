param N;# of station
param P;# max cap of truck 
param S;# max # of section
param Dis{i in 1..N, j in 1..N};
param Fixed_cost;
param Var_cost;

param In{i in 1..N}binary;
param Out{i in 1..N}binary;

param Available_bike{i in 1..N};
param Total_cap{i in 1..N};

var Load{i in 1..N, j in 1..N, s in 1..S};
var K{i in 1..N, j in 1..N, s in 1..S}binary;

minimize cost:
    sum{i in 1..N} sum{j in 1..N} sum{s in 1..S} (Load[i,j,s] * Var_cost * Dis[i,j] + K[i,j,s] * Fixed_cost);

# subject to Connected_route1{i in 1..N, j in 1..N, k in 1..N, s in 1..S-1}:
#     K[i,j,s] <= K[j,k,s+1];

subject to Connected_all{s in 1..S-1}:
    sum{i in 1..N} sum{j in 1..N} K[i,j,s] >= sum{i in 1..N} sum{j in 1..N}K[i,j,s+1];    

subject to Connected_route3{j in 1..N, s in 1..S-1}:
    sum{i in 1..N}K[i,j,s] >= sum{k in 1..N}K[j,k,s+1]; 

subject to Connected_route4{i in 1..N, s in 1..S}:
    K[i,i,s] = 0;

#subject to Connected_route2{i in 1..N, j in 1..N, k in 1..N, s in 1..S-1}:
#    K[j,k,s+1] <= K[i,j,s]; 

subject to Travel_a_place_each_time{s in 1..S}:
    sum{i in 1..N} sum{j in 1..N} K[i,j,s] <= 1;

subject to Allowed_to_be_imported{i in 1..N, j in 1..N, s in 1..S}:
    In[j] * Total_cap[i] >= Load[i,j,s];

subject to Allowed_to_be_exported{i in 1..N, j in 1..N, s in 1..S}:
    Out[i] * Total_cap[i] >= Load[i,j,s];

subject to Truck_cap{i in 1..N, j in 1..N, s in 1..S}:
    Load[i,j,s] <= P;

subject to Binary_con{i in 1..N, j in 1..N, s in 1..S}:
    Load[i,j,s] <= K[i,j,s] * Total_cap[i];

subject to Fullfill_upper_bound{i in 1..N}:
    Available_bike[i] - sum{j in 1..N} sum{s in 1..S}Load[i,j,s] + sum{j in 1..N} sum{s in 1..S}Load[j,i,s] <= 0.8 * Total_cap[i];

subject to Fullfill_lower_bound{i in 1..N}:
    Available_bike[i] - sum{j in 1..N}sum{s in 1..S} Load[i,j,s] + sum{j in 1..N} sum{s in 1..S}Load[j,i,s] >= 0.2 * Total_cap[i];

subject to non_neg{i in 1..N, j in 1..N, s in 1..S}:
    Load[i,j,s] >= 0;
