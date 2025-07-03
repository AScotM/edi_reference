#!/usr/bin/env python3
"""
Enhanced EDI Document Reference Tool

A comprehensive utility for looking up EDI document types across various standards,
including ANSI X12, EDIFACT, TRADACOMS, VDA, and RosettaNet with rich metadata.
"""

import argparse
from typing import Dict, List, Optional
from textwrap import fill
from dataclasses import dataclass
from enum import Enum, auto

class Industry(Enum):
    """Industry sectors for EDI documents"""
    RETAIL = auto()
    HEALTHCARE = auto()
    MANUFACTURING = auto()
    LOGISTICS = auto()
    AUTOMOTIVE = auto()
    TECHNOLOGY = auto()
    FINANCE = auto()

@dataclass
class EdiStandard:
    """Metadata about an EDI standard"""
    name: str
    latest_version: str
    region: str
    governing_body: str
    year_established: int

@dataclass
class EdiDocument:
    """Complete metadata about an EDI document type"""
    code: str
    name: str
    description: str
    common_versions: List[str]
    industries: List[Industry]
    direction: str  # Inbound, Outbound, or Both
    transaction_flow: Optional[str] = None

# --- Constants and Data Structures ---
STANDARDS = {
    "ANSI_X12": EdiStandard(
        name="ANSI X12 (North American Standard)",
        latest_version="6030",
        region="North America",
        governing_body="ANSI",
        year_established=1979
    ),
    "EDIFACT": EdiStandard(
        name="EDIFACT (International Standard)",
        latest_version="D22B",
        region="Global",
        governing_body="UNECE",
        year_established=1987
    ),
    "TRADACOMS": EdiStandard(
        name="TRADACOMS (UK Retail Standard)",
        latest_version="v3",
        region="United Kingdom",
        governing_body="GS1 UK",
        year_established=1982
    ),
    "VDA": EdiStandard(
        name="VDA (German Automotive Standard)",
        latest_version="6.0",
        region="Germany",
        governing_body="VDA",
        year_established=1977
    ),
    "ROSETTANET": EdiStandard(
        name="RosettaNet (Technology Industry Standard)",
        latest_version="02.00.00",
        region="Global",
        governing_body="GS1",
        year_established=1998
    )
}

