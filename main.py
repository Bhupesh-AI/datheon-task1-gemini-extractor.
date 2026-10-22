"""Extract structured invoice data from text using Google Gemini."""

import os

from google import genai
from google.genai import types
from pydantic import BaseModel, Field


class LineItem(BaseModel):
    description: str = Field(description="Name of the item or service")
    amount: float = Field(description="Price of this item")


class InvoiceData(BaseModel):
    invoice_number: str = Field(description="The unique invoice number")
    vendor_name: str = Field(
        description="Name of the company or vendor issuing the invoice"
    )
    date: str = Field(description="Date of the invoice in YYYY-MM-DD format")
    currency: str = Field(description="Currency code, for example INR or USD")
    items: list[LineItem] = Field(
        description="List of purchased items with their prices"
    )
    total_amount: float = Field(description="Total monetary amount on the invoice")


SAMPLE_INVOICE_TEXT = """
INVOICE #INV-2026-0891
Issued by: TechSource Solutions Pvt Ltd
Date: October 18, 2026

Items Purchased:
1. Python Masterclass Subscription - Rs. 2999
2. Generative AI E-Book - Rs. 1500

Total Paid: 4499.00 INR
Thank you for your business!
"""


def extract_structured_json(invoice_text: str = SAMPLE_INVOICE_TEXT) -> InvoiceData:
    """Ask Gemini to extract an invoice, then validate its JSON with Pydantic."""
    api_key = os.environ.get("GEMINI_API_KEY")
    if not api_key:
        raise RuntimeError(
            "GEMINI_API_KEY is not set. Add it in Replit Secrets, then run again."
        )

    client = genai.Client(api_key=api_key)
    prompt = f"""
You are an expert data parsing assistant. Extract the required details from the
invoice below. Return only data that matches the provided schema. Use ISO
YYYY-MM-DD for the date and a standard three-letter currency code.

Invoice text:
{invoice_text}
"""

    response = client.models.generate_content(
        model="gemini-2.5-flash",
        contents=prompt,
        config=types.GenerateContentConfig(
            response_mime_type="application/json",
            response_schema=InvoiceData,
            temperature=0,
        ),
    )

    if not response.text:
        raise RuntimeError("Gemini returned an empty response.")

    invoice = InvoiceData.model_validate_json(response.text)

    print("--- RAW JSON OUTPUT FROM GEMINI ---")
    print(response.text)
    print("\n--- VALIDATED PYDANTIC OBJECT ---")
    print(invoice.model_dump_json(indent=2))
    return invoice


def main() -> int:
    try:
        extract_structured_json()
    except Exception as error:
        print(f"Invoice extraction failed: {error}")
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
