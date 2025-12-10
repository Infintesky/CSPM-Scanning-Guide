#!/usr/bin/env python3
"""
Convert ScoutSuite AWS results (JS format) to CSV with all findings
"""

import json
import csv
import sys
from pathlib import Path


def parse_scoutsuite_js(filepath: str) -> dict:
    """Parse ScoutSuite JS file (strips 'scoutsuite_results =' prefix)."""
    with open(filepath, 'r') as f:
        content = f.read()
    
    # Remove the JS variable assignment
    json_str = content.replace('scoutsuite_results =', '', 1).strip()
    return json.loads(json_str)


def resolve_resource_path(data: dict, path: str) -> dict | None:
    """
    Resolve a ScoutSuite resource path to the actual resource object.
    Paths look like: 'iam.users.USERID.some_flag' or 's3.buckets.BUCKETID.something'
    """
    parts = path.split('.')
    current = data.get('services', {})
    
    for part in parts:
        if isinstance(current, dict):
            # Try direct key access
            if part in current:
                current = current[part]
            # Try 'regions' nested structure (e.g., ec2.regions.us-east-1.instances.ID)
            elif part == 'id':
                # 'id' is a placeholder, skip it
                continue
            else:
                return None
        else:
            return None
    
    return current if isinstance(current, dict) else None


def get_arn_from_path(data: dict, item_path: str) -> str:
    """
    Extract ARN from a resource path.
    Item paths look like: 'iam.users.USERID.flag' - we want the resource (user), not the flag.
    """
    parts = item_path.split('.')
    
    services = data.get('services', {})
    
    current = services
    resource_with_arn = None
    
    for i, part in enumerate(parts):
        if not isinstance(current, dict):
            break
        
        if part in current:
            current = current[part]
            # Check if this level has an ARN
            if isinstance(current, dict) and 'arn' in current:
                resource_with_arn = current
        else:
            break
    
    if resource_with_arn:
        return resource_with_arn.get('arn', '')
    
    return ''


def extract_all_findings(data: dict) -> list[dict]:
    """Extract all findings (flagged or not), one row per affected resource."""
    findings_list = []
    
    services = data.get('services', {})
    account_id = data.get('account_id', '')
    environment = data.get('environment', '')
    
    for service_name, service_data in services.items():
        findings = service_data.get('findings', {})
        
        for finding_id, finding in findings.items():
            flagged = finding.get('flagged_items', 0) > 0
            items = finding.get('items', [])
            
            # Base finding info
            base_info = {
                'account_id': account_id,
                'environment': environment,
                'service': finding.get('service', service_name),
                'finding_id': finding_id,
                'description': finding.get('description', ''),
                'level': finding.get('level', ''),
                'flagged': flagged,
                'flagged_items': finding.get('flagged_items', 0),
                'checked_items': finding.get('checked_items', 0),
                'rationale': finding.get('rationale', ''),
                'remediation': finding.get('remediation') or '',
                'references': '; '.join(finding.get('references') or []) if isinstance(finding.get('references'), list) else str(finding.get('references') or ''),
                'compliance': json.dumps(finding.get('compliance')) if finding.get('compliance') else '',
            }
            
            if items:
                # One row per affected resource
                for item_path in items:
                    row = base_info.copy()
                    row['resource_path'] = item_path
                    row['arn'] = get_arn_from_path(data, item_path)
                    findings_list.append(row)
            else:
                # No specific items - just one row for the finding
                row = base_info.copy()
                row['resource_path'] = ''
                row['arn'] = ''
                findings_list.append(row)
    
    return findings_list


def write_csv(findings: list[dict], output_path: str):
    """Write findings to CSV."""
    if not findings:
        print("No findings found.")
        return
    
    fieldnames = [
        'account_id', 'environment', 'service', 'finding_id', 'description',
        'level', 'flagged', 'flagged_items', 'checked_items', 'arn', 'resource_path',
        'rationale', 'remediation', 'references', 'compliance'
    ]
    
    with open(output_path, 'w', newline='', encoding='utf-8') as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(findings)
    
    print(f"Wrote {len(findings)} finding rows to {output_path}")


def main():
    if len(sys.argv) < 2:
        print("Usage: python scoutsuite_to_csv.py <input.js> [output.csv]")
        sys.exit(1)
    
    input_path = sys.argv[1]
    output_path = sys.argv[2] if len(sys.argv) > 2 else Path(input_path).stem + '_findings.csv'
    
    data = parse_scoutsuite_js(input_path)
    findings = extract_all_findings(data)
    write_csv(findings, output_path)


if __name__ == '__main__':
    main()