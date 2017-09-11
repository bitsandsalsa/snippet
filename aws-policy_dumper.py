#!/usr/bin/env python

import argparse
import boto3
from pprint import pprint


def parse_args(args=None):
    parser = argparse.ArgumentParser()
    parser.add_argument('-p', '--profile', help='AWS profile')
    return parser.parse_args(args)

def main(args):
    sess = boto3.session.Session(profile_name=args.profile)
    iam_client = sess.client('iam')
    res = iam_client.list_policies()

    for policy in res['Policies']:
        print '== {} =='.format(policy['PolicyName'])
        res = iam_client.get_policy_version(PolicyArn=policy['Arn'],
                                            VersionId=policy['DefaultVersionId'])
        pprint(res['PolicyVersion']['Document'])


if __name__ == '__main__':
        main(parse_args())

