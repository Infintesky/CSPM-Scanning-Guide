#!/usr/bin/env python3
"""
Convert ScoutSuite results (JS format) to CSV with all findings.
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


import re


def strip_html_tags(text: str) -> str:
    """Remove HTML tags and clean up whitespace."""
    if not text:
        return ''
    # Remove HTML tags
    clean = re.sub(r'<[^>]+>', ' ', text)
    # Normalize whitespace
    clean = re.sub(r'\s+', ' ', clean).strip()
    return clean


def extract_scout_id(item_path: str) -> str:
    """Extract scout ID from a resource path."""
    import re
    # Match scoutid-XXX pattern
    match = re.search(r'(scoutid-[a-f0-9]+)', item_path)
    return match.group(1) if match else ''


def get_resource_from_path(data: dict, item_path: str) -> dict | None:
    """
    Navigate a ScoutSuite path and return the deepest resource object found.
    """
    parts = item_path.split('.')
    services = data.get('services', {})
    
    current = services
    last_resource = None
    
    for part in parts:
        if not isinstance(current, dict):
            break
        
        if part in current:
            current = current[part]
            # If it looks like a resource (has 'name' or 'id'), remember it
            if isinstance(current, dict) and ('name' in current or 'id' in current):
                last_resource = current
        else:
            break
    
    return last_resource


def get_resource_id(data: dict, item_path: str, provider: str) -> str:
    """
    Extract resource identifier from a path.
    - AWS: returns ARN
    - Azure: constructs resource ID from components
    """
    resource = get_resource_from_path(data, item_path)
    
    if not resource:
        return ''
    
    if provider == 'aws':
        return resource.get('arn', '')
    
    elif provider == 'azure':
        # Try to find existing full resource ID
        for key in ['resource_id', 'id']:
            val = resource.get(key, '')
            if isinstance(val, str) and '/subscriptions/' in val:
                return val
        
        # Construct Azure resource ID from components
        # Path format: service.subscriptions.SUB_ID.resource_type.RESOURCE_ID
        parts = item_path.split('.')
        subscription_id = None
        for i, part in enumerate(parts):
            if part == 'subscriptions' and i + 1 < len(parts):
                subscription_id = parts[i + 1]
                break
        
        name = resource.get('name', '')
        rg = resource.get('resource_group_name', '')
        rtype = resource.get('type', '')
        
        if subscription_id and name and rg and rtype:
            return f"/subscriptions/{subscription_id}/resourceGroups/{rg}/providers/{rtype}/{name}"
        elif subscription_id and name:
            return f"/subscriptions/{subscription_id}/.../{name}"
        elif name:
            return name
        
        return ''
    
    return ''


def extract_all_findings(data: dict, provider: str) -> list[dict]:
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
                'rationale': strip_html_tags(finding.get('rationale', '')),
                'remediation': strip_html_tags(finding.get('remediation') or ''),
                'references': '; '.join(finding.get('references') or []) if isinstance(finding.get('references'), list) else str(finding.get('references') or ''),
                'compliance': json.dumps(finding.get('compliance')) if finding.get('compliance') else '',
            }
            
            if items:
                # One row per affected resource
                for item_path in items:
                    row = base_info.copy()
                    row['resource_path'] = item_path
                    row['resource_id'] = get_resource_id(data, item_path, provider)
                    row['scout_id'] = extract_scout_id(item_path)
                    findings_list.append(row)
            else:
                # No specific items - just one row for the finding
                row = base_info.copy()
                row['resource_path'] = ''
                row['resource_id'] = ''
                row['scout_id'] = ''
                findings_list.append(row)
    
    return findings_list


def detect_provider(data: dict) -> str:
    """Detect cloud provider from ScoutSuite data."""
    provider_code = data.get('provider_code', '').lower()
    if provider_code:
        return provider_code
    
    # Fallback: check service names
    services = data.get('services', {})
    if 'ec2' in services or 'iam' in services or 's3' in services:
        return 'aws'
    elif 'virtualmachines' in services or 'storageaccounts' in services or 'aad' in services:
        return 'azure'
    elif 'computeengine' in services or 'cloudstorage' in services:
        return 'gcp'
    
    return 'unknown'


def write_csv(findings: list[dict], output_path: str):
    """Write findings to CSV."""
    if not findings:
        print("No findings found.")
        return
    
    fieldnames = [
        'account_id', 'environment', 'service', 'finding_id', 'description',
        'level', 'flagged', 'flagged_items', 'checked_items', 'scout_id', 'resource_id', 'resource_path',
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
    provider = detect_provider(data)
    print(f"Detected provider: {provider}")
    
    findings = extract_all_findings(data, provider)
    write_csv(findings, output_path)


if __name__ == '__main__':
    main()