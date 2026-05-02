#!/usr/bin/env python3

import argparse
import sys
from pymongo import MongoClient

DB_URI = "mongodb://127.0.0.1/open5gs"

IMS_BASE = "208930000000000"

DEFAULT_SECURITY = {
    "k": "465B5CE8 B199B49F AA5F0A2E E238A6BC",
    "amf": "8000",
}

OP_VALUE = "E8ED289D EBA952E4 283B54E8 8E6183CA"
OPC_VALUE = "E8ED289D EBA952E4 283B54E8 8E6183CA"


def make_subscriber(imsi, use_op=True):
    sec = dict(DEFAULT_SECURITY)
    if use_op:
        sec["op"] = OP_VALUE
        # sec["opc"] = None
    else:
        # sec["op"] = None
        sec["opc"] = OPC_VALUE

    return {
        "schema_version": 1,
        "imsi": imsi,
        "msisdn": [],
        "imeisv": [],
        "mme_host": [],
        "mme_realm": [],
        "purge_flag": [],
        "access_restriction_data": 32,
        "subscriber_status": 0,
        "operator_determined_barring": 0,
        "network_access_mode": 0,
        "subscribed_rau_tau_timer": 12,
        "ambr": {
            "downlink": {"value": 1, "unit": 3},
            "uplink": {"value": 1, "unit": 3},
        },
        "security": sec,
        "slice": [
            {
                "sst": 1,
                "default_indicator": True,
                "session": [
                    {
                        "name": "internet",
                        "type": 3,
                        "qos": {
                            "index": 9,
                            "arp": {
                                "priority_level": 8,
                                "pre_emption_capability": 1,
                                "pre_emption_vulnerability": 1,
                            },
                        },
                        "ambr": {
                            "downlink": {"value": 1, "unit": 3},
                            "uplink": {"value": 1, "unit": 3},
                        },
                        "pcc_rule": [],
                    }
                ],
            }
        ],
    }


def create_subscribers(n, use_op=True):
    client = MongoClient(DB_URI)
    db = client["open5gs"]
    col = db["subscribers"]

    docs = []
    base = int(IMS_BASE)
    for i in range(1, n + 1):
        imsi = str(base + i)
        docs.append(make_subscriber(imsi, use_op))

    try:
        result = col.insert_many(docs, ordered=False)
        print(f"Inserted {len(result.inserted_ids)} subscribers ({'OP' if use_op else 'OPC'})")
    except Exception as e:
        print(f"Error inserting subscribers: {e}")
        sys.exit(1)
    finally:
        client.close()


def clean_subscribers():
    client = MongoClient(DB_URI)
    db = client["open5gs"]
    col = db["subscribers"]

    try:
        result = col.delete_many({})
        print(f"Deleted {result.deleted_count} subscribers")
    except Exception as e:
        print(f"Error deleting subscribers: {e}")
        sys.exit(1)
    finally:
        client.close()


def main():
    parser = argparse.ArgumentParser(description="Open5GS subscriber management")
    sub = parser.add_subparsers(dest="command")

    ue_parser = sub.add_parser("ue", help="Manage UEs/subscribers")
    ue_group = ue_parser.add_mutually_exclusive_group()
    ue_group.add_argument("--op", action="store_true", help="Use OP (default)")
    ue_group.add_argument("--opc", action="store_true", help="Use OPC")
    ue_parser.add_argument("-n", type=int, default=1, help="Number of UEs to create")
    ue_parser.add_argument("-c", action="store_true", help="Clean all subscribers")

    args = parser.parse_args()

    if args.command != "ue":
        parser.print_help()
        sys.exit(1)

    if args.c:
        clean_subscribers()
    else:
        use_op = not args.opc
        create_subscribers(args.n, use_op)


if __name__ == "__main__":
    main()