def get_edi_documents() -> Dict[str, Dict[str, EdiDocument]]:
    """Returns a complete dataset of EDI documents organized by standard"""
    return {
        STANDARDS["ANSI_X12"].name: {
            "204": EdiDocument(
                code="204",
                name="Motor Carrier Load Tender",
                description="A transportation order for shipping goods between locations",
                common_versions=["4010", "4030", "5010", "6030"],
                industries=[Industry.LOGISTICS, Industry.MANUFACTURING],
                direction="Outbound",
                transaction_flow="Shipper → Carrier"
            ),
            "210": EdiDocument(
                code="210",
                name="Motor Carrier Freight Details and Invoice",
                description="Detailed freight invoice from carrier to shipper",
                common_versions=["4010", "5010", "6030"],
                industries=[Industry.LOGISTICS],
                direction="Inbound",
                transaction_flow="Carrier → Shipper"
            ),
            "810": EdiDocument(
                code="810",
                name="Invoice",
                description="Electronic invoice document for billing purposes",
                common_versions=["4010", "5010", "6030"],
                industries=[Industry.RETAIL, Industry.MANUFACTURING, Industry.HEALTHCARE],
                direction="Both",
                transaction_flow="Supplier → Buyer or Service Provider → Client"
            ),
            "820": EdiDocument(
                code="820",
                name="Payment Order/Remittance Advice",
                description="Electronic funds transfer payment information",
                common_versions=["4010", "5010", "6030"],
                industries=[Industry.FINANCE, Industry.RETAIL, Industry.MANUFACTURING],
                direction="Outbound",
                transaction_flow="Payer → Payee"
            ),
            "834": EdiDocument(
                code="834",
                name="Benefit Enrollment and Maintenance",
                description="Health insurance enrollment information exchange",
                common_versions=["4010", "5010", "6030"],
                industries=[Industry.HEALTHCARE],
                direction="Both",
                transaction_flow="Employer → Insurance Carrier or Government Agency → Provider"
            ),
            "850": EdiDocument(
                code="850",
                name="Purchase Order",
                description="Buyer's formal request to purchase goods/services",
                common_versions=["4010", "5010", "6030"],
                industries=[Industry.RETAIL, Industry.MANUFACTURING, Industry.TECHNOLOGY],
                direction="Outbound",
                transaction_flow="Buyer → Supplier"
            ),
            "855": EdiDocument(
                code="855",
                name="Purchase Order Acknowledgment",
                description="Supplier's response accepting or rejecting a PO",
                common_versions=["4010", "5010", "6030"],
                industries=[Industry.RETAIL, Industry.MANUFACTURING],
                direction="Inbound",
                transaction_flow="Supplier → Buyer"
            ),
            "856": EdiDocument(
                code="856",
                name="Advance Shipping Notice",
                description="Detailed shipment information prior to delivery",
                common_versions=["4010", "5010", "6030"],
                industries=[Industry.RETAIL, Industry.MANUFACTURING, Industry.LOGISTICS],
                direction="Outbound",
                transaction_flow="Supplier → Buyer"
            ),
            "940": EdiDocument(
                code="940",
                name="Warehouse Shipping Order",
                description="Instruction to warehouse to ship goods",
                common_versions=["4010", "5010", "6030"],
                industries=[Industry.LOGISTICS, Industry.RETAIL],
                direction="Outbound",
                transaction_flow="Retailer → Warehouse"
            ),
            "945": EdiDocument(
                code="945",
                name="Warehouse Shipping Advice",
                description="Confirmation of warehouse shipment",
                common_versions=["4010", "5010", "6030"],
                industries=[Industry.LOGISTICS, Industry.RETAIL],
                direction="Inbound",
                transaction_flow="Warehouse → Retailer"
            ),
            "997": EdiDocument(
                code="997",
                name="Functional Acknowledgment",
                description="Technical confirmation of received EDI transmission",
                common_versions=["4010", "5010", "6030"],
                industries=[Industry.RETAIL, Industry.MANUFACTURING, Industry.HEALTHCARE],
                direction="Both",
                transaction_flow="Between trading partners"
            )
        },
        STANDARDS["EDIFACT"].name: {
            "DESADV": EdiDocument(
                code="DESADV",
                name="Dispatch Advice",
                description="Notification of goods dispatched (similar to X12 856)",
                common_versions=["D96A", "D00B", "D22B"],
                industries=[Industry.LOGISTICS, Industry.MANUFACTURING],
                direction="Outbound",
                transaction_flow="Supplier → Buyer"
            ),
            "IFCSUM": EdiDocument(
                code="IFCSUM",
                name="International Forwarding and Consolidation Summary",
                description="Shipping consolidation details for international logistics",
                common_versions=["D96A", "D00B", "D22B"],
                industries=[Industry.LOGISTICS],
                direction="Both",
                transaction_flow="Between logistics providers"
            ),
            "INVOIC": EdiDocument(
                code="INVOIC",
                name="Invoice",
                description="International invoice document for billing",
                common_versions=["D96A", "D00B", "D22B"],
                industries=[Industry.RETAIL, Industry.MANUFACTURING],
                direction="Outbound",
                transaction_flow="Supplier → Buyer"
            ),
            "ORDERS": EdiDocument(
                code="ORDERS",
                name="Purchase Order",
                description="International purchase order document",
                common_versions=["D96A", "D00B", "D22B"],
                industries=[Industry.RETAIL, Industry.MANUFACTURING],
                direction="Outbound",
                transaction_flow="Buyer → Supplier"
            ),
            "ORDRSP": EdiDocument(
                code="ORDRSP",
                name="Order Response",
                description="Response to a purchase order (acceptance/rejection)",
                common_versions=["D96A", "D00B", "D22B"],
                industries=[Industry.RETAIL, Industry.MANUFACTURING],
                direction="Inbound",
                transaction_flow="Supplier → Buyer"
            ),
            "PRICAT": EdiDocument(
                code="PRICAT",
                name="Price/Sales Catalog",
                description="Product catalog with pricing information",
                common_versions=["D96A", "D00B", "D22B"],
                industries=[Industry.RETAIL, Industry.MANUFACTURING],
                direction="Outbound",
                transaction_flow="Supplier → Buyer"
            ),
            "RECADV": EdiDocument(
                code="RECADV",
                name="Receiving Advice",
                description="Notification of goods received (similar to X12 861)",
                common_versions=["D96A", "D00B", "D22B"],
                industries=[Industry.RETAIL, Industry.MANUFACTURING],
                direction="Inbound",
                transaction_flow="Buyer → Supplier"
            )
        },
        STANDARDS["TRADACOMS"].name: {
            "DELHDR": EdiDocument(
                code="DELHDR",
                name="Delivery Header",
                description="Delivery instructions for UK retail orders",
                common_versions=["v1", "v2", "v3"],
                industries=[Industry.RETAIL],
                direction="Outbound",
                transaction_flow="Supplier → Retailer"
            ),
            "INVFIL": EdiDocument(
                code="INVFIL",
                name="Invoice File",
                description="UK retail-specific invoice format",
                common_versions=["v1", "v2", "v3"],
                industries=[Industry.RETAIL],
                direction="Outbound",
                transaction_flow="Supplier → Retailer"
            ),
            "ORDHDR": EdiDocument(
                code="ORDHDR",
                name="Order Header",
                description="UK retail purchase order document",
                common_versions=["v1", "v2", "v3"],
                industries=[Industry.RETAIL],
                direction="Outbound",
                transaction_flow="Retailer → Supplier"
            ),
            "ORDCHG": EdiDocument(
                code="ORDCHG",
                name="Order Change",
                description="Modification to an existing purchase order",
                common_versions=["v1", "v2", "v3"],
                industries=[Industry.RETAIL],
                direction="Both",
                transaction_flow="Between retailer and supplier"
            )
        },
        STANDARDS["VDA"].name: {
            "4905": EdiDocument(
                code="4905",
                name="Delivery Schedule",
                description="Just-in-time delivery schedule for automotive manufacturing",
                common_versions=["4.3", "5.0", "6.0"],
                industries=[Industry.AUTOMOTIVE],
                direction="Outbound",
                transaction_flow="OEM → Supplier"
            ),
            "4913": EdiDocument(
                code="4913",
                name="Invoice",
                description="Automotive industry-specific invoice format",
                common_versions=["4.3", "5.0", "6.0"],
                industries=[Industry.AUTOMOTIVE],
                direction="Outbound",
                transaction_flow="Supplier → OEM"
            ),
            "4981": EdiDocument(
                code="4981",
                name="Shipping Notification",
                description="Advanced shipping notice for automotive parts",
                common_versions=["4.3", "5.0", "6.0"],
                industries=[Industry.AUTOMOTIVE],
                direction="Outbound",
                transaction_flow="Supplier → OEM"
            )
        },
        STANDARDS["ROSETTANET"].name: {
            "3A4": EdiDocument(
                code="3A4",
                name="Purchase Order",
                description="High-tech industry purchase order",
                common_versions=["02.00.00"],
                industries=[Industry.TECHNOLOGY],
                direction="Outbound",
                transaction_flow="Buyer → Supplier"
            ),
            "3A8": EdiDocument(
                code="3A8",
                name="Purchase Order Change",
                description="Modification to a technology purchase order",
                common_versions=["02.00.00"],
                industries=[Industry.TECHNOLOGY],
                direction="Both",
                transaction_flow="Between trading partners"
            ),
            "3B2": EdiDocument(
                code="3B2",
                name="Shipping Notification",
                description="Advanced shipping notice for technology products",
                common_versions=["02.00.00"],
                industries=[Industry.TECHNOLOGY],
                direction="Outbound",
                transaction_flow="Supplier → Buyer"
            ),
            "4B2": EdiDocument(
                code="4B2",
                name="Advance Shipment Notification",
                description="Detailed shipment information for technology supply chain",
                common_versions=["02.00.00"],
                industries=[Industry.TECHNOLOGY],
                direction="Outbound",
                transaction_flow="Supplier → Buyer"
            )
        }
    }

