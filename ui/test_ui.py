import pytest
from ui.ui import UI

def test_parse_input_low_power():
    ui = UI()
    args = ui._UI__parse_input(['lp','-add','-bw','32','-area','-t','23','-mina', '0', '-maxa', '10'])  
    assert args.circuit_type == 'lp'
    assert args.add == True
    assert args.sub == False
    assert args.div == False
    assert args.mul == False
    assert args.bitwidth == 32
    assert args.area == True
    assert args.delay == False
    assert args.power == False
    assert args.threshold == 23
    assert args.mina == 0
    assert args.maxa == 10

def test_parse_input_mul_delay():
    ui = UI()
    args = ui._UI__parse_input(['lp','-mul','-bw','32','-delay','-t','23','-mina', '0', '-maxa', '10'])  
    assert args.circuit_type == 'lp'
    assert args.add == False
    assert args.sub == False
    assert args.div == False
    assert args.mul == True
    assert args.bitwidth == 32
    assert args.area == False
    assert args.delay == True
    assert args.power == False
    assert args.threshold == 23
    assert args.mina == 0
    assert args.maxa == 10

def test_parse_input_high_performance():
    ui = UI()
    args = ui._UI__parse_input(['hp','-div','-bw','64','-power','-t','90.23','-minr', '1', '-maxr', '2','-minp', '3', '-maxp', '4'])  
    assert args.circuit_type == 'hp'
    assert args.add == False
    assert args.sub == False
    assert args.div == True
    assert args.mul == False
    assert args.bitwidth == 64
    assert args.area == False
    assert args.delay == False
    assert args.power == True
    assert args.threshold == 90.23
    assert args.minr == 1
    assert args.maxr == 2
    assert args.minp == 3
    assert args.maxp == 4

def test_parse_input_circuit_type_missing():
    ui = UI()
    with pytest.raises(SystemExit):
        args = ui._UI__parse_input(['-mul','-bw','32','-delay','-t','23','-mina', '0', '-maxa', '10'])

def test_parse_input_operation_missing():
    ui = UI()
    with pytest.raises(SystemExit):
        args = ui._UI__parse_input(['lp','-bw','32','-delay','-t','23','-mina', '0', '-maxa', '10']) 

def test_parse_input_bw_missing():
    ui = UI()
    with pytest.raises(SystemExit):
        args = ui._UI__parse_input(['lp','-mul','-delay','-t','23','-mina', '0', '-maxa', '10'])

def test_parse_input_characteristic_missing():
    ui = UI()
    with pytest.raises(SystemExit):
        args = ui._UI__parse_input(['lp','-mul','-delay','-t','23','-mina', '0', '-maxa', '10']) 

def test_parse_input_threshold_missing():
    ui = UI()
    with pytest.raises(SystemExit):
        args = ui._UI__parse_input(['lp','-mul','-bw','32','-delay','-mina', '0', '-maxa', '10']) 

def test_parse_input_lp_mina_missing():
    ui = UI()
    with pytest.raises(SystemExit):
        args = ui._UI__parse_input(['lp','-mul','-bw','32','-delay','-t','23','-maxa', '10'])

def test_parse_input_lp_mixa_missing():
    ui = UI()
    with pytest.raises(SystemExit):
        args = ui._UI__parse_input(['lp','-add','-bw','32','-area','-t','23','-mina', '0']) 

def test_parse_input_hp_minr_missing():
    ui = UI()
    with pytest.raises(SystemExit):
        args = ui._UI__parse_input(['hp','-div','-bw','64','-power','-t','90.23','-maxr', '2','-minp', '3', '-maxp', '4']) 

def test_parse_input_hp_maxr_missing():
    ui = UI()
    with pytest.raises(SystemExit):
        args = ui._UI__parse_input(['hp','-div','-bw','64','-power','-t','90.23','-minr', '1','-minp', '3', '-maxp', '4'])         

def test_parse_input_hp_minp_missing():
    ui = UI()
    with pytest.raises(SystemExit):
        args = ui._UI__parse_input(['hp','-div','-bw','64','-power','-t','90.23','-minr', '1', '-maxr', '2', '-maxp', '4']) 

def test_parse_input_hp_maxp_missing():
    ui = UI()
    with pytest.raises(SystemExit):
        args = ui._UI__parse_input(['hp','-div','-bw','64','-power','-t','90.23','-minr', '1', '-maxr', '2','-minp', '3'])     