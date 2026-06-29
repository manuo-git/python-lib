# name: Saiki
# prefix: saiki
# ---
import pypyjit, sys
pypyjit.set_param('max_unroll_recursion=-1')
sys.setrecursionlimit(10**6)