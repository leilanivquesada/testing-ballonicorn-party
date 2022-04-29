"""Testsq for Balloonicorn's Flask app."""

import unittest
import party


class PartyTests(unittest.TestCase):
    """Tests for my party site."""

    def setUp(self):
        """Code to run before every test."""

        self.client = party.app.test_client()
        party.app.config['TESTING'] = True

    def test_homepage(self):
        """Can we reach the homepage?"""

        result = self.client.get("/")
        self.assertIn(b"having a party", result.data)

    def test_no_rsvp_yet(self):
        """Do users who haven't RSVPed see the correct view?"""

        # Add a test to show we haven't RSVP'd yet
        # client = party.app.test_client()
        result = self.client.get('/')
        self.assertIn(b'<h2>Please RSVP</h2>', result.data)
        
        # print("PASSED, shows RSVP heading")

    def test_rsvp(self):
        """Do RSVPed users see the correct view?"""

        rsvp_info = {'name': "Jane", 'email': "jane@jane.com"}

        result = self.client.post("/rsvp", data=rsvp_info,
                                  follow_redirects=True)

        # check that once we log in we see party details--but not the form!
        self.assertIn(b"<h2>Party Details</h2>", result.data)
        self.assertNotIn(b"Please RSVP", result.data)
        

    def test_rsvp_mel(self):
        """Can we keep Mel out?"""
        rsvp_info = {'name': "Mel Melitpolski", 'email': 'mel@ubermelons.com'}
        
        result = self.client.post("/rsvp", data=rsvp_info, follow_redirects=True)
        # test that mel can't invite himself
        self.assertNotIn(b"<h2>Party Details</h2>", result.data)
        self.assertIn(b"Please RSVP", result.data)


if __name__ == "__main__":
    unittest.main()
