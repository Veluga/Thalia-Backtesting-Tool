m = map(int,input().split())
N = input().split()
A = set(input().split())
B = set(input().split())

score = 0
for a in A:
    if a in N:
        score += 1

for b in B:
    if b in N:
        score -= 1

print(score)