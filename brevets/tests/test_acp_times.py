"""
Nose tests for acp_times.py

Write your tests HERE AND ONLY HERE.
"""
import acp_times
import arrow
import nose    # Testing framework
import logging
logging.basicConfig(format='%(levelname)s:%(message)s',
                    level=logging.WARNING)
log = logging.getLogger(__name__)


starttime = arrow.get(2021,1,1)
def test_brevit200():
    s100 = starttime.shift(hours=+2,minutes=+56)
    s200 = starttime.shift(hours=+5,minutes=+53)
    assert(acp_times.open_time(0, 200, starttime) == starttime)
    assert(acp_times.open_time(100, 200, starttime) ==  s100)
    assert(acp_times.open_time(240, 200, starttime) == s200)

    s0 = starttime.shift(hours=+1)
    s100 = starttime.shift(hours=+6, minutes=+40)
    s200 = starttime.shift(hours=+13, minutes=+ 30)
    assert(acp_times.close_time(0, 200, starttime) == s0)
    assert(acp_times.close_time(100, 200, starttime) == s100)
    assert(acp_times.close_time(240, 200, starttime) == s200)

def test_brevit300():
    s199 = starttime.shift(hours=+5,minutes=+51)
    s201 = starttime.shift(hours=5,minutes=+55)
    s360 = starttime.shift(hours=+9.0000)
    assert(acp_times.open_time(199, 300,starttime) == s199)
    assert(acp_times.open_time(201, 300,starttime) == s201)


    s199 = starttime.shift(hours=+13, minutes=+16)
    s201 = starttime.shift(hours=+13, minutes=+24)
    s360 = starttime.shift(hours=+20.0000)
    assert(acp_times.close_time(199, 400,starttime) == s199)
    assert(acp_times.close_time(201, 400,starttime) == s201)


def test_brevit400():

    s199 = starttime.shift(hours=+5, minutes=+51)
    s201 = starttime.shift(hours=+5, minutes=+55)
    s360 = starttime.shift(hours=+10, minutes=+53)
    s460 = starttime.shift(hours=+12, minutes=+8)
    assert(acp_times.open_time(199, 400,starttime) == s199)
    assert(acp_times.open_time(201, 400,starttime) == s201)
    assert(acp_times.open_time(360, 400,starttime) == s360)
    assert(acp_times.open_time(460, 400,starttime) == s460)

    s199 = starttime.shift(hours=+13, minutes=+16)
    s201 = starttime.shift(hours=+13, minutes=+24)
    s360 = starttime.shift(hours=+24, minutes=+0)
    s460 = starttime.shift(hours=+27, minutes=+0)
    assert(acp_times.close_time(199, 400,starttime) == s199)
    assert(acp_times.close_time(201, 400,starttime) == s201)
    assert(acp_times.close_time(360, 400,starttime) == s360)
    assert(acp_times.close_time(460, 400,starttime) == s460)


def test_brevit600():
        s170 = starttime.shift(hours=+5, minutes=+00)
        s370 = starttime.shift(hours=+11, minutes=+12)
        s700 = starttime.shift(hours=+18, minutes=+48)
        assert(acp_times.open_time(170, 600,starttime) ==s170)
        assert(acp_times.open_time(370, 600,starttime) ==s370)
        assert(acp_times.open_time(700, 600,starttime) ==s700)

        s170 = starttime.shift(hours=+11, minutes=+20)
        s370 = starttime.shift(hours=+24, minutes=+40)
        s700 = starttime.shift(hours=+40, minutes=+0)
        assert(acp_times.close_time(170, 600,starttime) ==s170)
        assert(acp_times.close_time(370, 600,starttime) ==s370)
        assert(acp_times.close_time(700, 600,starttime) ==s700)

def test_brevit1000():
        s230 = starttime.shift(hours=+6, minutes=+49)
        s430 = starttime.shift(hours=+13, minutes=+8)
        s630 = starttime.shift(hours=+19, minutes=+52)
        s1150 = starttime.shift(hours=+33, minutes=+5)
        assert(acp_times.open_time(230, 1000,starttime) == s230)
        assert(acp_times.open_time(430, 1000,starttime) == s430)
        assert(acp_times.open_time(630, 1000,starttime) == s630)
        assert(acp_times.open_time(1150, 1000,starttime) == s1150)


        s230 = starttime.shift(hours=+15, minutes=+20)
        s430 = starttime.shift(hours=+28, minutes=+40)
        s630 = starttime.shift(hours=+42, minutes=+38)
        s1150 = starttime.shift(hours=+75)


        assert(acp_times.close_time(230, 1000,starttime) == s230)
        assert(acp_times.close_time(430, 1000,starttime) == s430)
        assert(acp_times.close_time(630, 1000,starttime) == s630)
        assert(acp_times.close_time(1150, 1000,starttime) == s1150)
