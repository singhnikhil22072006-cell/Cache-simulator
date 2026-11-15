from backend.core.metrics import calculate_metrics
from tests.helpers import CONFIG

def test_amat_calculation():
    rows=[{"l1_hit":True,"l2_hit":None,"memory":False},
          {"l1_hit":False,"l2_hit":True,"memory":False},
          {"l1_hit":False,"l2_hit":False,"memory":True},
          {"l1_hit":True,"l2_hit":None,"memory":False}]
    m=calculate_metrics(rows,CONFIG)
    assert m["l1_hits"] == 2
    assert m["l2_hits"] == 1
    assert m["memory_misses"] == 1
    expected=1 + .5*(8 + .5*100)
    assert abs(m["amat"]-expected) < 1e-9
