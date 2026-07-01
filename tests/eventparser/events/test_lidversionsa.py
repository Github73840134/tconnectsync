#!/usr/bin/env python3

import json
import unittest

from tconnectsync.eventparser.generic import Event
from tconnectsync.eventparser import events as eventtypes
from tconnectsync.eventparser.raw_event import RawEvent


class TestLidVersionsA(unittest.TestCase):
    """307 / LID_VERSIONS_A: four plain uint32 version/part-number fields.
    Only one distinct capture shape exists, so a single real fixture suffices."""
    maxDiff = None

    def setUp(self):
        # Real captured LID_VERSIONS_A event, copied verbatim.
        self.fixtureVersions = {
            "deviceAssignmentId": "4ff6bebc-d4d6-4423-b123-eecfcf5a4238",
            "eventCode": 307,
            "sequenceGroup": 0,
            "sequenceNumber": 393111,
            "pumpDateTime": "2026-04-30T00:00:06",
            "eventProperties": {
                "armPartNumber": 1016587,
                "armSwVersion": 1108201743,
                "blePartNumber": 1016587,
                "bleSwVersion": 1108201743,
            },
            "estimatedDateTime": "2026-04-30T00:00:06Z",
        }

    def test_dispatches_to_lidversionsa(self):
        ev = Event(self.fixtureVersions)
        self.assertIsInstance(ev, eventtypes.LidVersionsA)
        self.assertNotIsInstance(ev, RawEvent)

    def test_envelope_fields(self):
        ev = Event(self.fixtureVersions)
        self.assertEqual(ev.eventId, 307)
        self.assertEqual(ev.seqNum, 393111)

    def test_timestamp_preserves_wall_clock(self):
        ev = Event(self.fixtureVersions)
        self.assertEqual(ev.eventTimestamp.format('YYYY-MM-DDTHH:mm:ss'),
                         "2026-04-30T00:00:06")

    def test_plain_fields_round_trip(self):
        ev = Event(self.fixtureVersions)
        self.assertEqual(ev.armpartnumber, 1016587)
        self.assertEqual(ev.armswversion, 1108201743)
        self.assertEqual(ev.blepartnumber, 1016587)
        self.assertEqual(ev.bleswversion, 1108201743)

    def test_todict_is_json_serializable(self):
        ev = Event(self.fixtureVersions)
        d = ev.todict()
        json.dumps(d)  # must not raise
        self.assertEqual(d["id"], 307)
        self.assertEqual(d["name"], "LID_VERSIONS_A")
        self.assertEqual(d["seqNum"], 393111)
        self.assertEqual(d["armpartnumber"], 1016587)
        self.assertEqual(d["armswversion"], 1108201743)
        self.assertEqual(d["blepartnumber"], 1016587)
        self.assertEqual(d["bleswversion"], 1108201743)


if __name__ == "__main__":
    unittest.main()
