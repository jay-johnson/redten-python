import uuid, json, os, sys, datetime
import time
import requests

from redten.shellprinting import good, boom, anmt, lg, mark

from unittest import TestCase

class TestAPI(TestCase):
       
    debug = True
    user = None

    def setUp(self):

        lg("")
        lg("")
        lg("--------------------------------------")
        lg("Setting up")

    # end of setUp


    def tearDown(self):
        lg("Tearing Down")
        if self.user:
            delete_result = self.user.delete()
            lg("User Delete Status=" + str(delete_result))
    # end of tearDown


    def dlg(self, msg, level=6):
        if self.debug:
            lg(msg, level)
    # end of dlg


    def test_that_tests_work(self):
        lg(str(__name__) + " - start")
        assert(1 == 1)
        lg(str(__name__) + " - end")
    # end of test_that_tests_work


# end of TestAPI
