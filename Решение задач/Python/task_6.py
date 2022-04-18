string = input().split(',')
N = int(input())

model = [int(string[i]) for i in range(len(string))]
for i in range(N):
    list_input=input().split(',')
    ticket_no=str(list_input[0])
    flight_id = int(list_input[1])
    if flight_id not in model:
        continue
    
    boarding=str(list_input[2])
    seat_no=str(list_input[3])

    list_output=[ticket_no, flight_id, boarding, seat_no]

    print(*list_output, sep=',', end='\n')
