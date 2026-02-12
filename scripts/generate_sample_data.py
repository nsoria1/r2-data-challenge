"""Generate sample CSV data for testing the pipeline."""

import argparse
import csv
import random
import uuid
import string
from datetime import datetime, timedelta
from pathlib import Path
from faker import Faker

fake = Faker()
Faker.seed(42)
random.seed(42)


def generate_store_group():
    """Generate 8 hex chars uppercase for store_group."""
    return ''.join(random.choices('0123456789ABCDEF', k=8))


def generate_receipt_token():
    """Generate 5-30 alphanumeric chars for receipt_token."""
    length = random.randint(5, 30)
    return ''.join(random.choices(string.ascii_uppercase + string.digits, k=length))


def generate_stores_csv(output_dir: Path, batch_date: str, with_header: bool = True):
    """Generate stores CSV with valid and invalid records."""
    filename = output_dir / f"stores_{batch_date}.csv"
    
    stores = []
    
    for i in range(50):
        stores.append({
            'store_group': generate_store_group(),
            'store_token': str(uuid.uuid4()),
            'store_name': fake.company()
        })
    
    for i in range(50, 55):
        if i < 52:
            stores.append({
                'store_group': generate_store_group(),
                'store_token': str(uuid.uuid4()),
                'store_name': ''
            })
        else:
            stores.append({
                'store_group': generate_store_group(),
                'store_token': str(uuid.uuid4()),
                'store_name': 'A' * 250
            })
    
    with open(filename, 'w', newline='') as f:
        writer = csv.DictWriter(f, fieldnames=['store_group', 'store_token', 'store_name'])
        if with_header:
            writer.writeheader()
        writer.writerows(stores)
    
    print(f"Generated {filename} ({len(stores)} records, header={with_header})")
    return [s['store_token'] for s in stores[:50]]


def generate_sales_csv(output_dir: Path, batch_date: str, date_offset: int, store_tokens: list, with_header: bool = True):
    """Generate sales CSV with valid, invalid, and duplicate records."""
    filename = output_dir / f"sales_{batch_date}.csv"
    
    transactions = []
    base_date = datetime.strptime(batch_date, '%Y%m%d') - timedelta(days=date_offset)
    
    for i in range(185):
        trans_time = base_date + timedelta(hours=random.randint(0, 23), minutes=random.randint(0, 59))
        transactions.append({
            'store_token': random.choice(store_tokens),
            'transaction_id': str(uuid.uuid4()),
            'receipt_token': generate_receipt_token(),
            'transaction_time': trans_time.strftime('%Y%m%dT%H%M%S.000'),
            'amount': f'${random.uniform(10, 500):.2f}',
            'user_role': random.choice(['cashier', 'manager', 'supervisor'])
        })
    
    for i in range(185, 200):
        trans_time = base_date + timedelta(hours=random.randint(0, 23))
        if i < 193:
            trans_time_str = 'INVALID_TIME'
        else:
            trans_time_str = trans_time.strftime('%Y%m%dT%H%M%S.000')
        
        if i >= 193:
            amount_str = 'NOT_A_NUMBER'
        else:
            amount_str = f'${random.uniform(10, 500):.2f}'
        
        transactions.append({
            'store_token': random.choice(store_tokens),
            'transaction_id': str(uuid.uuid4()),
            'receipt_token': generate_receipt_token(),
            'transaction_time': trans_time_str,
            'amount': amount_str,
            'user_role': random.choice(['cashier', 'manager'])
        })
    
    for i in range(10):
        dup_idx = random.randint(0, 100)
        dup = transactions[dup_idx].copy()
        dup['amount'] = f'${random.uniform(10, 500):.2f}'
        dup['receipt_token'] = generate_receipt_token()
        transactions.append(dup)
    
    with open(filename, 'w', newline='') as f:
        writer = csv.DictWriter(f, fieldnames=['store_token', 'transaction_id', 'receipt_token',
                                                'transaction_time', 'amount', 'user_role'])
        if with_header:
            writer.writeheader()
        writer.writerows(transactions)
    
    print(f"Generated {filename} ({len(transactions)} records, header={with_header})")


def main():
    parser = argparse.ArgumentParser(description='Generate sample CSV data')
    parser.add_argument('--output-dir', type=str, default='data/inbox', 
                        help='Output directory for CSV files')
    args = parser.parse_args()
    
    output_dir = Path(args.output_dir)
    output_dir.mkdir(parents=True, exist_ok=True)
    
    print("=== Generating sample data ===\n")
    
    # Generate files for current date
    batch_date = datetime.now().strftime('%Y%m%d')
    
    # Randomly omit headers (~30% chance) to test headerless file handling
    stores_header = random.random() > 0.3
    sales_header = random.random() > 0.3
    
    valid_store_tokens = generate_stores_csv(output_dir, batch_date, with_header=stores_header)
    
    # Sales file for current date
    generate_sales_csv(output_dir, batch_date, date_offset=0, store_tokens=valid_store_tokens, with_header=sales_header)
    
    print(f"\n=== Complete: 2 files generated in {output_dir} ===")


if __name__ == '__main__':
    main()