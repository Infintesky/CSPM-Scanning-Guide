#!/usr/bin/env python3
"""
Script to convert Prowler JSON findings to CSV format
Usage:
    python prowler_json2csv.py input.json -o output.csv
"""

import json
import csv
import argparse
import sys
from pathlib import Path


def flatten_compliance(compliance_dict):
    """Convert compliance dict to a readable string."""
    if not compliance_dict:
        return ""
    parts = []
    for framework, controls in compliance_dict.items():
        controls_str = ", ".join(str(c) for c in controls)
        parts.append(f"{framework}: [{controls_str}]")
    return "; ".join(parts)


def extract_fields(entry):
    """Extract relevant fields from a single JSON entry."""
    resources = entry.get("resources", [])
    resource = resources[0] if resources else {}
    resource_data = resource.get("data", {})
    resource_metadata = resource_data.get("metadata", {})
    
    cloud = entry.get("cloud", {})
    account = cloud.get("account", {})
    
    finding_info = entry.get("finding_info", {})
    
    remediation = entry.get("remediation", {})
    
    unmapped = entry.get("unmapped", {})
    compliance = unmapped.get("compliance", {})
    
    return {
        "message": entry.get("message", ""),
        "severity": entry.get("severity", ""),
        "severity_id": entry.get("severity_id", ""),
        "status": entry.get("status", ""),
        "status_code": entry.get("status_code", ""),
        "status_detail": entry.get("status_detail", ""),
        "event_code": entry.get("metadata", {}).get("event_code", ""),
        "prowler_version": entry.get("metadata", {}).get("product", {}).get("version", ""),
        "finding_uid": finding_info.get("uid", ""),
        "finding_title": finding_info.get("title", ""),
        "finding_desc": finding_info.get("desc", ""),
        "finding_types": ", ".join(finding_info.get("types", [])),
        "created_time_dt": finding_info.get("created_time_dt", ""),
        "cloud_provider": cloud.get("provider", ""),
        "cloud_region": cloud.get("region", ""),
        "account_uid": account.get("uid", ""),
        "account_name": account.get("name", ""),
        "account_type": account.get("type", ""),
        "resource_uid": resource.get("uid", ""),
        "resource_name": resource.get("name", ""),
        "resource_type": resource.get("type", ""),
        "resource_region": resource.get("region", ""),
        "resource_group": resource.get("group", {}).get("name", ""),
        "resource_status": resource_metadata.get("status", ""),
        "risk_details": entry.get("risk_details", ""),
        "remediation_desc": remediation.get("desc", ""),
        "remediation_references": ", ".join(remediation.get("references", [])),
        "related_url": unmapped.get("related_url", ""),
        "compliance": flatten_compliance(compliance),
        "activity_name": entry.get("activity_name", ""),
        "type_name": entry.get("type_name", ""),
        "category_name": entry.get("category_name", ""),
        "class_name": entry.get("class_name", ""),
    }


def load_json_file(input_path):
    """Load JSON from file, handling both JSON array and JSONL formats."""
    entries = []
    
    with open(input_path, 'r', encoding='utf-8') as f:
        content = f.read().strip()
    
    # Try parsing as a single JSON (object or array)
    try:
        data = json.loads(content)
        if isinstance(data, list):
            entries = data
        else:
            entries = [data]
        return entries
    except json.JSONDecodeError:
        pass
    
    # Try parsing as JSONL (one JSON object per line)
    with open(input_path, 'r', encoding='utf-8') as f:
        for line_num, line in enumerate(f, 1):
            line = line.strip()
            if not line:
                continue
            try:
                entry = json.loads(line)
                entries.append(entry)
            except json.JSONDecodeError as e:
                print(f"Warning: Could not parse line {line_num}: {e}", file=sys.stderr)
    
    return entries


def convert_json_to_csv(input_path, output_path):
    """Convert JSON file to CSV."""
    entries = load_json_file(input_path)
    
    if not entries:
        print("No valid JSON entries found in input file.", file=sys.stderr)
        sys.exit(1)
    
    rows = [extract_fields(entry) for entry in entries]
    
    fieldnames = list(rows[0].keys())
    
    with open(output_path, 'w', newline='', encoding='utf-8') as csvfile:
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(rows)
    
    print(f"Successfully converted {len(rows)} entries to {output_path}")


def main():
    parser = argparse.ArgumentParser(
        description="Convert Prowler JSON findings to CSV format"
    )
    parser.add_argument(
        "input_file",
        help="Input JSON file (supports single object, array, or JSONL format)"
    )
    parser.add_argument(
        "-o", "--output",
        help="Output CSV file (default: input filename with .csv extension)"
    )
    
    args = parser.parse_args()
    
    input_path = Path(args.input_file)
    
    if not input_path.exists():
        print(f"Error: Input file '{input_path}' not found.", file=sys.stderr)
        sys.exit(1)
    
    if args.output:
        output_path = Path(args.output)
    else:
        output_path = input_path.with_suffix('.csv')
    
    convert_json_to_csv(input_path, output_path)


if __name__ == "__main__":
    main()