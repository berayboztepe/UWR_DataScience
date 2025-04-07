def dhondt_method(votes, total_seats, threshold=0.05):
    total_votes = sum(votes.values())
    quotients = []
    
    print(f"All committees: {votes}")
    eligible_committees = {committee: vote for committee, vote in votes.items() if vote >= threshold * total_votes}
    print(f"Eligible Committees: {eligible_committees}")
    
    for committee, vote in eligible_committees.items():
        for seat in range(1, total_seats + 1):
            quotients.append((vote / seat, committee))
    
    quotients.sort(reverse=True, key=lambda x: x[0])
    
    seat_allocation = {committee: 0 for committee in eligible_committees}
    
    for i in range(total_seats):
        _, committee = quotients[i]
        seat_allocation[committee] += 1
    
    return seat_allocation

votes = {
    "Committee A": 100000,
    "Committee B": 80000,
    "Committee C": 40000,
    "Committee D": 30000,
    "Committee E": 10000
}

total_seats = 10

seat_distribution = dhondt_method(votes, total_seats)
print(seat_distribution)
