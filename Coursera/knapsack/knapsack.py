
class KnapsackSolver:
    """Solves the single Knapsack problem
    Args:
    n: Number of items
    K: Knapsack capacity
    v: Dictionary with value of each item
    w: Dictionary with weight of each item
    """

    def __init__(self, n: int, K: float, v: dict, w: dict) -> None:
        self.n = n
        self.K = K
        self.v = v
        self.w = w
        self.sol = list()

    @property
    def obj(self):
        return sum(self.v[i] for i in self.sol)

    @property
    def weight(self):
        return sum(self.w[i] for i in self.sol)

    def greedy_solve(self, by='value'):
        # sort by value
        if by == 'value':
            for item in sorted(self.v, key=self.v.get, reverse=True):
                if self.weight + self.w[item] <= self.K:
                    self.sol.append(item)
        # sort by weight
        elif by == 'weight':
            for item in sorted(self.w, key=self.w.get):
                if self.weight + self.w[item] <= self.K:
                    self.sol.append(item)
        # sort by ratio
        elif by == 'ratio':
            ratio = {i: t[0] / t[1] for i, t in enumerate(zip(self.v.values(), self.w.values()))}
            for item in sorted(ratio, key=ratio.get, reverse=True):
                if self.weight + self.w[item] <= self.K:
                    self.sol.append(item)
        return self.sol

    def mip_solver(self):
        import pyomo.environ as pe
        self.sol = []

        m = pe.ConcreteModel()

        m.i = pe.Set(initialize=list(self.v.keys()))
        m.x = pe.Var(m.i, domain=pe.Binary, initialize=0)

        m.capacity = pe.Constraint(expr=pe.quicksum(self.w[i] * m.x[i] for i in m.i) <= self.K)

        m.obj = pe.Objective(expr=pe.quicksum(self.v[i] * m.x[i] for i in m.i), sense=pe.maximize)

        opt = pe.SolverFactory('scip')
        opt.solve(m, tee=False)

        for i in m.i:
            if pe.value(m.x[i]) > 0.0001:
                self.sol.append(i)
        return self.sol

    def cp_solver(self):
        from ortools.sat.python import cp_model
        self.sol = []

        m = cp_model.CpModel()

        x = {}
        for i in self.v.keys():
            x[i] = m.NewBoolVar(f'x{i}')

        m.Add(sum(self.w[i] * x[i] for i in self.v.keys()) <= self.K)

        profit = sum(self.v[i] * x[i] for i in self.v.keys())
        m.Maximize(profit)

        solver = cp_model.CpSolver()
        solver.parameters.num_search_workers = 6
        solver.parameters.max_time_in_seconds = 100.0
        solver.parameters.log_search_progress = False
        solver.Solve(m)

        for i in self.v.keys():
            if solver.BooleanValue(x[i]):
                self.sol.append(i)
        return self.sol


if __name__ == '__main__':
    v = dict()
    w = dict()
    with open('data/ks_500_0', 'r') as f:
        n, K = [int(x) for x in f.readline().split(' ')]
        for index, line in enumerate(f):
            v[index], w[index] = [int(x) for x in line.split(' ')]
    sorter = ['value', 'weight', 'ratio']
    for s in sorter:
        a = KnapsackSolver(n, K, v, w)
        sol = a.greedy_solve(by=s)
        print(s, a.obj)

    a.mip_solver()
    print('mip', a.obj)

    a.cp_solver()
    print('cp', a.obj)
