def validate_keys(data):
    bad_records = []
    required = ['ticket_id', 'customer_id', 'category', 'resolution_minutes', 'escalated']
    for row in data:
        if not all(key in row for key in required):
            bad_records.append(row)
    return bad_records

def validate_resolution(data):
    bad_records = []
    for row in data:
        value = row.get('resolution_minutes')
        if type(value) != int:
            bad_records.append(row)
    return bad_records

def get_avg_resolution(data):
    totals = {} 
    counts = {} 
    for t in data:
        cat = t['category']
        time = t['resolution_minutes']
        if cat not in totals:
            totals[cat] = 0
            counts[cat] = 0
        totals[cat] += time
        counts[cat] += 1
    results = {}
    for cat in totals:
        results[cat] = round(totals[cat] / counts[cat], 2)
    return results

def get_customer_counts(data):
    counts = {}
    for t in data:
        cust = t['customer_id']
        counts[cust] = counts.get(cust, 0) + 1
    return counts

def get_escalation_rates(data):
    if not data:
        return {}
    total_esc = sum(1 for t in data if t['escalated'])
    overall_rate = total_esc / len(data)
    results = {'overall': round(overall_rate, 2)}
    cat_counts = {} 
    for t in data:
        cat = t['category']
        if cat not in cat_counts:
            cat_counts[cat] = [0, 0]
        cat_counts[cat][1] += 1           
        if t['escalated']:
            cat_counts[cat][0] += 1       
    for cat, val in cat_counts.items():
        results[cat] = round(val[0] / val[1], 2)
    return results