# --- Core Functions ---
def list_standards(detailed: bool = False) -> None:
    """Display all supported EDI standards with optional details"""
    print("\nSupported EDI Standards:\n")
    for std in STANDARDS.values():
        print(f"• {std.name}")
        if detailed:
            print(f"  - Latest Version: {std.latest_version}")
            print(f"  - Region: {std.region}")
            print(f"  - Governing Body: {std.governing_body}")
            print(f"  - Established: {std.year_established}\n")

def list_edi_documents(filter_standard: Optional[str] = None, 
                      filter_industry: Optional[str] = None) -> None:
    """List all EDI documents with filtering options"""
    edi_docs = get_edi_documents()
    
    if filter_standard:
        edi_docs = {k: v for k, v in edi_docs.items() 
                   if filter_standard.lower() in k.lower()}
        if not edi_docs:
            print(f"\nNo standards found matching '{filter_standard}'")
            return

    print("\nEDI Document Reference:\n")
    for standard, docs in edi_docs.items():
        print(f"== {standard} ==")
        print(f"{'-' * (len(standard) + 4)}\n")
        
        for code in sorted(docs.keys(), key=lambda x: (int(x) if x.isdigit() else x)):
            doc = docs[code]
            
            # Apply industry filter if specified
            if filter_industry:
                if not any(filter_industry.lower() in ind.name.lower() 
                         for ind in doc.industries):
                    continue
            
            print(f"• {code}: {doc.name}")
            print(f"  Direction: {doc.direction}")
            if doc.transaction_flow:
                print(f"  Flow: {doc.transaction_flow}")
            print(f"  Versions: {', '.join(doc.common_versions)}")
            print(f"  Industries: {', '.join(ind.name for ind in doc.industries)}")
            print(f"  Description: {fill(doc.description, width=70, subsequent_indent='    ')}\n")

