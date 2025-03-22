import axelrod as axl

# 1. Стратегія Grim Trigger
class GrimTrigger(axl.Player):
    name = "Grim Trigger"
    def strategy(self, opponent):
        return axl.Action.D if axl.Action.D in opponent.history else axl.Action.C

# 2. Набір стратегій для аналізу
strategies = [
    axl.TitForTat(), # "Око за око"
    GrimTrigger(),   # "Грізне покарання"
    axl.Defector(),  # "Зрадник"
]

# 3. Кількість ітерацій
ROUNDS = 15

# 4. Проведення матчів між усіма парами
for i in range(len(strategies)):
    for j in range(i + 1, len(strategies)):
        player1 = strategies[i]
        player2 = strategies[j]
        match = axl.Match((player1, player2), turns=ROUNDS)
        match.play()

        print(f"\n Матч: {player1.name} vs {player2.name}")
        print("Історія дій:")
        for round_num, (a1, a2) in enumerate(match.result, 1):
            print(f"  Раунд {round_num}: {a1} vs {a2}")
        print("Бали:")
        print(f"  {player1.name}: {match.final_score()[0]}")
        print(f"  {player2.name}: {match.final_score()[1]}")
        print("Висновок:", end=" ")
        if match.final_score()[0] > match.final_score()[1]:
            print(f"{player1.name} виграв.")
        elif match.final_score()[0] < match.final_score()[1]:
            print(f"{player2.name} виграв.")
        else:
            print("Нічия.")

        # Очищення історії для наступного матчу
        player1.reset()
        player2.reset()
