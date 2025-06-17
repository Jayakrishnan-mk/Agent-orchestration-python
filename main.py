

mock_prs = [
    { 'id': 1, "category": "Football" },
    { 'id': 2, "category": "Cricket" }
];


def fetch_prs() :
    return mock_prs;


def recommend_supplier(category) :
    if category == 'Football' :
        return "Premier League";
    elif category == 'Cricket' :
        return "ICC";
    else :
        return "Sports";


supplier = recommend_supplier('Football');
print(f"Recommended Supplier: {supplier}")


def create_rfq(pr, supplier) :
    return {
        "rfq_id": "rfq-" + str(pr["id"]),
        "category": pr["category"],
        "supplier": supplier
    }


def main() :
    prs = fetch_prs();
    print(f"Fetched PR: {prs}")

    for pr in prs:
        supplier = recommend_supplier(pr["category"]);
        rfq = create_rfq(pr,supplier);
        print("RFQ generated: ", rfq);


if __name__ == "__main__":
    main();