def search_edi_code(code: str, show_all: bool = False) -> None:
    """Search for EDI documents with flexible matching"""
    edi_docs = get_edi_documents()
    code = code.upper()
    found = False
    
    print(f"\nSearch Results for '{code}':\n")
    for standard, docs in edi_docs.items():
        for doc_code, doc in docs.items():
            if code in doc_code or show_all:
                print(f"== {standard} ==")
                print(f"• {doc_code}: {doc.name}")
                print(f"  Direction: {doc.direction}")
                if doc.transaction_flow:
                    print(f"  Flow: {doc.transaction_flow}")
                print(f"  Versions: {', '.join(doc.common_versions)}")
                print(f"  Industries: {', '.join(ind.name for ind in doc.industries)}")
                print(f"  Description: {fill(doc.description, width=70, subsequent_indent='    ')}\n")
                found = True
    
    if not found:
        print(f"No EDI documents found matching '{code}'")

# --- Command Line Interface ---
def main():
    parser = argparse.ArgumentParser(
        description="Enhanced EDI Document Reference Tool",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""Examples:
  List all X12 documents:    %(prog)s -s X12
  Search for invoices:       %(prog)s -c INVOIC -a
  Show healthcare docs:      %(prog)s -i healthcare
  View standard details:     %(prog)s -l -d"""
    )
    
    parser.add_argument(
        "-s", "--standard",
        type=str,
        help="Filter by EDI standard (e.g., 'X12' or 'EDIFACT')"
    )
    parser.add_argument(
        "-i", "--industry",
        type=str,
        help="Filter by industry (e.g., 'healthcare', 'automotive')"
    )
    parser.add_argument(
        "-c", "--code",
        type=str,
        help="Search for specific EDI document code (supports partial matches)"
    )
    parser.add_argument(
        "-a", "--all",
        action="store_true",
        help="Show all partial matches when searching"
    )
    parser.add_argument(
        "-l", "--list-standards",
        action="store_true",
        help="List all supported EDI standards"
    )
    parser.add_argument(
        "-d", "--detailed",
        action="store_true",
        help="Show detailed standard information"
    )
    
    args = parser.parse_args()
    
    if args.list_standards:
        list_standards(args.detailed)
    elif args.code:
        search_edi_code(args.code, args.all)
    else:
        list_edi_documents(args.standard, args.industry)

if __name__ == "__main__":
    main()
