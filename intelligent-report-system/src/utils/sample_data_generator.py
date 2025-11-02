"""
Sample Data Generator for Testing
Creates synthetic data files for POC demonstration
"""
import pandas as pd
import numpy as np
from pathlib import Path
from datetime import datetime, timedelta
import random
from PIL import Image, ImageDraw, ImageFont

from src.config.settings import settings
from src.utils.logger import app_logger as logger

class SampleDataGenerator:
    """Generate sample data for testing"""
    
    def __init__(self, output_dir: Path = None):
        self.output_dir = output_dir or settings.SAMPLE_DATA_DIR
        self.output_dir.mkdir(parents=True, exist_ok=True)
        logger.info(f"Sample data will be saved to: {self.output_dir}")
    
    def generate_sales_data(self, num_rows: int = 1000) -> str:
        """Generate sample sales CSV data"""
        logger.info(f"Generating sales data with {num_rows} rows")
        
        regions = ['North', 'South', 'East', 'West', 'Central']
        products = ['Product A', 'Product B', 'Product C', 'Product D', 'Product E']
        sales_reps = [f'Rep_{i}' for i in range(1, 21)]
        
        data = {
            'date': [datetime.now() - timedelta(days=random.randint(0, 365)) for _ in range(num_rows)],
            'region': [random.choice(regions) for _ in range(num_rows)],
            'product': [random.choice(products) for _ in range(num_rows)],
            'sales_rep': [random.choice(sales_reps) for _ in range(num_rows)],
            'quantity': np.random.randint(1, 100, num_rows),
            'unit_price': np.random.uniform(10, 500, num_rows).round(2),
        }
        
        df = pd.DataFrame(data)
        df['total_amount'] = (df['quantity'] * df['unit_price']).round(2)
        df['date'] = df['date'].dt.strftime('%Y-%m-%d')
        
        # Sort by date
        df = df.sort_values('date')
        
        output_path = self.output_dir / 'sales_data.csv'
        df.to_csv(output_path, index=False)
        
        logger.info(f"Sales data saved to: {output_path}")
        return str(output_path)
    
    def generate_financial_report(self) -> str:
        """Generate sample financial report text"""
        logger.info("Generating financial report")
        
        report_text = """
QUARTERLY FINANCIAL REPORT - Q3 2024

Executive Summary:
The company demonstrated strong financial performance in Q3 2024, with total revenue reaching $45.2 million, 
representing a 15% year-over-year growth. Net profit margin improved to 18.5%, up from 16.2% in Q3 2023.

Revenue Breakdown:
- Product Sales: $32.5M (72% of total revenue)
- Service Revenue: $9.8M (22% of total revenue)
- Other Income: $2.9M (6% of total revenue)

Regional Performance:
North Region showed exceptional growth with 25% increase in sales, driven by successful launch of Product D.
However, South Region experienced a 5% decline due to increased competition and market saturation.

Key Highlights:
- Customer acquisition increased by 30% quarter-over-quarter
- Operating expenses were controlled at 45% of revenue
- Cash reserves increased to $78.3M
- Debt-to-equity ratio improved to 0.45

Challenges:
Supply chain disruptions in September impacted delivery timelines, resulting in delayed revenue recognition 
of approximately $3.2M which will be realized in Q4.

Outlook:
Management remains optimistic about Q4 performance, projecting revenue between $48M-$52M based on current 
pipeline and seasonal trends. The launch of Product E in November is expected to drive additional growth.

Risk Factors:
- Currency fluctuations in international markets
- Rising raw material costs
- Regulatory changes in key markets
- Competitive pressure from new market entrants

Conclusion:
The company continues to execute well on its strategic initiatives while maintaining strong financial health. 
Investment in R&D and market expansion positions us favorably for continued growth.
"""
        
        output_path = self.output_dir / 'financial_report.txt'
        with open(output_path, 'w') as f:
            f.write(report_text.strip())
        
        logger.info(f"Financial report saved to: {output_path}")
        return str(output_path)
    
    def generate_customer_feedback(self) -> str:
        """Generate sample customer feedback document"""
        logger.info("Generating customer feedback document")
        
        feedback_text = """
CUSTOMER FEEDBACK ANALYSIS - OCTOBER 2024

Summary of Customer Interactions:
This document compiles feedback received from 250 customer interactions across various channels including 
email, phone, and in-person meetings during October 2024.

Positive Feedback (65% of responses):
1. Product Quality: Customers consistently praised the durability and reliability of Product A and Product C.
   "The build quality exceeds expectations" - Customer #1523
   
2. Customer Service: Response time and resolution quality received high marks.
   Average satisfaction score: 4.6/5.0

3. User Experience: The new mobile app interface was well-received.
   "Much more intuitive than the previous version" - Customer #2891

Areas for Improvement (35% of responses):
1. Delivery Times: 45% of complaints related to longer-than-expected delivery windows.
   Customers in the West region particularly affected.
   
2. Product B Issues: Multiple reports of minor defects in recent Product B batches.
   Quality control team investigating. Estimated 3% defect rate.

3. Documentation: Technical documentation needs improvement.
   "Instructions could be clearer for setup" - Customer #3104

Feature Requests:
- Integration with third-party software (mentioned 78 times)
- Mobile app offline mode (mentioned 52 times)
- Bulk ordering discounts (mentioned 41 times)
- Extended warranty options (mentioned 35 times)

Customer Retention Analysis:
- Retention rate: 87% (up from 84% last quarter)
- Net Promoter Score: 68 (industry average: 45)
- Repeat purchase rate: 62%

Action Items:
1. Work with logistics partners to improve delivery times
2. Conduct thorough quality audit of Product B manufacturing
3. Update technical documentation with clearer instructions
4. Evaluate feasibility of top feature requests

Geographic Insights:
North and East regions show highest satisfaction levels (4.7/5.0 average)
South and West regions slightly lower (4.2/5.0 average) primarily due to delivery issues

Customer Segments:
- Enterprise customers: 92% satisfaction, requesting more dedicated support
- Small business: 85% satisfaction, price-sensitive
- Individual consumers: 88% satisfaction, seeking easier online ordering
"""
        
        output_path = self.output_dir / 'customer_feedback.txt'
        with open(output_path, 'w') as f:
            f.write(feedback_text.strip())
        
        logger.info(f"Customer feedback saved to: {output_path}")
        return str(output_path)
    
    def generate_sample_invoice_image(self) -> str:
        """Generate a simple invoice image for OCR testing"""
        logger.info("Generating sample invoice image")
        
        # Create image
        width, height = 800, 600
        image = Image.new('RGB', (width, height), 'white')
        draw = ImageDraw.Draw(image)
        
        # Try to use default font, fallback to basic if not available
        try:
            font_large = ImageFont.truetype("arial.ttf", 24)
            font_medium = ImageFont.truetype("arial.ttf", 18)
            font_small = ImageFont.truetype("arial.ttf", 14)
        except:
            font_large = ImageFont.load_default()
            font_medium = ImageFont.load_default()
            font_small = ImageFont.load_default()
        
        # Draw invoice content
        y_offset = 30
        
        # Header
        draw.text((50, y_offset), "INVOICE", fill='black', font=font_large)
        y_offset += 50
        
        # Invoice details
        invoice_text = [
            "Invoice Number: INV-2024-001234",
            "Date: October 28, 2024",
            "Due Date: November 28, 2024",
            "",
            "Bill To:",
            "Acme Corporation",
            "123 Business St",
            "New York, NY 10001",
            "",
            "Items:",
            "1. Product A - Quantity: 10 - Unit Price: $50.00 - Total: $500.00",
            "2. Product C - Quantity: 5 - Unit Price: $120.00 - Total: $600.00",
            "3. Service Fee - Quantity: 1 - Unit Price: $250.00 - Total: $250.00",
            "",
            "Subtotal: $1,350.00",
            "Tax (10%): $135.00",
            "Total Amount Due: $1,485.00",
            "",
            "Payment Terms: Net 30 days",
            "Please remit payment to the address above."
        ]
        
        for line in invoice_text:
            draw.text((50, y_offset), line, fill='black', font=font_small)
            y_offset += 25
        
        # Save image
        output_path = self.output_dir / 'sample_invoice.png'
        image.save(output_path)
        
        logger.info(f"Sample invoice image saved to: {output_path}")
        return str(output_path)
    
    def generate_all_samples(self) -> dict:
        """Generate all sample data files"""
        logger.info("Generating all sample data files")
        
        files = {
            'sales_csv': self.generate_sales_data(),
            'financial_report': self.generate_financial_report(),
            'customer_feedback': self.generate_customer_feedback(),
            'invoice_image': self.generate_sample_invoice_image()
        }
        
        logger.info(f"Generated {len(files)} sample files")
        return files

if __name__ == "__main__":
    generator = SampleDataGenerator()
    files = generator.generate_all_samples()
    print("\nGenerated sample files:")
    for name, path in files.items():
        print(f"  {name}: {path}")