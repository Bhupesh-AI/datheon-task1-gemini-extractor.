# Gemini Invoice Extractor

A runnable Python example that sends the sample invoice text to Gemini, requests
structured JSON, validates the response with Pydantic, and prints both the raw
JSON and validated object.

## Run in Replit

1. Make sure the `GEMINI_API_KEY` Replit Secret is set.
2. Click **Run**. The workflow runs `python3 main.py`.

To run from the Shell instead:

```sh
python3 main.py
```

The sample invoice is in `SAMPLE_INVOICE_TEXT` in `main.py`. Edit that text to
try another invoice.

Gemini API usage may incur charges according to your Google AI account.
