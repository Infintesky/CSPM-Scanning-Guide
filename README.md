# CSPM Scanning Guide

This repository contains Markdown documentation for different purposes and instructions on how to convert them into Word (`.docx`) format using Pandoc.

## Documentation Types

1. **Master Guide**
   - File: `src/Master Guide.md`
   - Description: The full guide for reference.

2. **Internal Usage**
   - File: `src/Internal Usage.md`
   - Description: Documentation for internal teams on how to run and export VA scan results.

3. **Client Onboarding**
   - File: `src/Client Onboarding.md`
   - Description: Information that needs to be provisioned from the client.

## Repository Structure

- `src/`– Contains all Markdown guides.  
- `distrib/` – Contains editable `.docx` files generated from the Markdown guides.  
- `assets/` – Contains screenshots used in the Markdown guides.  
- `output/` – Contains sample reports and exported files.  

## Generate DOCX from Markdown

To convert a Markdown file to a Word document, use the following command:

```bash
pandoc src/Master\ Guide.md -o distrib/Master\ Guide.docx
